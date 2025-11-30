#!/usr/bin/env python3
"""
Merge converted transcripts into master CSV and regenerate Anki deck.
"""

import os
import csv
import subprocess
from datetime import datetime

EBOOK_DIR = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK"
MASTER_CSV = os.path.join(EBOOK_DIR, "AZ-104-Study-Deck/AZ-104-Master-Questions.csv")
CONVERTED_CSV = os.path.join(EBOOK_DIR, "AZ-104-Study-Deck/converted_transcripts.csv")
CREATE_DECK_SCRIPT = os.path.join(EBOOK_DIR, "AZ-104-Study-Deck/create_master_deck.py")
REPORTS_DIR = os.path.join(EBOOK_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

def merge_csvs():
    """Merge converted transcripts into master CSV."""
    print(f"\n📋 Merging Converted Transcripts into Master Deck")
    print(f"{'='*80}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Read master CSV
    print("📖 Reading master CSV...")
    master_rows = []
    master_fieldnames = None
    
    try:
        with open(MASTER_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            master_fieldnames = reader.fieldnames
            for row in reader:
                master_rows.append(row)
        print(f"✅ Master CSV: {len(master_rows)} cards\n")
    except Exception as e:
        print(f"❌ Error reading master CSV: {e}")
        return False
    
    # Read converted CSV
    print("📖 Reading converted transcripts CSV...")
    converted_rows = []
    
    try:
        with open(CONVERTED_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                converted_rows.append(row)
        print(f"✅ Converted CSV: {len(converted_rows)} questions\n")
    except Exception as e:
        print(f"❌ Error reading converted CSV: {e}")
        return False
    
    # Merge
    print("🔄 Merging...")
    
    # Ensure all fieldnames are present in converted rows
    if master_fieldnames:
        for row in converted_rows:
            for field in master_fieldnames:
                if field not in row:
                    row[field] = ''
    
    merged_rows = master_rows + converted_rows
    print(f"✅ Merged: {len(master_rows)} + {len(converted_rows)} = {len(merged_rows)} total cards\n")
    
    # Write merged CSV
    print("💾 Writing merged CSV...")
    try:
        with open(MASTER_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=master_fieldnames)
            writer.writeheader()
            for row in merged_rows:
                writer.writerow(row)
        print(f"✅ Updated: {MASTER_CSV}\n")
    except Exception as e:
        print(f"❌ Error writing merged CSV: {e}")
        return False
    
    # Generate report
    report_path = os.path.join(REPORTS_DIR, f"merge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("TRANSCRIPT MERGE REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        f.write("📊 SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Original Master Deck: {len(master_rows)} cards\n")
        f.write(f"Converted Transcripts: {len(converted_rows)} questions\n")
        f.write(f"New Total: {len(merged_rows)} cards\n")
        f.write(f"Increase: {len(converted_rows)} cards ({100*len(converted_rows)/len(master_rows):.1f}% expansion)\n\n")
        
        f.write("📋 BATCH CATEGORIES\n")
        f.write("-"*80 + "\n")
        
        # Count by batch
        batch_counts = {}
        for row in converted_rows:
            batch = row.get('Batch', 'Unknown').split('::')[0]
            batch_counts[batch] = batch_counts.get(batch, 0) + 1
        
        for batch in sorted(batch_counts.keys()):
            f.write(f"{batch}: {batch_counts[batch]} questions\n")
    
    print(f"📄 Report saved: {report_path}\n")
    
    return True

def regenerate_deck():
    """Regenerate Anki deck."""
    print("🃏 Regenerating Anki Deck...")
    print(f"{'='*80}\n")
    
    if not os.path.exists(CREATE_DECK_SCRIPT):
        print(f"❌ Create deck script not found: {CREATE_DECK_SCRIPT}")
        return False
    
    try:
        # Change to study deck directory
        original_cwd = os.getcwd()
        os.chdir(os.path.dirname(CREATE_DECK_SCRIPT))
        
        # Run script
        result = subprocess.run(['python3', CREATE_DECK_SCRIPT], 
                              capture_output=True, text=True, timeout=60)
        
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print("✅ Deck regenerated successfully!")
            print(f"Output: {result.stdout}\n")
            return True
        else:
            print(f"❌ Error regenerating deck:")
            print(f"Error: {result.stderr}\n")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Deck generation timed out (>60 seconds)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

def main():
    """Main merge and regenerate workflow."""
    print(f"\n{'='*80}")
    print(f"TRANSCRIPT INTEGRATION PIPELINE")
    print(f"{'='*80}\n")
    
    # Step 1: Merge
    if not merge_csvs():
        print("❌ Merge failed. Stopping.\n")
        return False
    
    # Step 2: Regenerate
    if not regenerate_deck():
        print("⚠️  Deck regeneration had issues. Check output above.\n")
        return False
    
    # Summary
    print(f"\n{'='*80}")
    print(f"✅ INTEGRATION COMPLETE")
    print(f"{'='*80}")
    
    # Count final cards
    try:
        with open(MASTER_CSV, 'r', encoding='utf-8') as f:
            final_count = len(list(csv.DictReader(f)))
        print(f"\n📊 Final Deck Size: {final_count} cards")
        print(f"📚 Ready to import into Anki\n")
    except:
        pass
    
    return True

if __name__ == '__main__':
    import sys
    
    if '--force' not in sys.argv:
        print("⚠️  This will merge converted transcripts into your master deck.")
        print("Make sure you've reviewed converted_transcripts.csv first!\n")
        response = input("Proceed with merge? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled.\n")
            sys.exit(0)
    
    success = main()
    sys.exit(0 if success else 1)
