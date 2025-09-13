# টেলিগ্রাম Bot Setup Guide

## ১. টেলিগ্রাম Bot তৈরি করুন

### Step 1: BotFather এর সাথে কথা বলুন
1. টেলিগ্রামে `@BotFather` খুঁজুন
2. `/newbot` command পাঠান
3. Bot এর নাম দিন (যেমন: "Website Monitor Bot")
4. Bot এর username দিন (যেমন: "website_monitor_bot")
5. BotFather আপনাকে একটি **Bot Token** দেবে

### Step 2: Chat ID খুঁজুন
1. আপনার টেলিগ্রাম চ্যানেল/গ্রুপে যান
2. `@userinfobot` এ message পাঠান
3. এটি আপনাকে **Chat ID** দেবে

## ২. Configuration Setup

### `webhook_config.py` ফাইল খুলুন এবং আপডেট করুন:

```python
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # আপনার Bot Token
TELEGRAM_CHAT_ID = "-1001234567890"  # আপনার Chat ID
```

## ৩. Test করুন

### Test Script চালান:
```bash
python test_telegram.py
```

## ৪. Advanced Automation চালান

```bash
python advanced_automation.py
```

## 📱 Message Format

Bot এই format এ message পাঠাবে:

```
💰 kamkg.com
🔄 Action: amount_update
💵 Amount: 1000.50
⏰ Time: 2024-01-01 12:00:00
```

## 🔧 Troubleshooting

### Bot Token Error:
- Bot Token সঠিক আছে কিনা check করুন
- Bot Token এ কোনো space নেই কিনা দেখুন

### Chat ID Error:
- Chat ID সঠিক আছে কিনা check করুন
- Bot কে channel/group এ admin করুন

### Permission Error:
- Bot কে channel/group এ add করুন
- Bot কে message পাঠানোর permission দিন

## 📞 Support

যদি কোনো সমস্যা হয়, console logs check করুন।
