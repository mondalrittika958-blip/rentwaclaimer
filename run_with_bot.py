import threading
import time
from advanced_automation import AdvancedAutomation
from telegram_bot import TelegramBot

def run_automation_with_bot():
    """Run automation with Telegram bot polling"""
    print("🚀 Starting Advanced Automation with Telegram Bot...")
    
    # Initialize automation
    automation = AdvancedAutomation()
    
    # Initialize Telegram bot
    bot = TelegramBot()
    
    try:
        # Start automation in a separate thread
        automation_thread = threading.Thread(target=automation.start_monitoring)
        automation_thread.daemon = True
        automation_thread.start()
        
        print("✅ Automation started in background")
        print("🤖 Starting Telegram Bot (Polling Method)...")
        
        # Start bot polling (this will block)
        bot.start_polling()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping both automation and bot...")
        automation.stop()
        bot.stop()
    except Exception as e:
        print(f"❌ Error: {e}")
        automation.stop()
        bot.stop()

if __name__ == "__main__":
    run_automation_with_bot()
