#!/usr/bin/env python3
"""
Basic monitoring without Playwright - uses HTTP requests
"""
import time
import requests
import json
import os
import sys
from datetime import datetime

def send_telegram_message(text):
    """Send message directly to Telegram"""
    try:
        # Get credentials from environment
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "8251061362:AAF0NHiKhVqvx8fMBsVNj9wwAjG4GtKiZk8")
        chat_id = os.getenv("TELEGRAM_CHAT_ID", "-1003095344192")
        
        if bot_token == "YOUR_BOT_TOKEN_HERE" or chat_id == "YOUR_CHAT_ID_HERE":
            print(f"📤 Telegram not configured. Would send: {text}")
            return False
            
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print(f"✅ Telegram message sent successfully")
            return True
        else:
            print(f"❌ Telegram failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")
        return False

def check_website_status(url, name):
    """Check if website is accessible"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {name} is accessible")
            return True
        else:
            print(f"⚠️ {name} returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name} is not accessible: {e}")
        return False

def run_basic_monitoring():
    """Basic website monitoring without browser automation"""
    print("🚀 Starting Basic Website Monitoring...")
    
    # Website list
    websites = [
        {"name": "kamkg.com", "url": "https://kamkg.com"},
        {"name": "kamate1.com", "url": "https://kamate1.com"},
        {"name": "wha2.net", "url": "https://wha2.net"},
        {"name": "lootlelo.com", "url": "https://lootlelo.com"}
    ]
    
    # Send startup message
    send_telegram_message("🚀 <b>Basic Website Monitor Started</b>\n🌐 Monitoring 4 websites\n📡 Using HTTP requests\n⏰ Time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Check all websites
    accessible_sites = []
    for site in websites:
        if check_website_status(site["url"], site["name"]):
            accessible_sites.append(site["name"])
    
    # Send status report
    if accessible_sites:
        status_msg = f"📊 <b>Website Status Report</b>\n✅ Accessible: {', '.join(accessible_sites)}\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        status_msg = f"⚠️ <b>Website Status Report</b>\n❌ No websites accessible\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    send_telegram_message(status_msg)
    
    # Keep running and send periodic updates
    counter = 0
    while True:
        try:
            counter += 1
            print(f"🔄 Basic monitoring running... (cycle {counter})")
            
            # Send periodic update every 10 minutes
            if counter % 10 == 0:
                # Re-check websites
                accessible_sites = []
                for site in websites:
                    if check_website_status(site["url"], site["name"]):
                        accessible_sites.append(site["name"])
                
                if accessible_sites:
                    message = f"📊 <b>Periodic Status Update #{counter//10}</b>\n✅ Accessible: {', '.join(accessible_sites)}\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n🔄 Status: Monitoring websites"
                else:
                    message = f"⚠️ <b>Periodic Status Update #{counter//10}</b>\n❌ No websites accessible\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n🔄 Status: Monitoring websites"
                
                send_telegram_message(message)
                print(f"📤 Sent periodic update: {message}")
            
            time.sleep(60)  # Wait 1 minute between cycles
            
        except Exception as e:
            print(f"❌ Error in basic monitoring loop: {e}")
            time.sleep(30)  # Wait 30 seconds before retrying

if __name__ == "__main__":
    try:
        run_basic_monitoring()
    except KeyboardInterrupt:
        print("🛑 Basic monitoring stopped by user")
    except Exception as e:
        print(f"❌ Fatal error in basic monitoring: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
