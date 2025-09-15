# Telegram Bot Configuration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables or use defaults
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8251061362:AAEVeQ36DY-cSDPkjeoSt9065P6FBKQOKHA")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1003095344192")

# Debug info
print(f"🔧 Bot Token: {TELEGRAM_BOT_TOKEN[:10]}...")
print(f"🔧 Chat ID: {TELEGRAM_CHAT_ID}")

def send_telegram_message(site_name, amount, action="amount_update"):
    """
    Send notification to Telegram channel
    
    Args:
        site_name (str): Name of the website
        amount (str): Amount value
        action (str): Type of action (amount_update, reset_claimed, etc.)
    """
    import requests
    import json
    from datetime import datetime
    
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print(f"📤 Telegram not configured. Would send: {site_name} - {amount}")
        return
    
    try:
        # Create message based on action
        if action == "login_required":
            emoji = "🔐"
            message = f"{emoji} **{site_name}**\n"
            message += f"⚠️ Login Required\n"
            message += f"🌐 Website requires authentication\n"
            message += f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            emoji = "💰" if action == "amount_update" else "🎯"
            message = f"{emoji} **{site_name}**\n"
            message += f"🔄 Action: {action}\n"
            message += f"💵 Amount: {amount}\n"
            message += f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Send to Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"✅ Telegram message sent successfully for {site_name}")
        else:
            print(f"❌ Telegram failed for {site_name}: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error sending Telegram message for {site_name}: {e}")

def send_webhook_notification(site_name, amount, action="amount_update"):
    """
    Send notification to webhook (Telegram)
    
    Args:
        site_name (str): Name of the website
        amount (str): Amount value
        action (str): Type of action (amount_update, reset_claimed, etc.)
    """
    send_telegram_message(site_name, amount, action)

# Global bot instance for polling
_telegram_bot = None

def get_telegram_bot():
    """Get or create Telegram bot instance"""
    global _telegram_bot
    if _telegram_bot is None:
        from telegram_bot import TelegramBot
        _telegram_bot = TelegramBot()
    return _telegram_bot

def send_notification_via_polling(site_name, amount, action="amount_update"):
    """
    Send notification via polling method
    
    Args:
        site_name (str): Name of the website
        amount (str): Amount value
        action (str): Type of action (amount_update, reset_claimed, etc.)
    """
    from datetime import datetime
    bot = get_telegram_bot()
    
    # Create message
    emoji = "💰" if action == "amount_update" else "🎯" if action == "reset_claimed" else "🔐"
    message = f"{emoji} {site_name}\n"
    message += f"🔄 Action: {action}\n"
    message += f"💵 Amount: {amount}\n"
    message += f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return bot.send_message(message, parse_mode="HTML")

# Example usage:
# send_webhook_notification("kamkg.com", "1000", "amount_update")
