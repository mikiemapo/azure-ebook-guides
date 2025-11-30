# ✅ Pipeline Execution Checklist

## Pre-Execution Validation

- [ ] Review `audio_list_consolidated.txt` (159 unique transcripts)
- [ ] Verify `converted_transcripts.csv` format (sample from test run)
- [ ] Check `AZ-104-Master-Questions.csv` is readable
- [ ] Backup original master CSV
- [ ] Backup original `.apkg` file

## Execution Steps

### Step 1: Full Transcript Conversion

```bash
cd "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK"
python3 transcript_to_qa_converter.py
```

**Expected Output:**

- [ ] Creates `converted_transcripts.csv` with ~318 questions
- [ ] Generates `reports/conversion_report_*.txt`
- [ ] Console shows "✅ CONVERSION COMPLETE"
- [ ] Question count breakdown by category

### Step 2: Validate Converted Output

```bash
# Check line count (should be ~319: 1 header + 318 data)
wc -l AZ-104-Study-Deck/converted_transcripts.csv

# Review sample questions
head -20 AZ-104-Study-Deck/converted_transcripts.csv

# Check categories represented
grep "Transcript Conversion" AZ-104-Study-Deck/converted_transcripts.csv | cut -d':' -f2 | sort | uniq -c
```

**Expected Results:**

- [ ] ~319 total lines
- [ ] Questions from all 8 categories
- [ ] Proper CSV format (Batch, Question, Answer)

### Step 3: Merge and Regenerate Deck

```bash
python3 merge_and_regenerate.py --force
```

**Expected Output:**

- [ ] "✅ Merged: 520 + ~318 = ~838 total cards"
- [ ] Deck regeneration completes successfully
- [ ] `reports/merge_report_*.txt` created
- [ ] Final deck size: ~838 cards

### Step 4: Verify Final Deck

```bash
# Check master CSV was updated
wc -l AZ-104-Study-Deck/AZ-104-Master-Questions.csv

# Verify .apkg exists and is recent
ls -lh AZ-104-Study-Deck/AZ-104-Master-Study-Deck.apkg

# Count total cards in master
python3 -c "import csv; print(f'Total cards: {len(list(csv.DictReader(open(\"AZ-104-Study-Deck/AZ-104-Master-Questions.csv\"))))}')"
```

**Expected Results:**

- [ ] Master CSV has ~839 lines (1 header + 838 data)
- [ ] `.apkg` file timestamp is recent (today)
- [ ] Total cards: 838 (approximately)

## Anki Import (Final Step)

### Step 5: Import into Anki

1. [ ] Open Anki desktop application
2. [ ] Select File → Import
3. [ ] Navigate to: `AZ-104-Study-Deck/AZ-104-Master-Study-Deck.apkg`
4. [ ] Click "Open"
5. [ ] Review import summary (should show ~318 new cards)
6. [ ] Click "Import"

### Step 6: Verify in Anki

1. [ ] Check "AZ-104-Master-Study-Deck" deck exists
2. [ ] Expand deck tree - should show:
   - [ ] Golden Rules Segments (112 cards)
   - [ ] Deep Dive Segments (150 cards)
   - [ ] Study Guide Segments (258 cards)
   - [ ] Transcript Conversion (318 cards) ← NEW
3. [ ] Total cards should be ~838
4. [ ] Sample a few Transcript Conversion cards
5. [ ] Verify questions are answerable and relevant

## Post-Integration Tasks

### Documentation Updates

- [ ] Update `STUDY_CALENDAR_8WEEK.md` with Transcript Conversion segment
  - Add 2-3 weeks for new 318 cards
  - Suggest order: Storage, Networking, Compute
  - Update total study hours
- [ ] Update `README.md` in Study-Deck folder
  - Document 4 segments (add Transcript Conversion)
  - Update card count: 520 → 838
  - Note expansion %: +61%

### Calendar Regeneration

- [ ] Run `create_master_deck.py` to verify ICS calendar if needed
- [ ] Update `AZ104_Study_Schedule.ics` if you added weeks to calendar

### Daily Tracking

- [ ] Set up daily noon tracking (optional)
  ```bash
  # Add to crontab
  0 12 * * * cd /path/EBOOK && python3 transcript_deck_tracker.py >> reports/daily_log.txt
  ```

## Troubleshooting Guide

### If Conversion Fails

1. Check consolidation completed: `ls -l audio_list_consolidated.txt`
2. Verify consolidated list has content: `wc -l audio_list_consolidated.txt` (should be ~159)
3. Re-run: `python3 transcript_to_qa_converter.py 5` (test with 5)

### If Merge Fails

1. Check master CSV exists: `ls AZ-104-Study-Deck/AZ-104-Master-Questions.csv`
2. Verify it's readable: `head AZ-104-Study-Deck/AZ-104-Master-Questions.csv`
3. Check converted CSV: `wc -l AZ-104-Study-Deck/converted_transcripts.csv`
4. Re-run: `python3 merge_and_regenerate.py --force`

### If Deck Regeneration Fails

1. Check script exists: `ls AZ-104-Study-Deck/create_master_deck.py`
2. Verify Python 3: `python3 --version` (should be 3.8+)
3. Check CSV format: `head -5 AZ-104-Study-Deck/AZ-104-Master-Questions.csv`

### If Anki Import Fails

1. Ensure file path is correct
2. Check file permissions: `ls -l AZ-104-Study-Deck/AZ-104-Master-Study-Deck.apkg`
3. Try importing older backup first to verify Anki is working
4. Close and reopen Anki if needed

## Rollback Procedure (If Issues)

If you encounter problems after import:

1. **Restore Original Deck**

   ```bash
   # Keep backup of merged version
   cp AZ-104-Study-Deck/AZ-104-Master-Study-Deck.apkg \
      AZ-104-Study-Deck/AZ-104-Master-Study-Deck.apkg.backup

   # Restore from previous backup if you have one
   # Or manually delete the Anki deck and re-import original .apkg
   ```

2. **Restore CSV**

   ```bash
   # Keep backup of merged CSV
   cp AZ-104-Study-Deck/AZ-104-Master-Questions.csv \
      AZ-104-Study-Deck/AZ-104-Master-Questions.csv.backup

   # Restore from git if possible
   git checkout AZ-104-Study-Deck/AZ-104-Master-Questions.csv
   ```

## Success Criteria

✅ **Pipeline Execution Successful When:**

- Conversion generates ~318 questions from 159 transcripts
- Merge completes without errors
- Final deck shows ~838 total cards
- Anki imports successfully
- Transcript Conversion segment appears with all 4 subcategories
- Sample questions are reasonable and answerable

---

## Timeline Estimate

| Phase                  | Time        | Status   |
| ---------------------- | ----------- | -------- |
| Consolidation          | 1 min       | ✅ Done  |
| Conversion (10 sample) | 30 sec      | ✅ Done  |
| Conversion (full 159)  | 2-3 min     | ⏳ Ready |
| Merge & Regenerate     | 2-3 min     | ⏳ Ready |
| Anki Import            | 1-2 min     | ⏳ Ready |
| **Total**              | **~10 min** | ⏳ Ready |

---

**Last Updated:** Nov 27, 2025
**Pipeline Status:** ✅ READY FOR EXECUTION
