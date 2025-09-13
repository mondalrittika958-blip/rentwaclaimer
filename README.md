# 🌐 Website Monitor Bot - 24/7 Automation

A powerful Python automation bot that monitors 4 websites 24/7, handles login/logout, claims reset buttons, and sends real-time updates via Telegram.

## 🚀 Features

### ✅ **Multi-Website Monitoring**
- **kamkg.com** - Primary website
- **kamate1.com** - Secondary website  
- **wha2.net** - Third website
- **lootlelo.com** - Fourth website

### ✅ **Smart Automation**
- Auto login/logout detection
- Popup handling ("I Know" buttons)
- Reset button claiming (every 2 hours)
- Amount tracking and reporting
- Error recovery and retry logic

### ✅ **Telegram Integration**
- Real-time notifications
- Bot commands (`/start`, `/status`)
- Amount updates
- Error reporting

### ✅ **24/7 Operation**
- GitHub + Render deployment
- Auto-restart on errors
- Health check endpoints
- Headless browser mode

## 🛠️ Quick Start

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run locally
python run_local.py
```

### 24/7 Deployment
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy website monitor bot"
git push origin main

# 2. Deploy on Render
# - Connect GitHub repository
# - Use render.yaml configuration
# - Set environment variables
```

## 📁 Project Structure

```
├── 🎯 main.py                          # Production entry point
├── 🏃 run_local.py                     # Local development entry point
├── 🤖 advanced_automation_playwright.py # Core automation logic
├── 📱 telegram_bot.py                  # Telegram bot implementation
├── ⚙️ webhook_config.py                # Configuration & notifications
├── 🔄 async_automation_wrapper.py      # Async wrapper for Playwright
├── 🏥 basic_monitoring.py              # Basic HTTP monitoring
├── 🧪 test_login.py                    # Debug script for login testing
├── 📋 requirements.txt                 # Python dependencies
├── 🚀 render.yaml                      # Render deployment config
├── 🔧 mcp_render.json                  # MCP Render configuration
├── 📖 README.md                        # This file
└── 📱 TELEGRAM_SETUP.md               # Telegram setup guide
```

## 🔧 Configuration

### Environment Variables
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Website Settings
Edit `advanced_automation.py` to modify:
- Login credentials
- Element selectors
- Monitoring intervals
- Reset timing

## 🎯 How It Works

### 1. **Login Process**
- Navigates to login page
- Fills phone number and password
- Handles login button clicks
- Manages popups and errors

### 2. **Monitoring Loop**
- Checks every 5 minutes for amount updates
- Handles popups automatically
- Detects logout and re-logs in
- Claims reset buttons every 2 hours

### 3. **Telegram Notifications**
- Sends amount updates
- Reports login status
- Handles bot commands
- Error notifications

### 4. **Error Handling**
- Auto-retry failed operations
- Graceful error recovery
- Detailed logging
- Service restart on critical errors

## 🌐 Deployment Options

### Option 1: Local Development
```bash
python run_with_bot.py
```

### Option 2: 24/7 Cloud (Recommended)
1. Push to GitHub
2. Deploy on Render
3. Configure environment variables
4. Monitor via health endpoints

## 📊 Monitoring

### Health Check Endpoints
- `GET /health` - Service status
- `GET /` - Bot information

### Logs to Watch
- `🚀 Starting Website Monitor Bot`
- `✅ Successfully logged into`
- `💰 Amount:`
- `📤 Telegram message sent`

## 🆘 Troubleshooting

### Common Issues
1. **Login fails** → Check credentials and selectors
2. **Element not found** → Update XPath selectors  
3. **Telegram not working** → Verify bot token and chat ID
4. **Service stops** → Check Render logs

### Debug Commands
```bash
# Test locally
python main.py

# Check health
curl https://your-app.onrender.com/health

# View logs
# Go to Render dashboard → Logs
```

## 💰 Cost

- **Render Free Tier**: 750 hours/month
- **GitHub**: Free for public repos
- **Total**: $0/month for 24/7 operation

## 🔄 Updates

To update the bot:
1. Make code changes
2. Commit and push to GitHub
3. Render auto-deploys
4. Monitor logs for success

## 📱 Telegram Commands

- `/start` - Welcome message
- `/status` - Bot status
- `/help` - Command list

## 🎉 Success Metrics

- ✅ 4 websites monitored simultaneously
- ✅ Auto login/logout handling
- ✅ Reset button claims every 2 hours
- ✅ Real-time Telegram notifications
- ✅ 24/7 uptime on Render
- ✅ Error recovery and auto-restart

---

**Ready to deploy?** Follow the [GitHub Deployment Guide](GITHUB_DEPLOYMENT.md) for 24/7 operation! 🚀