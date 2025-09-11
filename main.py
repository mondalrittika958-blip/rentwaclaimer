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

def run_automation():
    """Run the automation bot in a separate process"""
    try:
        # Wait a bit for everything to be ready
        time.sleep(10)
        
        import subprocess
        import sys
        
        logger.info("🚀 Starting simple automation process...")
        
        # Start the simple automation process
        process = subprocess.Popen([
            sys.executable, "simple_automation.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        logger.info("✅ Simple automation process started")
        
        # Monitor the process
        while True:
            # Check if process is still running
            if process.poll() is not None:
                logger.error("❌ Automation process stopped, restarting...")
                # Read any output before restarting
                try:
                    stdout, stderr = process.communicate(timeout=5)
                    if stdout:
                        logger.info(f"Automation stdout: {stdout}")
                    if stderr:
                        logger.error(f"Automation stderr: {stderr}")
                except subprocess.TimeoutExpired:
                    logger.warning("⚠️ Timeout reading process output")
                    process.kill()
                
                # Wait a bit before restarting
                time.sleep(5)
                
                # Restart the process
                process = subprocess.Popen([
                    sys.executable, "simple_automation.py"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                logger.info("🔄 Automation process restarted")
            
            time.sleep(30)  # Check every 30 seconds

    except Exception as e:
        logger.error(f"❌ Automation error: {e}")
        import traceback
        traceback.print_exc()

        # Restart after error (for 24/7 operation)
        logger.info("🔄 Restarting automation in 30 seconds...")
        time.sleep(30)
        run_automation()

def run_bot():
    """Run the automation bot"""
    try:
        from telegram_bot import TelegramBot
        from webhook_config import get_telegram_bot

        # Initialize Telegram Bot
        telegram_bot_instance = get_telegram_bot()
        telegram_bot_thread = threading.Thread(target=telegram_bot_instance.start_polling, daemon=True)
        telegram_bot_thread.start()
        logger.info("🤖 Telegram Bot polling started in background.")

        # Start automation in a separate thread to avoid asyncio conflict
        automation_thread = threading.Thread(target=run_automation, daemon=True)
        automation_thread.start()
        logger.info("🤖 Automation started in background thread.")

        # Keep main thread alive
        while True:
            time.sleep(1)

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
