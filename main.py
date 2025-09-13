#!/usr/bin/env python3
"""
Main entry point for the automation bot
This file is used for Render deployment
"""

import os
import sys
from advanced_automation_playwright import AdvancedAutomation

def main():
    """Main function to start the automation"""
    print("🚀 Starting Automation Bot...")
    print("📱 Telegram Bot Integration: Enabled")
    print("⏰ Monitoring Interval: 1 hour")
    print("🌐 Websites: kamkg.com, kamate1.com, wha2.net, lootlelo.com")
    
    try:
        # Create automation instance
        automation = AdvancedAutomation()
        
        # Start monitoring
        automation.start_monitoring()
        
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
