import genanki
import csv
from pathlib import Path

# Deck hierarchy: child of Deep Dive Segment
DECK_NAME = "AZ-104 Study Guide::Deep Dive Segments::Azure File Security Deep Dive"
DECK_ID = 2251412312
NOTE_TYPE_ID = 1607392310

# Use main template exactly
main_front_template = r"""
<div style="color:#e5e7eb; font-family:system-ui, -apple-system, Segoe UI, Roboto, Arial;">
  <div style="font-size:20px; margin-bottom:16px;">{{Question}}</div>
  <div class="choice" data-key="A">A. {{A}}</div>
  <div class="choice" data-key="B">B. {{B}}</div>
  <div class="choice" data-key="C">C. {{C}}</div>
  <div class="choice" data-key="D">D. {{D}}</div>
</div>
"""

main_back_template = r"""
<div style="color:#e5e7eb; font-family:system-ui;">
  <div style="font-size:20px; margin-bottom:16px;">{{Question}}</div>

  <div class="choice {{#isCorrectA}}correct{{/isCorrectA}}" data-key="A">A. {{A}}</div>
  <div class="choice {{#isCorrectB}}correct{{/isCorrectB}}" data-key="B">B. {{B}}</div>
  <div class="choice {{#isCorrectC}}correct{{/isCorrectC}}" data-key="C">C. {{C}}</div>
  <div class="choice {{#isCorrectD}}correct{{/isCorrectD}}" data-key="D">D. {{D}}</div>

  <div style="background:#2ecc71; color:#000; border-radius:6px; padding:12px; margin-top:16px;">
    <strong>Explanation</strong><br>
    {{Explanation}}
  </div>
</div>
"""

main_css_style = """
.card {
  background: linear-gradient(135deg, #0b1220 0%, #111827 50%, #0b1220 100%) !important;
  color: #e5e7eb;
  min-height: 100vh;
  padding: 16px;
}

.choice {
  background: #ffffff;
  color: #0f172a;
  border:1px solid #0f172a;
  border-radius:6px;
  padding:10px 12px;
  margin:8px 0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.18);
}

.choice.correct {
  background:#2ecc71 !important;
  color: #0f172a;
  border-color:#27ae60;
}
"""

mcq_model = genanki.Model(
  NOTE_TYPE_ID,
  'MCQ',
  fields=[
    {'name':'Question'},
    {'name':'A'},
    {'name':'B'},
    {'name':'C'},
    {'name':'D'},
    {'name':'Correct'},
    {'name':'Explanation'},
    {'name':'Tags'},
    {'name':'Source'},
    {'name':'Batch'},
    {'name':'isCorrectA'},
    {'name':'isCorrectB'},
    {'name':'isCorrectC'},
    {'name':'isCorrectD'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': main_front_template,
      'afmt': main_back_template,
    }
  ],
  css=main_css_style,
)

deck = genanki.Deck(DECK_ID, DECK_NAME)

csv_path = Path('/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/AZ-104-Critical-Priorities-Study-Deck/Deep Dive Segment/Azure File Security Deep Dive.csv')
if not csv_path.exists():
  raise FileNotFoundError(f'CSV not found: {csv_path}')

with csv_path.open('r', encoding='utf-8') as f:
  reader = csv.DictReader(f)
  for row in reader:
    correct_key = (row.get('Correct') or '').strip().upper()
    note = genanki.Note(
      model=mcq_model,
      fields=[
        row['Question'],
        row['ChoiceA'],
        row['ChoiceB'],
        row['ChoiceC'],
        row['ChoiceD'],
        correct_key,
        row.get('Explanation', ''),
        row.get('Tags', ''),
        row.get('Source', ''),
        row.get('Batch', ''),
        '1' if correct_key == 'A' else '',
        '1' if correct_key == 'B' else '',
        '1' if correct_key == 'C' else '',
        '1' if correct_key == 'D' else '',
      ],
      tags=row.get('Tags', '').split(';') if row.get('Tags') else [],
    )
    deck.add_note(note)

package = genanki.Package(deck)
package.media_files = []
output_path = Path('/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZURE_FILE_SECURITY_DEEP_DIVE.apkg')
package.write_to_file(str(output_path))
print(f"Wrote {output_path}")
