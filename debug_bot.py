#!/usr/bin/env python3
"""
Debug script to test bot functionality
"""

import os
import time
from advanced_automation_playwright import AdvancedAutomation
from telegram_bot import TelegramBot

def test_telegram_bot():
    """Test Telegram bot functionality"""
    print("🤖 Testing Telegram Bot...")
    
    try:
        bot = TelegramBot()
        print(f"✅ Bot Token: {bot.bot_token[:10]}...")
        print(f"✅ Chat ID: {bot.chat_id}")
        
        # Test sending a message
        test_message = "🧪 Test message from debug script"
        result = bot.send_message(test_message)
        if result:
            print("✅ Telegram message sent successfully")
        else:
            print("❌ Failed to send Telegram message")
            
    except Exception as e:
        print(f"❌ Telegram bot error: {e}")

def test_automation():
    """Test automation functionality"""
    print("🔍 Testing Automation...")
    
    try:
        automation = AdvancedAutomation()
        print("✅ Automation instance created")
        
        # Test with first website only
        from advanced_automation_playwright import WEBSITES
        test_site = WEBSITES[0]  # kamkg.com
        
        print(f"🌐 Testing with {test_site['name']}")
        print(f"🔗 URL: {test_site['url']}")
        
        # Test amount update
        automation.send_amount_update(test_site['name'], "1000", "test")
        print("✅ Amount update test completed")
        
    except Exception as e:
        print(f"❌ Automation error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main debug function"""
    print("🚀 Starting Bot Debug...")
    print(f"⏰ Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test Telegram bot
    test_telegram_bot()
    
    print("\n" + "="*50 + "\n")
    
    # Test automation
    test_automation()
    
    print("\n✅ Debug completed!")

if __name__ == "__main__":
    main()
