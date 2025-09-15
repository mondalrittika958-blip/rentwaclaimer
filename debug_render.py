#!/usr/bin/env python3
"""
Debug script specifically for Render deployment
"""
import time
import requests
from webhook_config import TELEGRAM_BOT_TOKEN, USER_CHAT_ID

def debug_render():
    """Debug Render-specific issues"""
    print("🔍 RENDER DEBUG STARTED")
    print(f"⏰ Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Token: {TELEGRAM_BOT_TOKEN[:15]}...")
    print(f"👤 User Chat: {USER_CHAT_ID}")
    
    # Test 1: Bot API connectivity
    print("\n🧪 TEST 1: Bot API Connectivity")
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        print(f"📡 API Response: {response.status_code}")
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
        else:
            print(f"❌ API Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ API Connection failed: {e}")
        return
    
    # Test 2: Send message to user
    print("\n🧪 TEST 2: Send Message to User")
    try:
        send_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        message = f"🔍 **RENDER DEBUG**\n⏰ {time.strftime('%Y-%m-%d %H:%M:%S')}\n🚀 Bot is alive on Render!"
        
        data = {
            "chat_id": USER_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(send_url, json=data, timeout=10)
        print(f"📤 Send Response: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Message sent to user")
        else:
            print(f"❌ Send Error: {response.text}")
    except Exception as e:
        print(f"❌ Send failed: {e}")
    
    # Test 3: Get recent updates
    print("\n🧪 TEST 3: Get Recent Updates")
    try:
        updates_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
        response = requests.get(updates_url, timeout=10)
        print(f"📨 Updates Response: {response.status_code}")
        if response.status_code == 200:
            updates = response.json()
            print(f"📊 Updates found: {len(updates['result'])}")
            if updates['result']:
                last_update = updates['result'][-1]
                if 'message' in last_update:
                    msg = last_update['message']
                    text = msg.get('text', 'No text')
                    username = msg['from'].get('username', 'Unknown')
                    print(f"📩 Last message: {username} -> '{text}'")
        else:
            print(f"❌ Updates Error: {response.text}")
    except Exception as e:
        print(f"❌ Updates failed: {e}")
    
    print(f"\n✅ RENDER DEBUG COMPLETED")

if __name__ == "__main__":
    debug_render()
