#!/usr/bin/env python3
"""
Periodic checker: Find new text files in cloud folder that don't have CSVs yet.
Helps identify which deep-dive decks still need to be created.

Usage: python3 check_new_deep_dive_files.py
"""

import os
import sys
from pathlib import Path

# Paths
CLOUD_TEXT_FOLDER = "/Users/mike1macbook/Library/Mobile Documents/3L68KQB4HG~com~readdle~CommonDocuments/Documents/azure-ebook-guides/Conversations not hub/Text files"
WORKSPACE_TEXT_FOLDER = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Conversations/AZ-104 CONVERSATIONS"
CSV_FOLDER = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/AZ-104-Critical-Priorities-Study-Deck/Topic-Based-Decks"

def get_text_files(folder):
    """Get all .txt files from folder"""
    if not os.path.exists(folder):
        return []
    return sorted([f for f in os.listdir(folder) if f.endswith('.txt') and os.path.getsize(os.path.join(folder, f)) > 1000])

def get_csv_decks():
    """Get all CSV deck names"""
    if not os.path.exists(CSV_FOLDER):
        return {}
    
    decks = {}
    for f in os.listdir(CSV_FOLDER):
        if f.endswith('.csv'):
            # Extract deck name (remove .csv, AZ104_ prefix)
            name = f.replace('.csv', '').replace('AZ104_', '')
            decks[name] = f
    return decks

def normalize_name(text):
    """Normalize text file name for matching"""
    return text.lower().replace('_', ' ').replace('-', ' ').replace('(transcribed)', '').strip()

def find_matching_csv(text_file, csv_names):
    """Find potential CSV match for text file"""
    normalized = normalize_name(text_file)
    normalized_words = set(normalized.split())
    
    for csv_name in csv_names.keys():
        csv_normalized = normalize_name(csv_name)
        csv_words = set(csv_normalized.split())
        
        # Calculate word overlap (Jaccard similarity)
        if len(csv_words & normalized_words) >= 2:  # At least 2 matching words
            return csv_name
    
    return None

def main():
    print("=" * 80)
    print("DEEP-DIVE TEXT FILE CHECKER")
    print("=" * 80)
    
    # Get files
    cloud_files = get_text_files(CLOUD_TEXT_FOLDER)
    workspace_files = get_text_files(WORKSPACE_TEXT_FOLDER)
    csv_decks = get_csv_decks()
    
    all_text_files = sorted(set(cloud_files + workspace_files))
    
    print(f"\n📁 Cloud folder: {len(cloud_files)} files")
    print(f"📁 Workspace folder: {len(workspace_files)} files")
    print(f"📊 CSV decks found: {len(csv_decks)}")
    print(f"\n📋 Total text files to check: {len(all_text_files)}")
    
    # Filter out non-transcript files
    skip_files = {'audio_list.txt', 'cards_replacement.txt', 'temp_data.txt'}
    text_files = [f for f in all_text_files if f not in skip_files]
    
    print("\n" + "=" * 80)
    print("TEXT FILE STATUS CHECK")
    print("=" * 80)
    
    done = []
    checking = []
    new = []
    skipped = []
    
    for text_file in text_files:
        # Get file size
        for folder in [WORKSPACE_TEXT_FOLDER, CLOUD_TEXT_FOLDER]:
            path = os.path.join(folder, text_file)
            if os.path.exists(path):
                size_kb = os.path.getsize(path) / 1024
                break
        
        # Check for CSV match
        match = find_matching_csv(text_file, csv_decks)
        
        if text_file in skip_files:
            skipped.append((text_file, size_kb))
        elif match:
            # Has CSV - need to check if content is duplicate or new
            checking.append((text_file, size_kb, match))
        else:
            # No CSV found - brand new
            new.append((text_file, size_kb))
    
    # Print done (VABRF only)
    if done:
        print("\n✅ DONE (Content Extracted)")
        print("-" * 80)
        for text_file, size_kb in done:
            print(f"  {text_file:<65} ({size_kb:>5.1f} KB)")
    
    # Print checking
    if checking:
        print("\n⏳ CHECKING (Need Comparison with Existing CSV)")
        print("-" * 80)
        for text_file, size_kb, csv_match in checking:
            csv_name = csv_decks.get(csv_match, csv_match)
            print(f"  {text_file:<40} → {csv_name:<40}")
            print(f"    {size_kb:>5.1f} KB")
    
    # Print new
    if new:
        print("\n🆕 NEW (No Existing CSV Found - Need New Decks)")
        print("-" * 80)
        for text_file, size_kb in new:
            print(f"  {text_file:<65} ({size_kb:>5.1f} KB)")
    
    # Print skipped
    if skipped:
        print("\n🚫 SKIPPED (Not Deep-Dive Transcripts)")
        print("-" * 80)
        for text_file, size_kb in skipped:
            print(f"  {text_file:<65} ({size_kb:>5.1f} KB)")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Done:        {len(done)} decks (fully extracted)")
    print(f"⏳ Checking:    {len(checking)} text files (need comparison)")
    print(f"🆕 New:         {len(new)} text files (need extraction)")
    print(f"🚫 Skipped:     {len(skipped)} files (not transcripts)")
    print(f"\nCompletion: {len(done)}/{len(text_files)} = {100*len(done)//max(1,len(text_files))}%")
    
    # Action items
    print("\n" + "=" * 80)
    print("ACTION ITEMS")
    print("=" * 80)
    
    if checking:
        print(f"\n1. COMPARE {len(checking)} text files with existing CSVs:")
        for _, _, csv_match in checking:
            print(f"   - {csv_match}")
        print("   → If content matches existing CSV: mark as SKIP (duplicate)")
        print("   → If content is new: extract 20 CPRS questions to CSV")
    
    if new:
        print(f"\n2. CREATE {len(new)} new deep-dive decks:")
        for text_file, _ in new:
            deck_name = text_file.replace(' (Transcribed)', '').replace('.txt', '')
            deck_name = deck_name.replace('_', ' ').replace('-', ' ')
            print(f"   - AZ104_{deck_name}_DeepDive.csv")
        print("   → Extract 20 CPRS questions per text file")
    
    if checking or new:
        print(f"\n3. COMMIT to git:")
        print("   git add AZ-104-Critical-Priorities-Study-Deck/Topic-Based-Decks/*.csv")
        print("   git commit -m 'docs: add new deep-dive decks from transcripts'")
        print("   git push origin feature/cli-az104-focus")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()
