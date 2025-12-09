# ⚠️ ANKI IMPORT LOCATION - DO NOT CHANGE

## 🎯 **ALWAYS IMPORT FROM THIS FOLDER**

**File to import:** `AZ-104-Master-Study-Deck.apkg`

---

## 📋 Folder Structure (LOCKED - DO NOT CREATE NEW FOLDERS)

```
/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/
│
├── AZ-104-Critical-Priorities-Study-Deck/  (Git repo - CSV + Python script)
│   ├── AZ-104-Master-Questions.csv
│   ├── create_master_deck.py
│   └── AZ-104-Master-Study-Deck.apkg (generated here, then auto-copied)
│
└── Anki-Decks/ ← **YOU ARE HERE - IMPORT FROM THIS FOLDER**
    ├── README.md (this file)
    └── AZ-104-Master-Study-Deck.apkg ← **IMPORT THIS FILE**
```

---

## 🔄 Workflow

1. Edit questions in: `AZ-104-Critical-Priorities-Study-Deck/AZ-104-Master-Questions.csv`
2. Run: `cd AZ-104-Critical-Priorities-Study-Deck && python3 create_master_deck.py`
3. Script automatically copies .apkg to: **`Anki-Decks/`** ✅
4. Import from: **`Anki-Decks/AZ-104-Master-Study-Deck.apkg`** ✅

---

## ⛔ RULES

- **NEVER** create new folders for Anki decks
- **ALWAYS** import from `Anki-Decks/AZ-104-Master-Study-Deck.apkg`
- **NEVER** copy .apkg files manually (script does it automatically)
- If you see duplicate folders, DELETE them

---

## 📍 **ABSOLUTE PATH TO IMPORT FILE:**

```
/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ-104-Master-Study-Deck.apkg
```

**THIS IS THE ONLY LOCATION. NO OTHER FOLDERS.**

---

## 🎴 DECK FORMAT SPECIFICATION

### Card Template Structure (Based on Deep Dive Segments)

All decks use the **AZ-104 Master Questions Model** with the following format:

#### **Front Side (Question)**

- Displays: Question text + 4 MCQ choices (A, B, C, D)
- **NO highlighting** on any choices
- Clean gray background (#f9f9f9) for all choices
- User reads question and selects answer

#### **Back Side (Answer Reveal)**

```
[Question text + choices with correct answer HIGHLIGHTED GREEN]
─────────────────────────────────
✓ Answer: [Correct Letter] - [2-sentence explanation]
```

**Layout Components:**

1. **Question with Highlighted Choices:**

   - Question text displayed again
   - All 4 choices shown
   - **Correct answer:** Green background (#4CAF50), white text, bold
   - **Incorrect answers:** Gray background (#f9f9f9), dark text

2. **Answer Explanation Box:**
   - Separator line (horizontal rule)
   - Green background box (#4CAF50)
   - White text (readable on green)
   - Format: "Correct: [LETTER] - [explanation]"
   - Limited to 2 sentences (150 chars max)

#### **CSS Styling (Applied to All Cards)**

```css
.card {
  font-family: Arial, sans-serif;
  font-size: 18px;
  line-height: 1.6;
  color: black;
  background-color: white;
  padding: 20px;
}

.choice {
  background-color: #f9f9f9;
  border: 2px solid #cccccc;
  padding: 12px 16px;
  margin: 10px 0;
  border-radius: 8px;
  display: block;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: #333333;
  font-weight: normal;
}

.choice.correct {
  background-color: #4caf50; /* GREEN */
  border: 2px solid #45a049; /* darker green border */
  color: white; /* WHITE TEXT */
  font-weight: bold;
}
```

#### **Card Field Structure**

| Field                | Content                                | Visibility            |
| -------------------- | -------------------------------------- | --------------------- |
| `Question`           | Question + 4 choices (no highlighting) | FRONT only            |
| `QuestionWithAnswer` | Question + 4 choices (correct = green) | BACK only             |
| `Answer`             | "Correct: [X] - [explanation]"         | BACK only (green box) |
| `Tags`               | Comma-separated tags                   | Metadata              |

#### **Example Card Display**

**FRONT:**

```
Which of the following correctly describes role scope in Entra ID?

A) Role assignment is per-application only
B) Role assignment applies across all Azure resources and Entra ID
C) Scopes depend on the role type (directory-wide or delegated)
D) Role assignment is per-user device only
```

**BACK:**

```
Which of the following correctly describes role scope in Entra ID?

A) Role assignment is per-application only
B) Role assignment applies across all Azure resources and Entra ID
C) Scopes depend on the role type (directory-wide or delegated)    [GREEN BACKGROUND, WHITE TEXT]
D) Role assignment is per-user device only

─────────────────────────────────
✓ Answer: Built-in roles have directory-wide scope. Custom roles can have resource-specific scopes using administrative units.
[GREEN BOX WITH WHITE TEXT]
```

---

### 📝 **Explainer Format (Critical)**

The **Answer field** contains the explanation that appears in the green box on the back of the card.

**Explainer Requirements:**

- **Length:** Exactly 2 sentences (150 characters max)
- **Content:** Brief reasoning explaining why the correct answer is right
- **Style:** Plain text only (no HTML, no bold, no special formatting)
- **Location:** Displays in green box below the `<hr>` separator
- **Text Color:** WHITE (automatically rendered on #4CAF50 green background)

**Example Explainer:**

```
Built-in roles have directory-wide scope. Custom roles can have
resource-specific scopes using administrative units.
```

**What NOT to do:**

- ❌ Don't include "C) " prefix or choice letter
- ❌ Don't use HTML tags (`<strong>`, `<br>`, etc.)
- ❌ Don't exceed 150 characters
- ❌ Don't write more than 2 sentences
- ❌ Don't make text same color as background (already white on green)

---

### 📝 **Content Guidelines**

- **Explanations:** Max 150 characters, 2 sentences (see Explainer Format above)
- **Answer Format:** "Correct: [LETTER] - [explanation]"
- **Tags:** No spaces; use hyphens (e.g., "Entra-ID", not "Entra ID")
- **Choices:** Clear, distinct options with one clearly correct answer
- **Question Clarity:** No ambiguity; all wording must reference Microsoft Learn standards

---

### 🎯 **Deck Hierarchy**

All decks are organized under the main parent deck:

```
AZ-104 Study Guide
├── Deep Dive Segments
│   └── [Deep Dive cards]
├── Golden Rules Segments
│   └── [Golden Rule cards]
├── Performance Review Segments
│   ├── [Performance Review cards]
│   └── Entra ID Tutorials Dojo ← NEW DECK LOCATION
└── Study Guide Segments
    └── [General study cards]
```

The **Entra ID Tutorials Dojo** deck is placed under **Performance Review Segments** following the standard hierarchy.
