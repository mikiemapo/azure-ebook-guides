#!/bin/bash
# Quick launcher for the media hub server

echo "🎯 AZ-104 Media Hub Server Launcher"
echo "===================================="

# Navigate to the directory
cd "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Conversations/AZ-104 CONVERSATIONS/"

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
    python3 start_server.py
elif command -v python &> /dev/null; then
    echo "✅ Python found"
    python start_server.py
else
    echo "❌ Python not found. Please install Python 3."
    echo "📋 You can install it from: https://python.org"
    exit 1
fi