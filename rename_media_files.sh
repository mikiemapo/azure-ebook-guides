#!/bin/bash

# Rename script for AZ-104 media files
# Generated from media_catalog.csv
# Run from: /Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK

set -e  # Exit on error

MEDIA_DIR="Conversations /AZ-104 CONVERSATIONS"
CSV_FILE="docs/media_catalog.csv"

echo "🔄 Starting rename process..."
echo "📁 Working directory: $MEDIA_DIR"
echo ""

# Check if CSV exists
if [ ! -f "$CSV_FILE" ]; then
    echo "❌ Error: $CSV_FILE not found!"
    exit 1
fi

# Counter
renamed=0
skipped=0

# Read CSV (skip header) and rename files
tail -n +2 "$CSV_FILE" | while IFS=',' read -r original new_name type domain size date guide path; do
    # Remove quotes if present
    original=$(echo "$original" | sed 's/^"//;s/"$//')
    new_name=$(echo "$new_name" | sed 's/^"//;s/"$//')
    
    old_path="$MEDIA_DIR/$original"
    new_path="$MEDIA_DIR/$new_name"
    
    # Skip if already renamed
    if [ "$original" == "$new_name" ]; then
        ((skipped++))
        continue
    fi
    
    # Check if source file exists
    if [ ! -f "$old_path" ]; then
        echo "⚠️  Source not found: $original"
        continue
    fi
    
    # Check if destination already exists
    if [ -f "$new_path" ]; then
        echo "⚠️  Already exists: $new_name"
        continue
    fi
    
    # Perform rename
    mv "$old_path" "$new_path"
    ((renamed++))
    echo "✓ $original"
    echo "  → $new_name"
done

echo ""
echo "✅ Rename complete!"
echo "   Renamed: $renamed files"
echo "   Skipped: $skipped files (already renamed)"
echo ""
echo "Next steps:"
echo "1. Verify files in: $MEDIA_DIR"
echo "2. Commit changes: git add . && git commit -m 'Organize media library'"
echo "3. Post-commit hook will sync to Readdle and push to GitHub"
