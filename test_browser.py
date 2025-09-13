#!/usr/bin/env python3
"""
Test browser automation on Render
"""

import os
import time
from advanced_automation_playwright import AdvancedAutomation, WEBSITES

def test_browser_automation():
    """Test browser automation functionality"""
    print("🌐 Testing Browser Automation...")
    
    try:
        # Set environment variables
        os.environ['TELEGRAM_BOT_TOKEN'] = '8251061362:AAGJgQDANqnOUYogInclBP3sZ6LVYlz4HoQ'
        os.environ['TELEGRAM_CHAT_ID'] = '-1003095344192'
        
        automation = AdvancedAutomation()
        print("✅ Automation instance created")
        
        # Test with first website
        test_site = WEBSITES[0]  # kamkg.com
        print(f"🔍 Testing with {test_site['name']}")
        print(f"🔗 URL: {test_site['url']}")
        
        # Test monitor_site_once
        print("🚀 Starting browser automation...")
        automation.monitor_site_once(test_site)
        print("✅ Browser automation test completed")
        
    except Exception as e:
        print(f"❌ Browser automation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_browser_automation()
