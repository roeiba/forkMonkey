#!/usr/bin/env python3
"""
Simple HTTP server for ForkMonkey web interface
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    # Change to web directory
    web_dir = Path(__file__).parent
    os.chdir(web_dir)
    
    Handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"""
╔═══════════════════════════════════════════╗
║     🐵 ForkMonkey Web Interface 🐵       ║
╚═══════════════════════════════════════════╝

Server running at: http://localhost:{PORT}

Press Ctrl+C to stop the server
        """)
        
        # Open browser
        webbrowser.open(f'http://localhost:{PORT}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
