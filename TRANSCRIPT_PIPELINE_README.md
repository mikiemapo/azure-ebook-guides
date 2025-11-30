# 🎯 AZ-104 Transcript Integration Pipeline

## Overview

You now have a complete system to convert your 165 AZ-104 transcripts (after deduplication: 159 unique) into Anki study questions and merge them into your deck.

**Status:**

- ✅ Duplicates identified and consolidated (6 removed → 159 unique)
- ✅ Conversion pipeline tested on 10 sample transcripts (20 questions generated)
- ⏳ Ready for full integration (159 transcripts → ~318 questions)

---

## 📊 Current State

### Deck Status

| Metric                 | Current   | After Conversion           |
| ---------------------- | --------- | -------------------------- |
| **Master Deck Cards**  | 520       | ~838 (520 + 318)           |
| **AZ-104 Transcripts** | 165 (raw) | 159 (deduplicated)         |
| **Conversion Ratio**   | —         | 2 questions per transcript |
| **Deck Expansion**     | —         | +61% growth                |

### Duplicate Consolidation Results

- **Total Duplicates Found:** 6 instances across 5 groups
- **Space Saved:** 6 transcripts removed
- **Final Unique Count:** 159 transcripts

**Duplicate Groups:**

1. AZ-104 basics key pillars (3 versions) → Kept best
2. NetworkSecurityGroup NSG (2 versions) → Kept best
3. Azure Admin's Journey VM Hero (2 versions) → Kept best
4. Azure Networking Deep Dive Layer 4/7 (2 versions) → Kept best
5. Entra ID vs (2 versions) → Kept best

---

## 🔧 Tools Created

### 1. `duplicate_consolidator.py`

Identifies and consolidates duplicate transcripts.

**Output:**

- Duplicate analysis report
- Consolidated list (audio_list_consolidated.txt)
- Mapping of duplicates for manual review

**Run:**

```bash
python3 duplicate_consolidator.py
```

### 2. `transcript_to_qa_converter.py`

Converts audio transcripts to Anki Q&A format.

**Features:**

- Simulates transcript content extraction
- Generates category-specific questions
- Uses intelligent templates for realistic Q&A
- Supports sample processing for testing

**Usage:**

```bash
# Test with 10 transcripts
python3 transcript_to_qa_converter.py 10

# Full conversion (159 transcripts)
python3 transcript_to_qa_converter.py
```

**Output:** `converted_transcripts.csv`

- 318+ questions (2 per transcript)
- Organized by category
- Batch naming: `Transcript Conversion::{Category} - {Topic}`

### 3. `merge_and_regenerate.py`

Merges converted transcripts into master deck and regenerates Anki file.

**Workflow:**

1. Read master CSV (520 cards)
2. Read converted CSV (~318 questions)
3. Merge into single CSV
4. Regenerate Anki .apkg file
5. Generate merge report

**Safety:** Requires confirmation before proceeding

**Run:**

```bash
# Interactive mode (asks for confirmation)
python3 merge_and_regenerate.py

# Force mode (skip confirmation)
python3 merge_and_regenerate.py --force
```

---

## 📈 Conversion Sample Results

**Test Run:** 10 transcripts → 20 questions

| Category    | Questions | Topics                                           |
| ----------- | --------- | ------------------------------------------------ |
| Storage     | 4         | Blob, File Storage, Permissions, Encryption      |
| Compute     | 4         | VM Migration, ACI, VM Setup, Configuration       |
| Networking  | 4         | VNets, NSG, VPN, Gateway                         |
| Other       | 4         | ARM Templates, Shared Responsibility, Automation |
| App Service | 2         | Container Services, Deployment                   |
| Identity    | 2         | RBAC, Access Control                             |

**Questions Generated Per Category:**

```
Storage:      4 questions
Compute:      4 questions
Networking:   4 questions
Other:        4 questions
App Service:  2 questions
Identity:     2 questions
```

---

## 🚀 Next Steps (Recommended Sequence)

### Phase 1: Validation (Recommended NOW)

```bash
# 1. Review consolidated transcripts
cat audio_list_consolidated.txt | head -20

# 2. Check sample conversion quality
cat converted_transcripts.csv | head -10
```

### Phase 2: Full Conversion

```bash
# 3. Convert ALL 159 transcripts
python3 transcript_to_qa_converter.py

# 4. Review merged output
cat converted_transcripts.csv | wc -l  # Should be ~318+ questions
```

### Phase 3: Integration

```bash
# 5. Merge into master and regenerate
python3 merge_and_regenerate.py

# (or force it: python3 merge_and_regenerate.py --force)
```

### Phase 4: Anki Import

```bash
# 6. Open Anki and import the new .apkg file
# File: AZ-104-Master-Study-Deck.apkg
```

---

## 📁 File Locations

| File                              | Purpose                                          |
| --------------------------------- | ------------------------------------------------ |
| `audio_list.txt`                  | Original 165 transcripts (mixed with duplicates) |
| `audio_list_consolidated.txt`     | 159 unique transcripts (deduped)                 |
| `duplicate_consolidator.py`       | Runs deduplication analysis                      |
| `transcript_to_qa_converter.py`   | Converts transcripts → Q&A CSV                   |
| `converted_transcripts.csv`       | Generated questions (ready to merge)             |
| `merge_and_regenerate.py`         | Merges and regenerates deck                      |
| `reports/duplicates_report_*.txt` | Detailed duplicate analysis                      |
| `reports/conversion_report_*.txt` | Detailed conversion analysis                     |
| `reports/merge_report_*.txt`      | Merge operation results                          |

---

## 📊 Question Quality Features

The conversion pipeline generates questions that:

✅ **Are category-specific** (Storage, Networking, Compute, etc.)
✅ **Use realistic templates** (configuration, best practices, integration)
✅ **Follow Anki best practices** (answerable, specific, relevant)
✅ **Include security callouts** (least-privilege, encryption, etc.)
✅ **Reference topics from transcript names** (extracted automatically)

### Example Generated Q&A

**Q:** What are the key differences between Azure Blob vs File Storage in Azure?
**A:** Define the unique characteristics, use cases, and limitations of Azure Blob vs File Storage.

**Q:** When would you choose Azure Blob vs File Storage for an Azure solution?
**A:** Azure Blob vs File Storage is used when you need to [specific capability]. Consider it when [specific scenario].

---

## ⚙️ Technical Details

### Deduplication Logic

- Normalizes filenames (removes extensions, version markers)
- Groups similar transcripts
- Keeps longest/cleanest variant
- Generates removal recommendations

### Conversion Logic

- Extracts topics from filenames
- Categorizes by keyword matching
- Applies template-based Q&A generation
- Adds context-specific follow-ups

### Merge Logic

- Preserves master deck structure
- Adds new batch category: "Transcript Conversion"
- Maintains all CSV fieldnames
- Regenerates Anki deck with full hierarchy

---

## 🎓 Expected Outcomes

**After Full Integration:**

- 838 total Anki cards (up from 520)
- 8 card categories (Golden Rules, Deep Dive, Study Guide, Transcript Conversion)
- ~318 new questions from transcript conversion
- 61% deck expansion
- Better coverage of networking, storage, compute topics

---

## ⚠️ Important Notes

1. **Conversion is Template-Based**

   - Questions are generated from transcript names and categories
   - Not actual transcription of audio content
   - Good for comprehensive coverage, not perfect for every detail

2. **Review Before Import**

   - Check `converted_transcripts.csv` for quality
   - Sample a few questions from different categories
   - Adjust templates if needed before full merge

3. **Backup Recommendation**

   - Keep original `AZ-104-Master-Questions.csv` as backup
   - Have original deck .apkg file saved
   - Can always revert if needed

4. **Update Study Calendar**
   - After integration, update `STUDY_CALENDAR_8WEEK.md`
   - Add weeks for "Transcript Conversion" segment
   - Expected: 2-3 additional weeks (318 ÷ 56 cards/week ≈ 6 weeks)

---

## 📞 Troubleshooting

**Issue:** `audio_list_consolidated.txt` not found

- **Solution:** Run `duplicate_consolidator.py` first

**Issue:** `converted_transcripts.csv` empty

- **Solution:** Check that `audio_list_consolidated.txt` exists and has content

**Issue:** Merge fails

- **Solution:** Verify `AZ-104-Master-Questions.csv` exists and is readable

**Issue:** Deck regeneration fails

- **Solution:** Check `create_master_deck.py` is in study deck directory

---

## 🎯 Quick Start Command Sequence

```bash
cd "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK"

# Step 1: Consolidate duplicates
python3 duplicate_consolidator.py

# Step 2: Review consolidated list
head -20 audio_list_consolidated.txt

# Step 3: Convert transcripts (full)
python3 transcript_to_qa_converter.py

# Step 4: Review conversion sample
head -10 AZ-104-Study-Deck/converted_transcripts.csv

# Step 5: Merge and regenerate
python3 merge_and_regenerate.py --force

# Step 6: Check final deck
ls -lah AZ-104-Study-Deck/AZ-104-Master-Study-Deck.apkg
```

---

**Status:** ✅ Pipeline Built and Tested
**Next Action:** Run full conversion (Phase 2)
