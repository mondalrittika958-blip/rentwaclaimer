#!/usr/bin/env python3
"""
Main entry point for the automation bot
This file is used for Render deployment
"""

import os
import sys
import threading
from flask import Flask
# Smart automation selection - Real website data preferred
import os
try:
    # Try Selenium first for real website automation
    from selenium_automation import SeleniumAutomation as AutomationClass
    automation_type = "Selenium Real Website Automation"
    print("🚀 Using Selenium for REAL website data")
except Exception as e:
    print(f"❌ Selenium import failed: {e}")
    try:
        # Fallback to Playwright
        from advanced_automation_playwright import AdvancedAutomation as AutomationClass
        automation_type = "Playwright Real Website Automation"
        print("🚀 Using Playwright for REAL website data")
    except Exception as e2:
        print(f"❌ Playwright also failed: {e2}")
        from render_automation import RenderAutomation as AutomationClass
        automation_type = "Simulation Mode (Last Resort)"
        print("⚠️ Using simulation mode as last resort")

# Create Flask app for health check
app = Flask(__name__)

@app.route('/')
def health_check():
    return {
        "status": "running",
        "service": "Website Monitor Bot",
        "message": "Bot is monitoring 4 websites 24/7"
    }

@app.route('/status')
def bot_status():
    return {
        "bot_status": "active",
        "websites": ["kamkg.com", "kamate1.com", "wha2.net", "lootlelo.com"],
        "monitoring_interval": "1 hour",
        "telegram_integration": "enabled"
    }

def run_automation():
    """Run automation in background thread"""
    try:
        automation = AutomationClass()
        automation.start_monitoring()
    except Exception as e:
        print(f"❌ Automation error: {e}")

def main():
    """Main function to start the automation"""
    print("🚀 Starting Automation Bot...")
    print("📱 Telegram Bot Integration: Enabled")
    print("⏰ Monitoring Interval: 1 hour")
    print("🌐 Websites: kamkg.com, kamate1.com, wha2.net, lootlelo.com")
    print(f"🔧 Using {automation_type} automation")
    
    try:
        # Start automation in background thread
        automation_thread = threading.Thread(target=run_automation, daemon=True)
        automation_thread.start()
        print("✅ Automation started in background")
        
        # Start Flask health check server
        port = int(os.environ.get("PORT", 10000))
        print(f"🏥 Starting health check server on port {port}")
        app.run(host="0.0.0.0", port=port, debug=False)
        
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()