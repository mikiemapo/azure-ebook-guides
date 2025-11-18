#!/usr/bin/env python3
"""
Fix filename mismatches in the media hub by creating a mapping
between the simplified names in HTML and actual file names.
"""

import os
import json
import re
from pathlib import Path

def scan_actual_files():
    """Scan the directory for actual audio/video files."""
    directory = Path("/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Conversations/AZ-104 CONVERSATIONS/")
    
    actual_files = []
    extensions = ['.m4a', '.wav', '.mp3', '.mp4', '.avi', '.mov']
    
    for ext in extensions:
        files = list(directory.glob(f'*{ext}'))
        actual_files.extend([f.name for f in files])
    
    return sorted(actual_files)

def create_filename_mapping():
    """Create a mapping between simplified names and actual file names."""
    actual_files = scan_actual_files()
    mapping = {}
    
    for actual_file in actual_files:
        # Create a simplified version by:
        # 1. Replace multiple underscores with single underscore
        # 2. Remove trailing underscores before extension
        simplified = re.sub(r'_+', '_', actual_file)
        simplified = re.sub(r'_+\.', '.', simplified)
        
        # If different, add to mapping
        if simplified != actual_file:
            mapping[simplified] = actual_file
            print(f"Mapping: {simplified} -> {actual_file}")
    
    return mapping

def generate_javascript_mapping():
    """Generate JavaScript code for filename mapping."""
    mapping = create_filename_mapping()
    
    js_code = """
// Filename mapping for cases where HTML names don't match actual files
const filenameMapping = {
"""
    
    for simplified, actual in mapping.items():
        js_code += f'  "{simplified}": "{actual}",\n'
    
    js_code += """};

function getActualFilename(filename) {
  return filenameMapping[filename] || filename;
}
"""
    
    return js_code

if __name__ == "__main__":
    print("🔍 Scanning for filename mismatches...")
    print("\n" + "="*50)
    
    actual_files = scan_actual_files()
    print(f"📁 Found {len(actual_files)} media files")
    
    print("\n🔧 Creating filename mapping...")
    mapping = create_filename_mapping()
    
    print(f"\n✅ Found {len(mapping)} filename mismatches")
    
    print("\n📝 Generated JavaScript mapping:")
    print("="*50)
    print(generate_javascript_mapping())