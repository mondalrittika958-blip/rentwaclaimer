#!/usr/bin/env python3
"""
Simple health check server for Render
This prevents the "No open ports detected" warning
"""

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health_data = {
                "status": "healthy",
                "service": "website-monitor-bot",
                "timestamp": datetime.now().isoformat(),
                "message": "Bot is running and monitoring websites"
            }
            
            self.wfile.write(json.dumps(health_data).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Website Monitor Bot</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .status { color: green; font-weight: bold; }
                </style>
            </head>
            <body>
                <h1>🤖 Website Monitor Bot</h1>
                <p class="status">✅ Bot is running and monitoring websites</p>
                <p>Monitoring: kamkg.com, kamate1.com, wha2.net, lootlelo.com</p>
                <p>Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_health_server():
    """Start the health check server"""
    try:
        server = HTTPServer(('0.0.0.0', 10000), HealthHandler)
        print("🏥 Health server started on port 10000")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Health server error: {e}")

def run_health_server():
    """Run health server in background thread"""
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    print("✅ Health server thread started")

if __name__ == "__main__":
    run_health_server()
    # Keep the script running
    while True:
        time.sleep(1)
