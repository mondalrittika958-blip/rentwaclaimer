#!/usr/bin/env python3
"""
Test complete bot functionality with polling
"""
import time
import threading
from telegram_bot import TelegramBot

def test_live_bot():
    """Test live bot with real polling"""
    print("🧪 Testing Live Bot...")
    
    try:
        # Create bot instance
        bot = TelegramBot()
        print(f"🤖 Bot created successfully")
        print(f"📱 Token: {bot.bot_token[:15]}...")
        print(f"📢 Channel: {bot.chat_id}")
        print(f"👤 User: {bot.user_chat_id}")
        
        # Start polling in the main thread (not daemon)
        print(f"\n🚀 Starting bot polling...")
        print(f"👆 Go to @money_claimer_bot and try clicking buttons!")
        
        # This will run indefinitely until interrupted
        bot.start_polling()
        
    except KeyboardInterrupt:
        print(f"\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error in live bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Set environment variable
    import os
    os.environ["TELEGRAM_BOT_TOKEN"] = "8251061362:AAEVeQ36DY-cSDPkjeoSt9065P6FBKQOKHA"
    
    test_live_bot()
    print("✅ Live bot test finished!")
