#!/usr/bin/env python3
"""
Main entry point for the Website Monitor Bot
This is the production version that runs on Render
"""

import time
import logging
import threading
from advanced_automation_playwright import AdvancedAutomation
from health_server import run_health_server

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to run automation"""
    try:
        logger.info("🚀 Starting Website Monitor Bot...")
        logger.info(f"⏰ Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Start health server in background
        logger.info("🏥 Starting health server...")
        run_health_server()
        
        # Create automation instance
        automation = AdvancedAutomation()

        # Start Telegram bot in background
        logger.info("🤖 Starting Telegram bot...")
        from telegram_bot import TelegramBot
        bot = TelegramBot()
        bot.set_automation(automation)  # Connect automation to bot
        bot_thread = threading.Thread(target=bot.start_polling, daemon=False)
        bot_thread.start()
        
        # Give bot time to start
        logger.info("⏳ Waiting for bot to initialize...")
        time.sleep(10)
        
        # Start monitoring in background
        logger.info("🌐 Starting website monitoring...")
        monitor_thread = threading.Thread(target=automation.start_monitoring, daemon=True)
        monitor_thread.start()
        
        # Keep main thread alive
        logger.info("✅ All services started! Bot is now active.")
        try:
            while True:
                time.sleep(60)
                logger.info("💓 Bot heartbeat - All services running")
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down...")
        
    except KeyboardInterrupt:
        logger.info("🛑 Automation stopped by user")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
