#!/usr/bin/env python3
"""
Detailed duplication risk assessment before full conversion.
"""

import csv
import os
from collections import defaultdict

MASTER_CSV = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/AZ-104-Study-Deck/AZ-104-Master-Questions.csv"
CONSOLIDATED = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/audio_list_consolidated.txt"
REPORTS_DIR = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/reports"

os.makedirs(REPORTS_DIR, exist_ok=True)

def analyze_duplication_risk():
    """Analyze if conversion will create duplicates."""
    
    print(f"\n🔍 DETAILED DUPLICATION RISK ASSESSMENT")
    print(f"{'='*80}\n")
    
    # Load master CSV
    master_data = {
        'questions': [],
        'batches': set(),
        'by_batch': defaultdict(list),
        'keywords': defaultdict(set)
    }
    
    print("📖 Loading master CSV...")
    with open(MASTER_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = row.get('Question', '').strip()
            b = row.get('Batch', '').strip()
            master_data['questions'].append(q)
            master_data['batches'].add(b)
            master_data['by_batch'][b].append(q)
            
            # Extract keywords (4+ chars)
            words = [w.lower() for w in q.split() if len(w) > 3]
            for word in words:
                master_data['keywords'][word].add(q[:50])
    
    print(f"✅ Master has {len(master_data['questions'])} questions across {len(master_data['batches'])} batches\n")
    
    # Load consolidated transcripts
    print("📖 Loading consolidated transcripts...")
    transcripts = []
    with open(CONSOLIDATED, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and 'az-104' in line.lower():
                transcripts.append(line)
    
    print(f"✅ Found {len(transcripts)} transcripts to convert\n")
    
    # Analyze overlap
    print("🔎 Analyzing content overlap...\n")
    
    transcript_analysis = []
    for transcript in transcripts:
        # Extract clean name
        t_name = transcript.replace('./Conversations /AZ-104 CONVERSATIONS/', '')
        t_name = t_name.replace('.wav', '').replace('.mp4', '').replace('.m4a', '')
        
        # Extract keywords
        t_keywords = [w.lower() for w in t_name.split() if len(w) > 4]
        
        # Find matches in master
        matches = []
        for keyword in t_keywords:
            if keyword in master_data['keywords']:
                matches.append(keyword)
        
        overlap_pct = (len(set(matches)) / len(t_keywords) * 100) if t_keywords else 0
        
        transcript_analysis.append({
            'name': t_name,
            'keywords': len(t_keywords),
            'overlap_keywords': len(set(matches)),
            'overlap_pct': overlap_pct,
            'is_duplicate_risk': overlap_pct > 80
        })
    
    # Generate report
    report_path = os.path.join(REPORTS_DIR, "duplication_risk_assessment.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("DUPLICATION RISK ASSESSMENT\n")
        f.write("="*80 + "\n\n")
        
        # Summary
        high_risk = [t for t in transcript_analysis if t['is_duplicate_risk']]
        medium_risk = [t for t in transcript_analysis if 40 <= t['overlap_pct'] <= 80]
        low_risk = [t for t in transcript_analysis if t['overlap_pct'] < 40]
        
        f.write("📊 RISK SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Transcripts: {len(transcripts)}\n")
        f.write(f"High Risk (>80% overlap): {len(high_risk)} transcripts\n")
        f.write(f"Medium Risk (40-80% overlap): {len(medium_risk)} transcripts\n")
        f.write(f"Low Risk (<40% overlap): {len(low_risk)} transcripts\n\n")
        
        if high_risk:
            f.write("🔴 HIGH RISK TRANSCRIPTS (Likely already covered)\n")
            f.write("-"*80 + "\n")
            for t in sorted(high_risk, key=lambda x: x['overlap_pct'], reverse=True):
                f.write(f"• {t['name'][:60]}\n")
                f.write(f"  Overlap: {t['overlap_pct']:.0f}% ({t['overlap_keywords']}/{t['keywords']} keywords match)\n")
                f.write(f"  ACTION: Consider skipping or reviewing\n\n")
        
        f.write("\n✅ MEDIUM & LOW RISK TRANSCRIPTS (Safe to convert)\n")
        f.write("-"*80 + "\n")
        f.write(f"Medium Risk: {len(medium_risk)} (different angles, supplementary)\n")
        f.write(f"Low Risk: {len(low_risk)} (new topics, no overlap)\n\n")
        
        # Master deck structure
        f.write("\n📚 CURRENT MASTER DECK STRUCTURE\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Batches: {len(master_data['batches'])}\n")
        f.write(f"Total Questions: {len(master_data['questions'])}\n\n")
        
        # Parent categories
        parents = defaultdict(int)
        for batch in master_data['batches']:
            parent = batch.split('::')[0] if '::' in batch else batch
            parents[parent] += len(master_data['by_batch'][batch])
        
        for parent in sorted(parents.keys()):
            f.write(f"{parent}: {parents[parent]} questions\n")
        
        f.write("\n\n📈 PROJECTION AFTER CONVERSION\n")
        f.write("-"*80 + "\n")
        f.write(f"Current Master: {len(master_data['questions'])} questions\n")
        f.write(f"High Risk (skip): {len(high_risk)} transcripts × 2 = {len(high_risk)*2} questions saved\n")
        f.write(f"Medium + Low Risk (convert): {len(medium_risk)+len(low_risk)} transcripts × 2 = {(len(medium_risk)+len(low_risk))*2} questions\n")
        f.write(f"CONSERVATIVE ESTIMATE: {len(master_data['questions'])} + {(len(medium_risk)+len(low_risk))*2} = {len(master_data['questions']) + (len(medium_risk)+len(low_risk))*2} questions\n")
        f.write(f"OPTIMISTIC ESTIMATE: {len(master_data['questions'])} + {len(transcripts)*2} = {len(master_data['questions']) + len(transcripts)*2} questions\n\n")
        
        f.write("\n💡 RECOMMENDATION\n")
        f.write("-"*80 + "\n")
        if len(high_risk) > 0:
            f.write(f"⚠️  {len(high_risk)} transcripts show high overlap. Consider:\n")
            f.write(f"   1. Skip high-risk items to avoid duplicates\n")
            f.write(f"   2. OR convert all and manually review duplicates after merge\n")
            f.write(f"   3. Proceed with medium/low risk items ({len(medium_risk)+len(low_risk)} safe transcripts)\n\n")
        else:
            f.write(f"✅ LOW DUPLICATION RISK - All transcripts are supplementary\n")
            f.write(f"   Proceed with full conversion\n\n")
        
        f.write("🎯 FINAL VERDICT\n")
        f.write("-"*80 + "\n")
        if len(high_risk) > 0:
            f.write(f"Safe to convert: {len(medium_risk)+len(low_risk)}/{len(transcripts)} transcripts\n")
            f.write(f"Expected safe expansion: {(len(medium_risk)+len(low_risk))*2} new questions\n")
            f.write(f"Final deck estimate: {len(master_data['questions']) + (len(medium_risk)+len(low_risk))*2} cards (conservative)\n")
        else:
            f.write(f"All {len(transcripts)} transcripts are safe to convert\n")
            f.write(f"Expected expansion: {len(transcripts)*2} new questions\n")
            f.write(f"Final deck: {len(master_data['questions']) + len(transcripts)*2} cards (optimistic)\n")
    
    # Console output
    print(f"{'='*80}")
    print(f"📊 ASSESSMENT RESULTS")
    print(f"{'='*80}\n")
    
    print(f"High Risk: {len(high_risk)} ({100*len(high_risk)/len(transcripts):.1f}%)")
    print(f"Medium Risk: {len(medium_risk)} ({100*len(medium_risk)/len(transcripts):.1f}%)")
    print(f"Low Risk: {len(low_risk)} ({100*len(low_risk)/len(transcripts):.1f}%)\n")
    
    print(f"Master deck: {len(master_data['questions'])} questions")
    print(f"Safe to add: {(len(medium_risk)+len(low_risk))*2} questions (conservative)")
    print(f"Final deck: {len(master_data['questions']) + (len(medium_risk)+len(low_risk))*2} cards\n")
    
    if len(high_risk) > 0:
        print(f"⚠️  Recommendation: Review high-risk transcripts first")
        print(f"    Safe items: {len(medium_risk)+len(low_risk)} can be converted immediately\n")
    else:
        print(f"✅ All transcripts are safe - low duplication risk\n")
    
    print(f"📄 Full report: {report_path}\n")

if __name__ == '__main__':
    analyze_duplication_risk()
