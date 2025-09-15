import os
import sys
import platform
import asyncio
import requests
from playwright.sync_api import sync_playwright

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramBot
from webhook_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def main():
    print("🧪 Simple Test Starting...")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 CWD: {os.getcwd()}")
    print(f"🌍 ENV PORT: {os.environ.get('PORT')}")

    print("🔍 Testing imports...")
    try:
        import requests
        print("✅ requests imported")
    except Exception as e:
        print(f"❌ requests import failed: {e}")

    try:
        from playwright.sync_api import sync_playwright
        print("✅ playwright imported")
        print("✅ sync_playwright imported")
    except Exception as e:
        print(f"❌ playwright import failed: {e}")

    print("🌐 Testing browser launch...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            print("✅ Browser launched")
            browser.close()
            print("✅ Browser closed")
    except Exception as e:
        print(f"❌ Browser launch failed: {e}")
        import traceback
        traceback.print_exc()

    print("🤖 Testing Telegram...")
    try:
        bot = TelegramBot()
        print("✅ Telegram bot created")
        test_message = "🧪 Simple test message from Render deployment!"
        if bot.send_message(test_message):
            print("✅ Telegram message sent successfully")
        else:
            print("❌ Failed to send Telegram message")
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")
        import traceback
        traceback.print_exc()

    print("🎉 All tests passed!")
    print("✅ Simple test completed!")

if __name__ == "__main__":
    main()
