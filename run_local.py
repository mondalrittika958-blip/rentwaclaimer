#!/usr/bin/env python3
"""
Run the automation locally and in production
This file works both locally and on Render
"""

import time
import logging
import threading
import os
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
        
        # Run tests first
        logger.info("🧪 Running system tests...")
        from simple_test import main as test_main
        test_main()
        
        # Start health server in background (for Render)
        if os.environ.get('PORT'):
            logger.info("🏥 Starting health server...")
            run_health_server()

        # Create automation instance
        logger.info("🤖 Creating automation instance...")
        automation = AdvancedAutomation()

        # Start Telegram bot in background
        logger.info("🤖 Starting Telegram bot...")
        from telegram_bot import TelegramBot
        bot = TelegramBot()
        bot.set_automation(automation)  # Connect automation to bot
        bot_thread = threading.Thread(target=bot.start_polling, daemon=True)
        bot_thread.start()

        # Start monitoring
        logger.info("🌐 Starting website monitoring...")
        
        # Test browser automation first
        logger.info("🧪 Testing browser automation...")
        try:
            from advanced_automation_playwright import WEBSITES
            test_site = WEBSITES[0]  # kamkg.com
            logger.info(f"🔍 Testing with {test_site['name']}")
            automation.monitor_site_once(test_site)
            logger.info("✅ Browser automation test completed")
        except Exception as e:
            logger.error(f"❌ Browser automation test failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Start full monitoring
        logger.info("🚀 Starting full monitoring...")
        automation.start_monitoring()
        
    except KeyboardInterrupt:
        logger.info("🛑 Automation stopped by user")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
