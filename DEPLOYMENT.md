# 🚀 Deployment Guide

## Manual GitHub Upload

### Step 1: Prepare Files
All files are ready for upload:
- ✅ `main.py` - Production entry point
- ✅ `run_local.py` - Local development
- ✅ `advanced_automation_playwright.py` - Core automation
- ✅ `telegram_bot.py` - Telegram bot
- ✅ `webhook_config.py` - Configuration
- ✅ `requirements.txt` - Dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `.gitignore` - Git ignore rules

### Step 2: Upload to GitHub
1. Go to your GitHub repository
2. Upload all files from the local folder
3. Commit with message: "Deploy website monitor bot"

### Step 3: Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Use these settings:

**Build Command:**
```bash
pip install -r requirements.txt && playwright install chromium
```

**Start Command:**
```bash
python main.py
```

**Environment Variables:**
```
TELEGRAM_BOT_TOKEN=8251061362:AAF0NHiKhVqvx8fMBsVNj9wwAjG4GtKiZk8
TELEGRAM_CHAT_ID=-1003095344192
PYTHON_VERSION=3.9.18
PLAYWRIGHT_BROWSERS_PATH=0
```

### Step 4: Monitor
- Check logs in Render dashboard
- Monitor Telegram notifications
- Verify website monitoring

## Local Testing
```bash
# Test locally before upload
python run_local.py
```

## Troubleshooting
- Check Render logs for errors
- Verify environment variables
- Test Telegram bot token
- Check website accessibility
