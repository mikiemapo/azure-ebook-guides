#!/usr/bin/env python3
from flask import Flask, g, jsonify, request, send_from_directory, render_template
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import json

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'quiz_mastery.db'

app = Flask(__name__, static_folder=str(BASE_DIR / 'static'), template_folder=str(BASE_DIR / 'templates'))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(str(DB_PATH))
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id TEXT PRIMARY KEY,
        source TEXT,
        question TEXT,
        answer TEXT,
        times_seen INTEGER DEFAULT 0,
        correct_total INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        last_seen TEXT,
        next_review TEXT,
        box TEXT DEFAULT 'new',
        tags TEXT
    )
    ''')
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def row_to_item(r):
    return {k: r[k] for k in r.keys()}

def iso_now():
    return datetime.utcnow().isoformat() + 'Z'

def add_days_iso(days:int):
    return (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def api_items():
    due = request.args.get('due', 'false').lower() == 'true'
    db = get_db()
    if due:
        now = datetime.utcnow().isoformat() + 'Z'
        cur = db.execute("SELECT * FROM items WHERE box!='mastered' OR (next_review IS NOT NULL AND next_review<=?) ORDER BY next_review IS NULL, next_review", (now,))
    else:
        cur = db.execute('SELECT * FROM items ORDER BY rowid DESC')
    rows = cur.fetchall()
    return jsonify([row_to_item(r) for r in rows])

@app.route('/api/mastered', methods=['GET'])
def api_mastered():
    db = get_db()
    cur = db.execute("SELECT * FROM items WHERE box='mastered' ORDER BY last_seen DESC")
    return jsonify([row_to_item(r) for r in cur.fetchall()])

@app.route('/api/answer', methods=['POST'])
def api_answer():
    data = request.get_json() or {}
    item_id = data.get('id')
    correct = bool(data.get('correct'))
    if not item_id:
        return jsonify({'error': 'missing id'}), 400
    db = get_db()
    cur = db.execute('SELECT * FROM items WHERE id=?', (item_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({'error': 'item not found'}), 404
    item = dict(row)
    # Update per algorithm
    times_seen = item.get('times_seen') or 0
    correct_total = item.get('correct_total') or 0
    streak = item.get('streak') or 0
    times_seen += 1
    last_seen = iso_now()
    next_review = None
    box = item.get('box') or 'new'
    if correct:
        correct_total += 1
        streak += 1
        if streak >= 3:
            box = 'mastered'
            next_review = None
        else:
            box = 'learning'
            if streak == 1:
                next_review = add_days_iso(1)
            elif streak == 2:
                next_review = add_days_iso(3)
            else:
                next_review = add_days_iso(7)
    else:
        streak = 0
        box = 'review'
        next_review = add_days_iso(1)

    db.execute('''
        UPDATE items SET times_seen=?, correct_total=?, streak=?, last_seen=?, next_review=?, box=? WHERE id=?
    ''', (times_seen, correct_total, streak, last_seen, next_review, box, item_id))
    db.commit()
    cur = db.execute('SELECT * FROM items WHERE id=?', (item_id,))
    return jsonify(row_to_item(cur.fetchone()))

@app.route('/api/import', methods=['POST'])
def api_import():
    payload = request.get_json() or {}
    items = payload.get('items') if isinstance(payload, dict) else payload
    if not items:
        return jsonify({'error': 'no items provided'}), 400
    db = get_db()
    count = 0
    for it in items:
        try:
            db.execute('''INSERT OR REPLACE INTO items (id, source, question, answer, times_seen, correct_total, streak, last_seen, next_review, box, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (
                it.get('id'), it.get('source'), it.get('question'), it.get('answer'), it.get('times_seen') or 0, it.get('correct_total') or 0, it.get('streak') or 0, it.get('last_seen'), it.get('next_review'), it.get('box') or 'new', json.dumps(it.get('tags') or [])
            ))
            count += 1
        except Exception as e:
            print('import error', e)
    db.commit()
    return jsonify({'imported': count})

@app.route('/api/export', methods=['GET'])
def api_export():
    db = get_db()
    cur = db.execute('SELECT * FROM items')
    rows = cur.fetchall()
    return jsonify({'items': [row_to_item(r) for r in rows]})

def ensure_sample_data():
    db = get_db()
    cur = db.execute('SELECT COUNT(*) as c FROM items')
    if cur.fetchone()['c'] == 0:
        sample = json.loads((BASE_DIR / 'sample_data.json').read_text())
        for it in sample.get('items', []):
            db.execute('''INSERT INTO items (id, source, question, answer, times_seen, correct_total, streak, last_seen, next_review, box, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (
                it.get('id'), it.get('source'), it.get('question'), it.get('answer'), it.get('times_seen') or 0, it.get('correct_total') or 0, it.get('streak') or 0, it.get('last_seen'), it.get('next_review'), it.get('box') or 'new', json.dumps(it.get('tags') or [])
            ))
        db.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
        ensure_sample_data()
    app.run(host='127.0.0.1', port=5000, debug=True)
