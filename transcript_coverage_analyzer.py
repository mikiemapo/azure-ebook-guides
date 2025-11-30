#!/usr/bin/env python3
"""
Analyze which transcripts are already covered by existing deck batches
vs. which represent new, unconverted content.
"""

import csv
import os
import re
from collections import defaultdict
from datetime import datetime

# Configuration
EBOOK_DIR = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK"
MASTER_CSV = os.path.join(EBOOK_DIR, "AZ-104-Study-Deck/AZ-104-Master-Questions.csv")
AUDIO_LIST = os.path.join(EBOOK_DIR, "audio_list.txt")
REPORTS_DIR = os.path.join(EBOOK_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

def extract_keywords(text):
    """Extract meaningful keywords from text."""
    # Remove common words and special characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Extract words longer than 3 characters
    words = [w for w in text.split() if len(w) > 3]
    
    # Remove common Azure terms to reduce noise
    common = {'azure', 'virtual', 'network', 'storage', 'compute', 'service', 'machine', 
              'managed', 'policy', 'resource', 'access', 'identity', 'monitoring', 'security',
              'deployment', 'configuration', 'operations', 'management'}
    
    keywords = [w for w in words if w not in common]
    return set(keywords[:10])  # Top 10 keywords

def get_batch_keywords():
    """Extract keywords from all existing deck batches."""
    batch_keywords = defaultdict(set)
    
    try:
        with open(MASTER_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                batch = row.get('Batch', '').strip()
                question = row.get('Question', '').strip()
                
                if batch and question:
                    keywords = extract_keywords(batch + ' ' + question)
                    batch_keywords[batch].update(keywords)
    except Exception as e:
        print(f"❌ Error reading master CSV: {e}")
    
    return batch_keywords

def extract_az104_transcripts():
    """Extract AZ-104 transcripts from audio_list.txt."""
    transcripts = []
    
    try:
        with open(AUDIO_LIST, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Look for AZ-104 references (case-insensitive)
                if 'az-104' in line.lower() or 'az104' in line.lower():
                    # Clean up the path for display
                    transcript = line.replace('./', '').strip()
                    transcripts.append(transcript)
    except Exception as e:
        print(f"❌ Error reading audio_list.txt: {e}")
    
    return transcripts

def calculate_match_score(transcript_name, batch_keywords_dict):
    """
    Calculate match score between transcript and existing batches.
    Returns: (best_batch, score, all_matches)
    """
    trans_keywords = extract_keywords(transcript_name)
    
    all_matches = []
    for batch, batch_kw in batch_keywords_dict.items():
        # Calculate overlap
        overlap = trans_keywords.intersection(batch_kw)
        score = len(overlap) / max(len(trans_keywords), len(batch_kw), 1)
        
        if score > 0:
            all_matches.append((batch, score, len(overlap)))
    
    # Sort by score descending
    all_matches.sort(key=lambda x: x[1], reverse=True)
    
    best = all_matches[0] if all_matches else (None, 0, 0)
    return best[0], best[1], all_matches[:3]  # Top 3 matches

def categorize_transcript(transcript_name):
    """Categorize transcript by topic."""
    trans_lower = transcript_name.lower()
    
    categories = {
        'App Service': ['app service', 'webapp', 'function', 'container', 'aci', 'aks'],
        'Storage': ['storage', 'blob', 'file', 'queue', 'table', 'databox', 'azcopy'],
        'Networking': ['network', 'vnet', 'nsg', 'firewall', 'gateway', 'load balancer', 
                      'vpn', 'expressroute', 'peering', 'dns'],
        'Compute': ['vm', 'virtual machine', 'vmss', 'scale set', 'disk', 'image', 
                   'linux', 'windows', 'availability'],
        'Identity': ['rbac', 'aad', 'ad', 'identity', 'msi', 'keyvault', 'secret'],
        'Backup/DR': ['backup', 'recovery', 'site recovery', 'vabrf', 'resilience', 
                     'ransomware', 'disaster'],
        'Monitoring': ['monitor', 'alert', 'log', 'metrics', 'application insight', 
                      'diagnostic'],
        'Governance': ['policy', 'compliance', 'governance', 'blueprint', 'management'],
    }
    
    for category, keywords in categories.items():
        if any(kw in trans_lower for kw in keywords):
            return category
    
    return 'Other'

def analyze_coverage():
    """Main analysis function."""
    print(f"\n🔍 Analyzing Transcript Coverage")
    print(f"{'='*80}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get batch keywords
    print("📖 Reading existing deck batches...")
    batch_keywords = get_batch_keywords()
    print(f"✅ Found {len(batch_keywords)} batches\n")
    
    # Extract transcripts
    print("🎵 Reading transcripts from audio_list.txt...")
    all_transcripts = extract_az104_transcripts()
    
    print(f"✅ Found {len(all_transcripts)} unique AZ-104 transcripts\n")
    
    # Handle empty case
    if len(all_transcripts) == 0:
        print(f"\n❌ No AZ-104 transcripts found in audio_list.txt")
        print(f"Please verify the file contains AZ-104 entries.")
        return
    
    unique_transcripts = all_transcripts
    
    # Analyze each transcript
    covered = []
    new = []
    ambiguous = []
    
    print(f"📊 Analyzing coverage...\n")
    
    for i, transcript in enumerate(sorted(unique_transcripts), 1):
        best_batch, score, top_matches = calculate_match_score(transcript, batch_keywords)
        category = categorize_transcript(transcript)
        
        result = {
            'transcript': transcript,
            'category': category,
            'best_batch': best_batch,
            'score': score,
            'top_matches': top_matches
        }
        
        if score >= 0.5:
            covered.append(result)
        elif score >= 0.3:
            ambiguous.append(result)
        else:
            new.append(result)
        
        if i % 30 == 0:
            print(f"   Processed {i}/{len(unique_transcripts)}...")
    
    print(f"✅ Analysis complete!\n")
    
    # Generate report
    report_path = os.path.join(REPORTS_DIR, f"coverage_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("TRANSCRIPT COVERAGE ANALYSIS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # Summary
        f.write("📊 SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Transcripts: {len(unique_transcripts)}\n")
        f.write(f"Already Covered: {len(covered)} ({100*len(covered)/len(unique_transcripts):.1f}%)\n")
        f.write(f"Ambiguous: {len(ambiguous)} ({100*len(ambiguous)/len(unique_transcripts):.1f}%)\n")
        f.write(f"NEW (Not Covered): {len(new)} ({100*len(new)/len(unique_transcripts):.1f}%)\n\n")
        
        # Covered transcripts
        f.write("✅ ALREADY COVERED BY EXISTING BATCHES\n")
        f.write("-"*80 + "\n")
        f.write(f"Count: {len(covered)} transcripts\n\n")
        
        by_batch = defaultdict(list)
        for item in covered:
            by_batch[item['best_batch']].append(item)
        
        for batch in sorted(by_batch.keys()):
            items = by_batch[batch]
            f.write(f"\n{batch} ({len(items)} transcripts, avg match: {sum(x['score'] for x in items)/len(items):.2f}):\n")
            for item in items[:5]:  # Show first 5
                f.write(f"  • {item['transcript'][:70]} (score: {item['score']:.2f})\n")
            if len(items) > 5:
                f.write(f"  ... and {len(items)-5} more\n")
        
        f.write(f"\n\n🆕 NEW TRANSCRIPTS (NOT COVERED - HIGH PRIORITY)\n")
        f.write("-"*80 + "\n")
        f.write(f"Count: {len(new)} transcripts\n")
        f.write(f"These represent completely new content that should be converted to deck questions.\n\n")
        
        # Group by category
        new_by_category = defaultdict(list)
        for item in new:
            new_by_category[item['category']].append(item)
        
        for category in sorted(new_by_category.keys()):
            items = new_by_category[category]
            f.write(f"\n{category} ({len(items)} transcripts):\n")
            for item in items[:20]:  # Show first 20
                f.write(f"  • {item['transcript'][:75]}\n")
            if len(items) > 20:
                f.write(f"  ... and {len(items)-20} more\n")
        
        f.write(f"\n\n❓ AMBIGUOUS (POSSIBLE MATCH - REVIEW)\n")
        f.write("-"*80 + "\n")
        f.write(f"Count: {len(ambiguous)} transcripts\n")
        f.write(f"These might be already covered but with low confidence (30-50% match).\n")
        f.write(f"Consider manual review to confirm if they need new deck generation.\n\n")
        
        for item in ambiguous:
            f.write(f"• {item['transcript'][:70]}\n")
            f.write(f"  Category: {item['category']}\n")
            if item['best_batch']:
                f.write(f"  Possible match: {item['best_batch']} ({item['score']:.2f})\n")
            f.write("\n")
        
        # Recommendations
        f.write(f"\n\n💡 RECOMMENDATIONS\n")
        f.write("-"*80 + "\n")
        f.write(f"1. IMMEDIATE: Convert {len(new)} new transcripts to deck questions\n")
        f.write(f"   Priority by category:\n")
        
        category_counts = sorted(new_by_category.items(), key=lambda x: len(x[1]), reverse=True)
        for cat, items in category_counts[:5]:
            f.write(f"     • {cat}: {len(items)} transcripts\n")
        
        f.write(f"\n2. REVIEW: Verify {len(ambiguous)} ambiguous transcripts\n")
        f.write(f"   Ensure they're not already covered before conversion\n")
        f.write(f"\n3. CONSOLIDATE: Remove duplicate transcripts (37 found previously)\n")
        f.write(f"   This will reduce actual count and improve quality\n")
    
    # Console output
    print(f"\n{'='*80}")
    print(f"📊 COVERAGE SUMMARY")
    print(f"{'='*80}")
    print(f"\n✅ Already Covered: {len(covered)}/{len(unique_transcripts)} ({100*len(covered)/len(unique_transcripts):.1f}%)")
    print(f"❓ Ambiguous: {len(ambiguous)}/{len(unique_transcripts)} ({100*len(ambiguous)/len(unique_transcripts):.1f}%)")
    print(f"🆕 NEW (Not Covered): {len(new)}/{len(unique_transcripts)} ({100*len(new)/len(unique_transcripts):.1f}%)")
    
    print(f"\n🆕 NEW BY CATEGORY:")
    for cat, items in sorted(new_by_category.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {cat}: {len(items)} transcripts")
    
    print(f"\n📄 Full report saved to: {report_path}\n")
    
    return {
        'covered': covered,
        'new': new,
        'ambiguous': ambiguous,
        'total': len(unique_transcripts)
    }

if __name__ == '__main__':
    analyze_coverage()
