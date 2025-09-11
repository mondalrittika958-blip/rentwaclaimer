#!/usr/bin/env python3
"""
Main entry point for the Website Monitor Bot
Runs 24/7 on Render with GitHub integration
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def run_bot():
    """Run the automation bot"""
    try:
        from advanced_automation_playwright import AdvancedAutomation, WEBSITES
        from telegram_bot import TelegramBot
        from webhook_config import get_telegram_bot

        # Initialize Telegram Bot
        telegram_bot_instance = get_telegram_bot()
        telegram_bot_thread = threading.Thread(target=telegram_bot_instance.start_polling, daemon=True)
        telegram_bot_thread.start()
        logger.info("🤖 Telegram Bot polling started in background.")

        # Start Advanced Automation
        automation = AdvancedAutomation()
        automation.start_monitoring()

    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        import traceback
        traceback.print_exc()

        # Restart after error (for 24/7 operation)
        logger.info("🔄 Restarting bot in 30 seconds...")
        time.sleep(30)
        run_bot()

def run_health_server():
    """Run the health check server"""
    try:
        from health_check import app
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"❌ Health server error: {e}")

def main():
    """Main function to run both bot and health server"""
    logger.info("🚀 Starting Website Monitor Bot...")
    logger.info(f"⏰ Start time: {datetime.now()}")
    
    # Start health server in a separate thread
    health_thread = threading.Thread(target=run_health_server)
    health_thread.daemon = True
    health_thread.start()
    
    logger.info("🏥 Health server started")
    
    # Run the bot in main thread
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Main error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
