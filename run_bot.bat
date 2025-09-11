@echo off
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Starting Advanced Automation with Telegram Bot...
echo This will:
echo - Start website automation in background
echo - Start Telegram bot with polling method
echo - Send notifications to your Telegram channel
echo.
echo Make sure to configure your Bot Token and Chat ID in webhook_config.py
echo.
echo Press Ctrl+C to stop
echo.
python run_with_bot.py
echo.
echo Automation and bot stopped!
pause
