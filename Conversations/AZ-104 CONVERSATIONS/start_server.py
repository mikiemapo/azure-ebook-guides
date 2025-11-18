#!/usr/bin/env python3
"""
Simple HTTP server to serve the media hub files locally.
This resolves browser security restrictions when accessing local audio files.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Get the directory where this script is located
DIRECTORY = Path(__file__).parent
PORT = 8080

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow audio file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    """Start the HTTP server and open the browser."""
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Starting server at http://localhost:{PORT}")
        print(f"📁 Serving files from: {DIRECTORY}")
        print(f"🎯 Opening media hub in your browser...")
        print(f"✨ Press Ctrl+C to stop the server")
        
        # Open the browser to the media hub
        webbrowser.open(f'http://localhost:{PORT}/media-hub-static-complete.html')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")

if __name__ == "__main__":
    start_server()