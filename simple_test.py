#!/usr/bin/env python3
"""
Simple test for Render
"""

import os
import sys
import time

def main():
    print("🧪 Simple Test Starting...")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 CWD: {os.getcwd()}")
    print(f"🌍 ENV PORT: {os.environ.get('PORT', 'Not set')}")
    
    try:
        print("📦 Testing imports...")
        import requests
        print("✅ requests imported")
        
        import playwright
        print("✅ playwright imported")
        
        from playwright.sync_api import sync_playwright
        print("✅ sync_playwright imported")
        
        print("🌐 Testing browser launch...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            print("✅ Browser launched")
            browser.close()
            print("✅ Browser closed")
        
        print("🤖 Testing Telegram...")
        from telegram_bot import TelegramBot
        bot = TelegramBot()
        print("✅ Telegram bot created")
        
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("✅ Simple test completed!")

if __name__ == "__main__":
    main()
