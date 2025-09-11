from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "website-monitor-bot",
        "version": "1.0.0"
    })

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Website Monitor Bot is running",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
