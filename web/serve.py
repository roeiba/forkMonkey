#!/usr/bin/env python3
"""
Simple HTTP server for ForkMonkey web interface
"""

import http.server
import socketserver
import webbrowser
import os
import argparse
from pathlib import Path

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    parser = argparse.ArgumentParser(description='Simple HTTP server for ForkMonkey web interface')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    parser.add_argument('--dev', choices=['true', 'false'], default='true', help='Enable development mode')
    args = parser.parse_args()
    
    PORT = args.port
    dev_mode = args.dev == 'true'
    
    # Change to project root directory (parent of web/)
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print(f"Serving from: {project_root}")
    
    Handler = MyHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"""
╔═══════════════════════════════════════════╗
║     🐵 ForkMonkey Web Interface 🐵        ║
╚═══════════════════════════════════════════╝

Server running at: http://localhost:{PORT}

Press Ctrl+C to stop the server
        """)
        
        # Open browser to web/index.html
        dev_param = "?dev=true" if dev_mode else ""
        webbrowser.open(f'http://localhost:{PORT}/web/index.html{dev_param}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
