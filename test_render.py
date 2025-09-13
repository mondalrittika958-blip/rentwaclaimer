#!/usr/bin/env python3
"""
Test script for Render deployment
"""

import os
import time
import sys

def test_playwright():
    """Test Playwright installation and browser launch"""
    print("🧪 Testing Playwright on Render...")
    
    try:
        from playwright.sync_api import sync_playwright
        print("✅ Playwright imported successfully")
        
        with sync_playwright() as p:
            print("✅ Playwright context created")
            
            # Launch browser
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-gpu',
                    '--window-size=1366,768'
                ]
            )
            print("✅ Browser launched successfully")
            
            # Create context
            context = browser.new_context(
                viewport={'width': 375, 'height': 667},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            )
            print("✅ Browser context created")
            
            # Create page
            page = context.new_page()
            print("✅ Browser page created")
            
            # Test navigation
            page.goto("https://kamkg.com/#/pages/login/index", timeout=30000)
            print("✅ Navigation successful")
            
            # Get page title
            title = page.title()
            print(f"✅ Page title: {title}")
            
            # Close browser
            browser.close()
            print("✅ Browser closed successfully")
            
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_telegram():
    """Test Telegram bot"""
    print("🤖 Testing Telegram bot...")
    
    try:
        from telegram_bot import TelegramBot
        bot = TelegramBot()
        print("✅ Telegram bot created")
        
        # Test sending message
        result = bot.send_message("🧪 Test message from Render")
        if result:
            print("✅ Telegram message sent successfully")
        else:
            print("❌ Failed to send Telegram message")
            
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 Starting Render Tests...")
    print(f"⏰ Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Test Playwright
    playwright_ok = test_playwright()
    
    print("\n" + "="*50 + "\n")
    
    # Test Telegram
    telegram_ok = test_telegram()
    
    print("\n" + "="*50 + "\n")
    
    if playwright_ok and telegram_ok:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    print("✅ Test completed!")

if __name__ == "__main__":
    main()
