# Anki MCQ Template Snapshots (Canonical)

This file snapshots the canonical templates used across generators like `generate_azure_monitor_mcq_apkg.py`. Use these as the single source of truth for future decks.

## Model and Fields
- Note Type ID: `1607392310`
- Fields (in order):
  - Question
  - A
  - B
  - C
  - D
  - Correct
  - Explanation
  - Tags
  - Source
  - Batch
  - isCorrectA
  - isCorrectB
  - isCorrectC
  - isCorrectD

## Front Template (qfmt)
```
<div style="color:#e5e7eb; font-family:system-ui, -apple-system, Segoe UI, Roboto, Arial;">
  <div style="font-size:20px; margin-bottom:16px;">{{Question}}</div>
  <div class="choice" data-key="A">A. {{A}}</div>
  <div class="choice" data-key="B">B. {{B}}</div>
  <div class="choice" data-key="C">C. {{C}}</div>
  <div class="choice" data-key="D">D. {{D}}</div>
</div>
```

## Back Template (afmt)
```
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
```

## CSS
```
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
```

## Generator Boilerplate
- Deck hierarchy example: `AZ-104 Study Guide::Deep Dive Segments::<Topic Name> Deep Dive`
- Map CSV headers to fields:
  - `ChoiceA` → `A`, `ChoiceB` → `B`, `ChoiceC` → `C`, `ChoiceD` → `D`
  - Normalize `Correct` to A/B/C/D and set flags:
    - `isCorrectA` = `1` if `Correct == 'A'` else `''` (same for B/C/D)
- Tag parsing tip:
  - Use `row.get('Tags', '').split(';')` when tags are semicolon-delimited; otherwise `split(',')`.

## Minimal Code Skeleton
```
mcq_model = genanki.Model(
  1607392310,
  'MCQ',
  fields=[ ...as above... ],
  templates=[{'name':'Card 1','qfmt': main_front_template, 'afmt': main_back_template}],
  css=main_css_style,
)

deck = genanki.Deck(DECK_ID, DECK_NAME)

correct_key = (row.get('Correct') or '').strip().upper()
note = genanki.Note(
  model=mcq_model,
  fields=[row['Question'], row['ChoiceA'], row['ChoiceB'], row['ChoiceC'], row['ChoiceD'], correct_key,
          row.get('Explanation',''), row.get('Tags',''), row.get('Source',''), row.get('Batch',''),
          '1' if correct_key=='A' else '', '1' if correct_key=='B' else '', '1' if correct_key=='C' else '', '1' if correct_key=='D' else ''],
  tags=row.get('Tags', '').split(';') if row.get('Tags') else [],
)
```
