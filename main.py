#!/usr/bin/env python3
"""
Main entry point for the Website Monitor Bot
This is the production version that runs on Render
"""

import time
import logging
from advanced_automation_playwright import AdvancedAutomation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to run automation"""
    try:
        logger.info("🚀 Starting Website Monitor Bot...")
        logger.info(f"⏰ Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Create automation instance
        automation = AdvancedAutomation()
        
        # Start monitoring
        automation.start_monitoring()
        
    except KeyboardInterrupt:
        logger.info("🛑 Automation stopped by user")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
