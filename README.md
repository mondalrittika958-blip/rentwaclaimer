# 🤖 Website Monitor Bot

A 24/7 automation bot that monitors multiple websites for login status, amount tracking, and reset button claims.

## 🌐 Monitored Websites
- kamkg.com
- kamate1.com  
- wha2.net
- lootlelo.com

## ✨ Features
- 🔐 Automatic login to all websites
- 💰 Real-time amount tracking
- 🔄 Reset button claiming (every 2 hours)
- 📱 Telegram notifications
- 🛡️ Popup handling
- ⚡ Sequential monitoring (no threading issues)
- 📊 1-hour monitoring intervals

## 🚀 Local Usage

### Prerequisites
- Python 3.11+
- Chrome/Chromium browser

### Installation
```bash
pip install -r requirements.txt
playwright install chromium
```

### Run Locally
```bash
python run_local.py
```
Or double-click `run_local.bat` on Windows.

## 🌐 Online Deployment (Render)

### Deploy to Render
1. Push code to GitHub
2. Connect to Render
3. Set environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### Configuration Files
- `render.yaml` - Render deployment config
- `requirements.txt` - Python dependencies
- `main.py` - Entry point for online deployment

## 📱 Telegram Integration

### Setup
1. Create a bot with @BotFather
2. Get your bot token
3. Get your chat ID
4. Update `webhook_config.py` or set environment variables

### Commands
- `/start` - Welcome message
- `/status` - Check bot status
- `/sites` - Show monitored websites
- `/amount` - Get current amounts
- `/help` - Show help

## 🔧 Configuration

### Login Credentials
Update in `advanced_automation_playwright.py`:
```python
phone_field.fill("YOUR_PHONE")
password_field.fill("YOUR_PASSWORD")
```

### Monitoring Interval
Default: 1 hour (3600 seconds)
Change in `advanced_automation_playwright.py`:
```python
time.sleep(3600)  # Monitoring interval
```

## 📁 File Structure
```
github/
├── main.py                          # Online entry point
├── run_local.py                     # Local entry point
├── run_local.bat                    # Windows batch file
├── advanced_automation_playwright.py # Main automation logic
├── telegram_bot.py                 # Telegram bot functionality
├── webhook_config.py               # Telegram configuration
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render deployment config
└── README.md                       # This file
```

## 🛠️ Technical Details

### Browser Settings
- Mobile viewport (375x667)
- iPhone user agent
- Headless mode (configurable)
- Custom Chrome flags for stability

### Error Handling
- Automatic retry on login failure
- Popup detection and handling
- Amount validation
- Network timeout handling
- Browser cleanup

### Sequential Monitoring
- No threading issues
- Individual browser instances per site
- Proper resource cleanup
- Stable long-running operation

## 📊 Monitoring Logic

1. **Login Phase**: Navigate to login page, fill credentials, verify success
2. **Amount Tracking**: Extract current amount, send updates on changes
3. **Reset Claiming**: Check for reset button availability every 2 hours
4. **Popup Handling**: Detect and close popups automatically
5. **Status Monitoring**: Verify login status, re-login if needed

## 🔄 Reset Button Strategy

- Multiple XPath selectors for robustness
- Scroll into view before clicking
- JavaScript click fallback
- 2-hour claiming interval
- Amount tracking after reset

## 📱 Notification System

### Telegram Messages
- 💰 Amount updates
- 🎯 Reset button claims
- 🔐 Login status
- ⚠️ Error notifications

### Message Format
```
💰 kamkg.com
🔄 Action: amount_update
💵 Amount: 1500
⏰ Time: 2024-01-01 12:00:00
```

## 🚨 Troubleshooting

### Common Issues
1. **Login failures**: Check credentials in code
2. **Popup blocking**: Verify popup selectors
3. **Amount not found**: Check amount element selectors
4. **Telegram not working**: Verify bot token and chat ID

### Debug Mode
Set `headless=False` in browser launch for visual debugging.

### Logs
All activities are logged with timestamps and emojis for easy monitoring.

## 📝 License
This project is for educational purposes only.

## 🤝 Support
For issues or questions, check the code comments or update configurations as needed.
