#!/usr/bin/env python3
"""
Simple test to send keyboard to telegram
"""
import requests
import json
import time

# Bot configuration
BOT_TOKEN = "8251061362:AAEVeQ36DY-cSDPkjeoSt9065P6FBKQOKHA"
CHANNEL_ID = "-1003095344192"

def test_keyboard():
    """Test sending keyboard"""
    print("🧪 Testing Telegram Keyboard...")
    
    # First get bot info
    try:
        bot_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(bot_url)
        print(f"📱 Bot Info Response: {response.status_code}")
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
        else:
            print(f"❌ Bot token invalid: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error getting bot info: {e}")
        return
    
    # Get updates to see if there are any private messages
    try:
        updates_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        response = requests.get(updates_url)
        print(f"📨 Updates Response: {response.status_code}")
        if response.status_code == 200:
            updates = response.json()
            print(f"📊 Total updates: {len(updates['result'])}")
            
            # Look for private chats
            private_chats = []
            for update in updates['result']:
                if 'message' in update:
                    chat = update['message']['chat']
                    if chat['type'] == 'private':
                        private_chats.append({
                            'chat_id': chat['id'],
                            'username': chat.get('username', 'Unknown'),
                            'first_name': chat.get('first_name', 'Unknown')
                        })
            
            # Remove duplicates
            unique_chats = []
            seen_ids = set()
            for chat in private_chats:
                if chat['chat_id'] not in seen_ids:
                    unique_chats.append(chat)
                    seen_ids.add(chat['chat_id'])
            
            print(f"👤 Private chats found: {len(unique_chats)}")
            for chat in unique_chats:
                print(f"  - {chat['first_name']} (@{chat['username']}) - ID: {chat['chat_id']}")
                
                # Send keyboard to this user
                test_keyboard_to_user(chat['chat_id'])
        else:
            print(f"❌ Failed to get updates: {response.text}")
    except Exception as e:
        print(f"❌ Error getting updates: {e}")

def test_keyboard_to_user(chat_id):
    """Send keyboard to specific user"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        keyboard = {
            "keyboard": [
                [{"text": "🔄 Monitor Now"}, {"text": "📊 Status"}],
                [{"text": "🌐 Sites"}, {"text": "💰 Amounts"}],
                [{"text": "❓ Help"}, {"text": "⏰ Schedule"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False,
            "selective": False
        }
        
        data = {
            "chat_id": chat_id,
            "text": "🤖 **Keyboard Test!**\n\nIf you can see buttons below, the keyboard is working!",
            "parse_mode": "Markdown",
            "reply_markup": json.dumps(keyboard)
        }
        
        response = requests.post(url, data=data)
        print(f"⌨️ Keyboard sent to {chat_id}: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Keyboard sent successfully!")
        else:
            print(f"❌ Failed to send keyboard: {response.text}")
            
    except Exception as e:
        print(f"❌ Error sending keyboard: {e}")

def test_channel_message():
    """Test sending normal message to channel"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHANNEL_ID,
            "text": "🧪 **Channel Test Message**\n\n✅ Bot is working and can send to channel!",
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, data=data)
        print(f"📢 Channel message: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Channel message sent successfully!")
        else:
            print(f"❌ Failed to send to channel: {response.text}")
            
    except Exception as e:
        print(f"❌ Error sending to channel: {e}")

if __name__ == "__main__":
    print("🚀 Starting Telegram Keyboard Test...")
    test_keyboard()
    test_channel_message()
    print("✅ Test completed!")
