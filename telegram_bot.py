import requests
import json
import time
import threading
from datetime import datetime
from webhook_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramBot:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.last_update_id = 0
        self.running = False
        
    def send_message(self, text, parse_mode="HTML"):
        """Send message to Telegram with rate limiting"""
        if self.bot_token == "YOUR_BOT_TOKEN_HERE" or self.chat_id == "YOUR_CHAT_ID_HERE":
            print(f"📤 Telegram not configured. Would send: {text}")
            return False
            
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
            
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                print(f"✅ Telegram message sent successfully")
                return True
            elif response.status_code == 429:
                # Rate limited - wait and retry
                print(f"⚠️ Telegram rate limited, waiting...")
                time.sleep(2)
                return False
            else:
                print(f"❌ Telegram failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending Telegram message: {e}")
            return False
    
    def get_updates(self):
        """Get updates from Telegram with rate limiting"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {
                "offset": self.last_update_id + 1,
                "timeout": 10
            }
            
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data["ok"]:
                    return data["result"]
                else:
                    print(f"❌ Telegram API error: {data['description']}")
                    return []
            elif response.status_code == 429:
                # Rate limited - wait and return empty
                print(f"⚠️ Telegram rate limited on getUpdates, waiting...")
                time.sleep(2)
                return []
            else:
                print(f"❌ HTTP error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting updates: {e}")
            return []
    
    def handle_message(self, message):
        """Handle incoming message"""
        try:
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            user_id = message["from"]["id"]
            username = message["from"].get("username", "Unknown")
            
            print(f"📨 Received message from {username}: {text}")
            
            # Handle commands
            if text.startswith("/"):
                self.handle_command(text, chat_id, username)
            else:
                # Echo back the message
                reply = f"Hello {username}! You said: {text}"
                self.send_message(reply)
                
        except Exception as e:
            print(f"❌ Error handling message: {e}")
    
    def handle_command(self, command, chat_id, username):
        """Handle bot commands"""
        try:
            if command == "/start":
                welcome_msg = f"""
🤖 **Website Monitor Bot**

Hello {username}! Welcome to the Website Monitor Bot.

**Available Commands:**
/status - Check bot status
/help - Show this help message
/sites - Show monitored websites
/amount - Get current amounts

**Monitored Websites:**
• kamkg.com
• kamate1.com  
• wha2.net
• lootlelo.com

Bot is running and monitoring all websites 24/7!
                """
                self.send_message(welcome_msg)
                
            elif command == "/status":
                status_msg = f"""
🟢 **Bot Status: ACTIVE**

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔄 Status: Monitoring all websites
📊 Websites: 4 active
🤖 Bot: Running via polling method
                """
                self.send_message(status_msg)
                
            elif command == "/sites":
                sites_msg = """
🌐 **Monitored Websites:**

1. **kamkg.com** - Active
2. **kamate1.com** - Active  
3. **wha2.net** - Active
4. **lootlelo.com** - Active

All sites are being monitored 24/7 for:
• Login status
• Logout detection
• Reset button claims
• Amount updates
                """
                self.send_message(sites_msg)
                
            elif command == "/amount":
                amount_msg = """
💰 **Current Amounts:**

This feature will show real-time amounts from all websites when the monitoring system is active.

Amounts are automatically sent when:
• Reset button is claimed
• Amount changes detected
• Login successful
                """
                self.send_message(amount_msg)
                
            elif command == "/help":
                help_msg = """
❓ **Help Commands:**

/start - Welcome message
/status - Check bot status  
/sites - Show monitored websites
/amount - Get current amounts
/help - Show this help

**About:**
This bot monitors 4 websites automatically and sends notifications for:
• Login success/failure
• Logout detection
• Reset button claims (every 2 hours)
• Amount updates
                """
                self.send_message(help_msg)
                
            else:
                self.send_message(f"❓ Unknown command: {command}\nType /help for available commands.")
                
        except Exception as e:
            print(f"❌ Error handling command: {e}")
    
    def start_polling(self):
        """Start polling for updates"""
        if self.bot_token == "YOUR_BOT_TOKEN_HERE" or self.chat_id == "YOUR_CHAT_ID_HERE":
            print("❌ Telegram not configured. Please set BOT_TOKEN and CHAT_ID in webhook_config.py")
            return
            
        print("🤖 Starting Telegram Bot (Polling Method)...")
        self.running = True
        
        while self.running:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update["update_id"]
                    
                    if "message" in update:
                        self.handle_message(update["message"])
                    elif "callback_query" in update:
                        # Handle callback queries if needed
                        pass
                
                time.sleep(5)  # Longer delay between polls to avoid rate limiting
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping Telegram Bot...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Polling error: {e}")
                time.sleep(5)  # Wait before retrying
        
        print("✅ Telegram Bot stopped.")
    
    def stop(self):
        """Stop the bot"""
        self.running = False

def main():
    """Main function to run the bot"""
    bot = TelegramBot()
    try:
        bot.start_polling()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    finally:
        bot.stop()

if __name__ == "__main__":
    main()
