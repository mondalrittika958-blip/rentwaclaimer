import requests
import json
import time
import threading
from datetime import datetime
from webhook_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from advanced_automation_playwright import AdvancedAutomation

class TelegramBot:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.last_update_id = 0
        self.running = False
        self.automation = None
        
        # Debug info
        print(f"🤖 Telegram Bot initialized")
        print(f"📱 Bot Token: {self.bot_token[:10]}...")
        print(f"💬 Chat ID: {self.chat_id}")
    
    def set_automation(self, automation):
        """Set automation instance for manual monitoring"""
        self.automation = automation
        
    def send_message(self, text, parse_mode="HTML", reply_markup=None):
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
            
            if reply_markup:
                data["reply_markup"] = reply_markup
            
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                print(f"✅ Telegram message sent successfully")
                return True
            elif response.status_code == 429:
                # Rate limited - wait much longer and retry
                print(f"⚠️ Telegram rate limited (429), waiting 60 seconds...")
                time.sleep(60)
                return False
            elif response.status_code == 409:
                # Conflict - webhook vs polling conflict
                print(f"⚠️ Telegram conflict (409), waiting 30 seconds...")
                time.sleep(30)
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
                # Rate limited - wait much longer and return empty
                print(f"⚠️ Telegram rate limited (429) on getUpdates, waiting 120 seconds...")
                time.sleep(120)
                return []
            elif response.status_code == 409:
                # Conflict - webhook vs polling conflict
                print(f"⚠️ Telegram conflict (409) on getUpdates, waiting 60 seconds...")
                time.sleep(60)
                return []
            else:
                print(f"❌ HTTP error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting updates: {e}")
            return []
    
    def get_main_menu(self):
        """Get main menu keyboard"""
        keyboard = {
            "keyboard": [
                [{"text": "🔄 Monitor Now"}, {"text": "📊 Status"}],
                [{"text": "🌐 Sites"}, {"text": "💰 Amounts"}],
                [{"text": "❓ Help"}, {"text": "⏰ Schedule"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
        return keyboard

    def handle_message(self, message):
        """Handle incoming message"""
        try:
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            user_id = message["from"]["id"]
            username = message["from"].get("username", "Unknown")
            
            print(f"📨 Received message from {username}: {text}")
            
            # Handle commands and menu buttons
            if text.startswith("/"):
                self.handle_command(text, chat_id, username)
            elif text == "🔄 Monitor Now":
                self.handle_manual_monitor(chat_id, username)
            elif text == "📊 Status":
                self.handle_status(chat_id, username)
            elif text == "🌐 Sites":
                self.handle_sites(chat_id, username)
            elif text == "💰 Amounts":
                self.handle_amounts(chat_id, username)
            elif text == "❓ Help":
                self.handle_help(chat_id, username)
            elif text == "⏰ Schedule":
                self.handle_schedule(chat_id, username)
            else:
                # Show main menu
                self.send_message("🤖 Choose an option from the menu below:", reply_markup=self.get_main_menu())
                
        except Exception as e:
            print(f"❌ Error handling message: {e}")
    
    def handle_manual_monitor(self, chat_id, username):
        """Handle manual monitoring request"""
        try:
            if not self.automation:
                self.send_message("❌ Automation not available. Please try again later.")
                return
            
            self.send_message("🔄 Starting manual monitoring... Please wait...")
            
            # Run manual monitoring in a separate thread to avoid blocking
            def run_manual_monitor():
                try:
                    self.automation.manual_monitor_all()
                    self.send_message("✅ Manual monitoring completed!")
                except Exception as e:
                    self.send_message(f"❌ Manual monitoring failed: {e}")
            
            monitor_thread = threading.Thread(target=run_manual_monitor, daemon=True)
            monitor_thread.start()
            
        except Exception as e:
            print(f"❌ Error in manual monitor: {e}")
            self.send_message("❌ Error starting manual monitoring.")

    def handle_status(self, chat_id, username):
        """Handle status request"""
        try:
            status_msg = f"""
🟢 **Bot Status: ACTIVE**

⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔄 Status: Monitoring all websites
📊 Websites: 4 active
🤖 Bot: Running via polling method
⏰ Schedule: Every hour at 5 minutes past (12:05, 1:05, 2:05...)
            """
            self.send_message(status_msg, reply_markup=self.get_main_menu())
        except Exception as e:
            print(f"❌ Error in status: {e}")

    def handle_sites(self, chat_id, username):
        """Handle sites request"""
        try:
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
            self.send_message(sites_msg, reply_markup=self.get_main_menu())
        except Exception as e:
            print(f"❌ Error in sites: {e}")

    def handle_amounts(self, chat_id, username):
        """Handle amounts request"""
        try:
            amount_msg = """
💰 **Current Amounts:**

This feature will show real-time amounts from all websites when the monitoring system is active.

Amounts are automatically sent when:
• Reset button is claimed
• Amount changes detected
• Login successful
            """
            self.send_message(amount_msg, reply_markup=self.get_main_menu())
        except Exception as e:
            print(f"❌ Error in amounts: {e}")

    def handle_help(self, chat_id, username):
        """Handle help request"""
        try:
            help_msg = """
❓ **Help & Commands:**

**Menu Buttons:**
🔄 Monitor Now - Start monitoring immediately
📊 Status - Check bot status
🌐 Sites - Show monitored websites
💰 Amounts - Get current amounts
❓ Help - Show this help
⏰ Schedule - Show monitoring schedule

**About:**
This bot monitors 4 websites automatically and sends notifications for:
• Login success/failure
• Logout detection
• Reset button claims (every hour at 5 minutes past)
• Amount updates

**Schedule:**
Monitoring happens every hour at 5 minutes past:
12:05, 1:05, 2:05, 3:05... 24/7
            """
            self.send_message(help_msg, reply_markup=self.get_main_menu())
        except Exception as e:
            print(f"❌ Error in help: {e}")

    def handle_schedule(self, chat_id, username):
        """Handle schedule request"""
        try:
            schedule_msg = """
⏰ **Monitoring Schedule:**

🕐 **Bangladesh Time (BST):**
• 12:05 AM - Morning monitoring
• 1:05 AM - Night monitoring
• 2:05 AM - Night monitoring
• ... (every hour at 5 minutes past)
• 11:05 PM - Evening monitoring

🔄 **Manual Monitoring:**
• Use "🔄 Monitor Now" button anytime
• Immediate monitoring of all 4 websites
• Results sent to Telegram

📊 **Automatic Notifications:**
• Login success/failure
• Amount updates
• Reset button claims
• System status updates
            """
            self.send_message(schedule_msg, reply_markup=self.get_main_menu())
        except Exception as e:
            print(f"❌ Error in schedule: {e}")

    def handle_command(self, command, chat_id, username):
        """Handle bot commands"""
        try:
            if command == "/start":
                welcome_msg = f"""
🤖 **Website Monitor Bot**

Hello {username}! Welcome to the Website Monitor Bot.

**Use the menu buttons below to control the bot:**

🔄 **Monitor Now** - Start monitoring immediately
📊 **Status** - Check bot status
🌐 **Sites** - Show monitored websites
💰 **Amounts** - Get current amounts
❓ **Help** - Show help information
⏰ **Schedule** - Show monitoring schedule

**Monitored Websites:**
• kamkg.com
• kamate1.com  
• wha2.net
• lootlelo.com

Bot is running and monitoring all websites 24/7!
                """
                self.send_message(welcome_msg, reply_markup=self.get_main_menu())
                
            elif command == "/status":
                self.handle_status(chat_id, username)
                
            elif command == "/sites":
                self.handle_sites(chat_id, username)
                
            elif command == "/amount":
                self.handle_amounts(chat_id, username)
                
            elif command == "/help":
                self.handle_help(chat_id, username)
                
            elif command == "/monitor":
                self.handle_manual_monitor(chat_id, username)
                
            elif command == "/schedule":
                self.handle_schedule(chat_id, username)
                
            else:
                self.send_message(f"❓ Unknown command: {command}\nUse the menu buttons below or type /help for available commands.", reply_markup=self.get_main_menu())
                
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
                
                time.sleep(30)  # Much longer delay between polls to avoid rate limiting
                
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
