#!/usr/bin/env python3
"""
Consolidate duplicate transcripts by identifying variations and creating a cleaned list.
Outputs: mapping, recommendations, and cleaned audio_list.txt
"""

import re
import os
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher

EBOOK_DIR = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK"
AUDIO_LIST = os.path.join(EBOOK_DIR, "audio_list.txt")
REPORTS_DIR = os.path.join(EBOOK_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

def normalize_transcript_name(name):
    """Normalize transcript name for comparison."""
    # Remove file extensions
    name = re.sub(r'\.(wav|mp4|m4a|flac|aac)$', '', name, flags=re.IGNORECASE)
    # Remove version suffixes
    name = re.sub(r'\s*\(?v?(\d+\.?\d*|version)\)?', '', name, flags=re.IGNORECASE)
    # Remove duplicate markers (1), (2), etc.
    name = re.sub(r'\s*\(\d+\)\s*$', '', name)
    # Remove leading/trailing whitespace and normalize
    name = name.strip().lower()
    # Normalize special characters
    name = re.sub(r'[_\-\s]+', ' ', name)
    return name

def similarity_score(str1, str2):
    """Calculate similarity between two strings (0-1)."""
    return SequenceMatcher(None, str1, str2).ratio()

def extract_az104_transcripts():
    """Extract AZ-104 transcripts from audio_list.txt."""
    transcripts = []
    try:
        with open(AUDIO_LIST, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and 'az-104' in line.lower():
                    transcripts.append(line)
    except Exception as e:
        print(f"❌ Error reading audio_list.txt: {e}")
    return transcripts

def find_duplicates(transcripts, threshold=0.75):
    """Find potential duplicates using normalized comparison."""
    duplicates = defaultdict(list)
    normalized_map = {}
    
    for transcript in transcripts:
        normalized = normalize_transcript_name(transcript)
        normalized_map[transcript] = normalized
    
    # Group by normalized name
    grouped = defaultdict(list)
    for transcript, normalized in normalized_map.items():
        grouped[normalized].append(transcript)
    
    # Find groups with multiple items
    duplicate_groups = {k: v for k, v in grouped.items() if len(v) > 1}
    
    return duplicate_groups, normalized_map

def extract_category(transcript):
    """Extract category from transcript name."""
    trans_lower = transcript.lower()
    
    categories = {
        'Networking': ['network', 'vnet', 'nsg', 'firewall', 'gateway', 'load balancer', 
                      'vpn', 'expressroute', 'peering', 'dns'],
        'Storage': ['storage', 'blob', 'file', 'queue', 'azcopy', 'databox'],
        'Compute': ['vm', 'virtual machine', 'vmss', 'scale set', 'disk', 'linux', 'windows'],
        'App Service': ['app service', 'webapp', 'function', 'container', 'aci', 'aks'],
        'Identity': ['rbac', 'aad', 'ad', 'identity', 'msi', 'keyvault'],
        'Monitoring': ['monitor', 'alert', 'log', 'metrics'],
        'Governance': ['policy', 'compliance', 'governance', 'blueprint'],
        'Backup/DR': ['backup', 'recovery', 'site recovery', 'vabrf', 'resilience'],
    }
    
    for category, keywords in categories.items():
        if any(kw in trans_lower for kw in keywords):
            return category
    return 'Other'

def analyze_duplicates():
    """Main analysis function."""
    print(f"\n🔍 Analyzing Duplicate Transcripts")
    print(f"{'='*80}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Extract transcripts
    print("📖 Reading AZ-104 transcripts...")
    transcripts = extract_az104_transcripts()
    print(f"✅ Found {len(transcripts)} transcripts\n")
    
    # Find duplicates
    print("🔎 Identifying duplicates...")
    duplicate_groups, normalized_map = find_duplicates(transcripts)
    
    print(f"✅ Found {len(duplicate_groups)} duplicate groups")
    print(f"📊 Total duplicates: {sum(len(v)-1 for v in duplicate_groups.values())}\n")
    
    # Generate report
    report_path = os.path.join(REPORTS_DIR, f"duplicates_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("DUPLICATE TRANSCRIPT CONSOLIDATION REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # Summary
        f.write("📊 SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Transcripts: {len(transcripts)}\n")
        f.write(f"Duplicate Groups: {len(duplicate_groups)}\n")
        f.write(f"Duplicate Instances: {sum(len(v)-1 for v in duplicate_groups.values())}\n")
        f.write(f"Unique Transcripts After Consolidation: {len(transcripts) - sum(len(v)-1 for v in duplicate_groups.values())}\n\n")
        
        # Duplicate groups
        f.write("🔴 DUPLICATE GROUPS (CONSOLIDATION REQUIRED)\n")
        f.write("-"*80 + "\n\n")
        
        for i, (normalized, group) in enumerate(sorted(duplicate_groups.items()), 1):
            category = extract_category(group[0])
            f.write(f"{i}. {category} - {len(group)} instances\n")
            f.write(f"   Normalized: {normalized}\n")
            f.write(f"   Instances:\n")
            
            for j, transcript in enumerate(group, 1):
                # Extract just the filename part
                filename = transcript.replace('./Conversations /AZ-104 CONVERSATIONS/', '')
                f.write(f"      [{j}] {filename}\n")
            
            # Recommend keeping the cleanest name
            best = max(group, key=lambda x: len(x))
            best_filename = best.replace('./Conversations /AZ-104 CONVERSATIONS/', '')
            f.write(f"   → KEEP: {best_filename}\n")
            f.write(f"   → DELETE: {len(group)-1} others\n\n")
        
        # Generate cleaned list
        f.write("\n💾 CONSOLIDATED LIST (RECOMMENDED)\n")
        f.write("-"*80 + "\n")
        f.write(f"Keep {len(transcripts) - sum(len(v)-1 for v in duplicate_groups.values())} unique transcripts:\n\n")
        
        kept_transcripts = []
        for normalized, group in duplicate_groups.items():
            # Keep the longest/cleanest name
            best = max(group, key=lambda x: len(x))
            kept_transcripts.append(best)
        
        # Add non-duplicate transcripts
        for transcript in transcripts:
            normalized = normalized_map[transcript]
            if normalized not in duplicate_groups:
                kept_transcripts.append(transcript)
        
        kept_transcripts.sort()
        for transcript in kept_transcripts:
            filename = transcript.replace('./Conversations /AZ-104 CONVERSATIONS/', '')
            category = extract_category(transcript)
            f.write(f"• [{category:12}] {filename}\n")
        
        # CSV format for easy import
        f.write("\n\n📋 CSV FORMAT (For merging into master)\n")
        f.write("-"*80 + "\n")
        f.write("Batch,Question,Answer\n")
        
        for transcript in sorted(kept_transcripts):
            category = extract_category(transcript)
            filename = transcript.replace('./Conversations /AZ-104 CONVERSATIONS/', '').replace('.wav', '').replace('.mp4', '').replace('.m4a', '')
            batch = f"Transcript Conversion::{category}"
            q = f"Source: {filename}"
            a = f"Transcript file to be processed into deck questions"
            f.write(f'"{batch}","{q}","{a}"\n')
    
    # Console output
    print(f"{'='*80}")
    print(f"✅ CONSOLIDATION SUMMARY")
    print(f"{'='*80}")
    print(f"\n🔴 Duplicates Found: {sum(len(v)-1 for v in duplicate_groups.values())}")
    print(f"🟢 After Consolidation: {len(transcripts) - sum(len(v)-1 for v in duplicate_groups.values())} unique transcripts")
    print(f"📈 Space Saved: {sum(len(v)-1 for v in duplicate_groups.values())} transcripts\n")
    
    print(f"📄 Full report saved to: {report_path}\n")
    
    # Save consolidated list
    consolidated_path = os.path.join(EBOOK_DIR, "audio_list_consolidated.txt")
    kept_transcripts_unique = set()
    for normalized, group in duplicate_groups.items():
        best = max(group, key=lambda x: len(x))
        kept_transcripts_unique.add(best)
    for transcript in transcripts:
        normalized = normalized_map[transcript]
        if normalized not in duplicate_groups:
            kept_transcripts_unique.add(transcript)
    
    with open(consolidated_path, 'w', encoding='utf-8') as f:
        for transcript in sorted(kept_transcripts_unique):
            f.write(transcript + "\n")
    
    print(f"✅ Consolidated list saved to: audio_list_consolidated.txt\n")
    
    return duplicate_groups, normalized_map

if __name__ == '__main__':
    analyze_duplicates()
