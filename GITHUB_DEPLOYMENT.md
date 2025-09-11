# GitHub + Render 24/7 Deployment Guide

## 🚀 Step 1: GitHub Repository Setup

### 1.1 Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `website-monitor-bot`
3. Make it **Public** (required for free Render)
4. Add description: "24/7 Website Monitor Bot with Telegram Integration"

### 1.2 Upload Code to GitHub
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Website Monitor Bot"

# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/website-monitor-bot.git

# Push to GitHub
git push -u origin main
```

## 🌐 Step 2: Render Deployment

### 2.1 Connect to Render
1. Go to [Render](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository

### 2.2 Configure Render Service
- **Name**: `website-monitor-bot`
- **Environment**: `Python 3.11.9`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt && playwright install --with-deps chromium`
- **Start Command**: `python main.py`

### 2.3 Environment Variables
Add these in Render dashboard:
- `TELEGRAM_BOT_TOKEN`: `8251061362:AAF0NHiKhVqvx8fMBsVNj9wwAjG4GtKiZk8`
- `TELEGRAM_CHAT_ID`: `-1003095344192`
- `PYTHON_VERSION`: `3.11.0`

### 2.4 Deploy
1. Click "Create Web Service"
2. Wait for build to complete (5-10 minutes)
3. Check logs for any errors

## 📱 Step 3: Test Deployment

### 3.1 Check Health
Visit: `https://your-app-name.onrender.com/health`
Should return: `{"status": "healthy"}`

### 3.2 Check Bot Status
Visit: `https://your-app-name.onrender.com/`
Should return: `{"message": "Website Monitor Bot is running"}`

### 3.3 Test Telegram
Send `/start` to your bot
Should receive welcome message

## 🔧 Step 4: Monitor & Maintain

### 4.1 View Logs
- Go to Render dashboard
- Click on your service
- View "Logs" tab for real-time monitoring

### 4.2 Update Code
```bash
# Make changes to code
git add .
git commit -m "Update: description of changes"
git push origin main

# Render will automatically redeploy
```

### 4.3 Restart Service
- Go to Render dashboard
- Click "Manual Deploy" → "Deploy latest commit"

## 🎯 Features

### ✅ 24/7 Operation
- Runs continuously on Render
- Auto-restart on errors
- Health check endpoint

### ✅ Telegram Integration
- Real-time notifications
- Bot commands support
- Amount updates

### ✅ Website Monitoring
- 4 websites: kamkg.com, kamate1.com, wha2.net, lootlelo.com
- Auto login/logout detection
- Reset button claims (every 2 hours)
- Amount tracking

### ✅ Auto Setup
- ChromeDriver auto-download
- Environment configuration
- Headless browser mode

## 🆘 Troubleshooting

### Common Issues:
1. **Build fails**: Check Python version compatibility
2. **ChromeDriver error**: Verify platform detection
3. **Telegram not working**: Check bot token and chat ID
4. **Service stops**: Check Render logs for errors

### Debug Commands:
```bash
# Check service status
curl https://your-app-name.onrender.com/health

# View recent logs
# Go to Render dashboard → Logs
```

## 📊 Monitoring

### Health Check Endpoints:
- `/health` - Service health status
- `/` - Bot status and info

### Logs to Watch:
- `🚀 Starting Website Monitor Bot`
- `✅ Successfully logged into`
- `💰 Amount:`
- `📤 Telegram message sent successfully`

## 🔄 Updates

To update the bot:
1. Make changes to code
2. Commit and push to GitHub
3. Render auto-deploys
4. Monitor logs for success

## 💰 Cost

- **Render Free Tier**: 750 hours/month
- **GitHub**: Free for public repos
- **Total Cost**: $0/month

Perfect for 24/7 operation!
