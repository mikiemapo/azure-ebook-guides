#!/usr/bin/env python3
"""
AZ-104 Transcript to Deck Tracking System
Tracks which transcripts have been converted to Anki questions
Runs at noon daily to generate a compliance report
"""

import os
import csv
from datetime import datetime
from collections import defaultdict
import re

# Paths
AUDIO_LIST = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/audio_list.txt"
MASTER_CSV = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/AZ-104-Study-Deck/AZ-104-Master-Questions.csv"
DEEP_DIVE_DIR = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/AZ-104-Critical-Priorities-Study-Deck/"
REPORT_DIR = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/reports/"

# Ensure report directory exists
os.makedirs(REPORT_DIR, exist_ok=True)

def extract_az104_transcripts():
    """Extract only AZ-104 related transcripts from audio_list.txt"""
    transcripts = []
    try:
        with open(AUDIO_LIST, 'r') as f:
            for line in f:
                line = line.strip()
                if 'AZ-104' in line or 'Azure' in line.split('/')[-1]:
                    if line.startswith('./'):
                        transcripts.append(line[2:])  # Remove ./
    except FileNotFoundError:
        print(f"❌ audio_list.txt not found at {AUDIO_LIST}")
        return []
    return transcripts

def get_deck_batches():
    """Extract all batch names from master CSV"""
    batches = defaultdict(int)
    try:
        with open(MASTER_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                batch = row.get('Batch', '').strip()
                if batch:
                    batches[batch] += 1
    except FileNotFoundError:
        print(f"❌ Master CSV not found at {MASTER_CSV}")
        return {}
    return batches

def find_deep_dive_csvs():
    """Find all deep dive CSV files"""
    deep_dives = {}
    try:
        for file in os.listdir(DEEP_DIVE_DIR):
            if file.endswith('.csv') and file != 'AZ-104-Master-Questions.csv':
                path = os.path.join(DEEP_DIVE_DIR, file)
                with open(path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    count = sum(1 for _ in reader)
                    deep_dives[file] = count
    except FileNotFoundError:
        pass
    return deep_dives

def categorize_transcripts(transcripts):
    """Categorize transcripts by topic"""
    categories = defaultdict(list)
    
    topics = {
        'App Service': ['App Service', 'App_Service', 'application', 'PaaS'],
        'Storage': ['Storage', 'Blob', 'Files', 'RBAC', 'Access', 'SAS'],
        'Networking': ['Network', 'VNet', 'NSG', 'DNS', 'Load Balanc', 'Firewall', 'Gateway', 'VPN'],
        'Compute': ['VM', 'VMSS', 'Compute', 'Scale Set', 'ACI', 'Container'],
        'Backup/DR': ['Backup', 'Recovery', 'Resilience', 'VABRF', 'Disaster'],
        'Identity': ['RBAC', 'Entra', 'Access', 'IAM', 'Authorization'],
        'Monitoring': ['Monitor', 'Alert', 'Logs'],
        'Governance': ['Governance', 'Compliance', 'Policy'],
        'Other': []
    }
    
    for transcript in transcripts:
        categorized = False
        for category, keywords in topics.items():
            if category != 'Other':
                for keyword in keywords:
                    if keyword.lower() in transcript.lower():
                        categories[category].append(transcript)
                        categorized = True
                        break
        if not categorized:
            categories['Other'].append(transcript)
    
    return categories

def find_duplicates(transcripts):
    """Find potentially duplicate transcripts"""
    duplicates = defaultdict(list)
    
    for transcript in transcripts:
        # Extract core name (remove version numbers, extensions, etc.)
        core_name = re.sub(r'[\s_-]+([\d\w]+)?\..*$', '', transcript)
        core_name = re.sub(r'\s*\(\d+\)\s*', '', core_name)  # Remove (1), (2), etc.
        duplicates[core_name].append(transcript)
    
    # Filter to only actual duplicates
    return {k: v for k, v in duplicates.items() if len(v) > 1}

def generate_report(transcripts, batches, deep_dives):
    """Generate comprehensive tracking report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_name = f"transcript_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path = os.path.join(REPORT_DIR, report_name)
    
    categories = categorize_transcripts(transcripts)
    duplicates = find_duplicates(transcripts)
    
    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write(f"AZ-104 TRANSCRIPT TO DECK TRACKING REPORT\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary
        f.write("📊 SUMMARY\n")
        f.write(f"Total AZ-104 Transcripts: {len(transcripts)}\n")
        f.write(f"Total Deck Cards: {sum(batches.values())}\n")
        f.write(f"Total Batches: {len(batches)}\n")
        f.write(f"Potential Duplicates: {sum(len(v) for v in duplicates.values())}\n")
        f.write(f"Deep Dive CSVs Found: {len(deep_dives)}\n\n")
        
        # Current deck structure
        f.write("📚 CURRENT DECK STRUCTURE (520 Cards)\n")
        f.write("-" * 80 + "\n")
        f.write("🏆 Golden Rules Segments: 112 cards\n")
        f.write("   - Golden Rule Part 1 & 2: 56 cards\n")
        f.write("   - Golden Rule Enriched Part 1 & 2 FULL: 41 cards\n")
        f.write("   - Tutorial Dojo VM Restore: 15 cards\n\n")
        
        f.write("🔬 Deep Dive Segments: 150 cards\n")
        for batch, count in sorted(batches.items()):
            if 'Deep Dive' in batch or 'Mastery' in batch:
                f.write(f"   - {batch}: {count} cards\n")
        f.write("\n")
        
        f.write("📚 Study Guide Segments: 258 cards\n")
        for batch, count in sorted(batches.items()):
            if 'Study Guide' in batch or 'Deep Dive' not in batch and 'Golden' not in batch:
                f.write(f"   - {batch}: {count} cards\n")
        f.write("\n\n")
        
        # Transcripts by category
        f.write("🎯 TRANSCRIPTS BY CATEGORY\n")
        f.write("-" * 80 + "\n")
        for category in sorted(categories.keys()):
            count = len(categories[category])
            f.write(f"\n{category}: {count} transcripts\n")
            for transcript in sorted(categories[category])[:5]:  # Show first 5
                f.write(f"  - {transcript}\n")
            if count > 5:
                f.write(f"  ... and {count - 5} more\n")
        
        # Potential duplicates
        if duplicates:
            f.write("\n\n⚠️  POTENTIAL DUPLICATES TO REVIEW\n")
            f.write("-" * 80 + "\n")
            for core_name, transcripts_list in sorted(duplicates.items()):
                f.write(f"\n{core_name}:\n")
                for t in transcripts_list:
                    f.write(f"  - {t}\n")
        else:
            f.write("\n\n✅ NO DUPLICATES DETECTED\n")
        
        # Deep dive CSVs
        f.write("\n\n📁 DEEP DIVE CSV FILES\n")
        f.write("-" * 80 + "\n")
        for csv_file, count in sorted(deep_dives.items()):
            f.write(f"{csv_file}: {count} cards\n")
        
        # Recommendations
        f.write("\n\n💡 RECOMMENDATIONS\n")
        f.write("-" * 80 + "\n")
        f.write("1. Review potential duplicates above for redundancy\n")
        f.write("2. Identify which uncategorized transcripts need processing\n")
        f.write("3. Verify all deep dive CSVs are merged into master\n")
        f.write("4. Next: Generate new decks from unprocessed transcripts\n")
    
    return report_path

def main():
    print(f"\n🔄 Running AZ-104 Transcript Tracker ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
    
    # Extract data
    transcripts = extract_az104_transcripts()
    batches = get_deck_batches()
    deep_dives = find_deep_dive_csvs()
    
    if not transcripts:
        print("❌ No transcripts found!")
        return
    
    print(f"✅ Found {len(transcripts)} AZ-104 transcripts")
    print(f"✅ Found {len(batches)} deck batches ({sum(batches.values())} total cards)")
    print(f"✅ Found {len(deep_dives)} deep dive CSV files")
    
    # Generate report
    report_path = generate_report(transcripts, batches, deep_dives)
    print(f"\n📊 Report generated: {report_path}\n")
    
    # Print summary to console
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Transcripts: {len(transcripts)}")
    print(f"Total Deck Cards: {sum(batches.values())}")
    print(f"Deck Segments: 3 (Golden Rules, Deep Dive, Study Guide)")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
