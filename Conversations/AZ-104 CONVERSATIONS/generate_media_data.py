#!/usr/bin/env python3
import re
import json
import os

# Read the audio list
with open('/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Conversations/AZ-104 CONVERSATIONS/audio_list.txt', 'r') as f:
    lines = [line.strip()[2:] for line in f.readlines() if line.strip().startswith('./')]

# Function to determine domain from filename
def get_domain(filename):
    filename_lower = filename.lower()
    if any(x in filename_lower for x in ['vm', 'compute', 'container', 'aci', 'vmss', 'scale', 'bastion', 'disk', 'image']):
        return 'Compute'
    elif any(x in filename_lower for x in ['storage', 'blob', 'file', 'disk', 'backup', 'azcopy', 'redundancy']):
        return 'Storage'
    elif any(x in filename_lower for x in ['network', 'vnet', 'subnet', 'gateway', 'firewall', 'load', 'dns', 'nsg', 'vpn', 'peering']):
        return 'Networking'
    elif any(x in filename_lower for x in ['rbac', 'identity', 'entra', 'auth', 'access', 'permission', 'role']):
        return 'Identity'
    elif any(x in filename_lower for x in ['governance', 'compliance', 'policy', 'management', 'arm', 'template', 'bicep']):
        return 'Governance'
    elif any(x in filename_lower for x in ['monitor', 'alert', 'log', 'diagnostic']):
        return 'Monitor'
    else:
        return 'General'

# Function to generate new name
def generate_new_name(original):
    # Remove leading/trailing spaces and normalize
    clean = original.strip()
    
    # Get domain
    domain = get_domain(clean)
    
    # Get extension
    ext = clean.split('.')[-1] if '.' in clean else 'wav'
    
    # Remove extension for processing
    base = clean.rsplit('.', 1)[0] if '.' in clean else clean
    
    # Clean up the base name
    # Remove special characters and normalize spaces
    cleaned = re.sub(r'[^\w\s\-\_]', '_', base)
    cleaned = re.sub(r'\s+', '_', cleaned)
    cleaned = re.sub(r'_+', '_', cleaned)
    cleaned = cleaned.strip('_')
    
    # Create new name
    new_name = f"AZ-104-{domain}-{cleaned}.{ext}"
    
    return new_name

# Process all files
media_data = []
for original in lines:
    if not original:
        continue
        
    new_name = generate_new_name(original)
    ext = original.split('.')[-1].upper() if '.' in original else 'WAV'
    domain = get_domain(original)
    
    # Mock size and date for now
    size_mb = f"{round(20 + hash(original) % 80, 2)}"
    date_mod = "2025-01-15"
    
    entry = {
        "Original_Name": original,
        "New_Name": new_name,
        "Type": ext,
        "Domain": domain,
        "Size_MB": size_mb,
        "Date_Modified": date_mod
    }
    
    media_data.append(entry)

# Sort by domain then name
media_data.sort(key=lambda x: (x['Domain'], x['New_Name']))

print(f"// Generated {len(media_data)} media entries")
print("const MEDIA_DATA = [")
for i, item in enumerate(media_data):
    comma = "," if i < len(media_data) - 1 else ""
    print(f'  {json.dumps(item)}{comma}')
print("];")