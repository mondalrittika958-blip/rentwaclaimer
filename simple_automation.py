#!/usr/bin/env python3
"""
Real website monitoring automation with Playwright
"""
import asyncio
import time
import requests
import json
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Website configurations
WEBSITES = [
    {
        "name": "kamkg.com",
        "url": "https://kamkg.com/#/pages/login/index",
        "main_url": "https://kamkg.com",
        "phone_field": "//input[@type='number']",
        "password_field": "//input[@type='password']",
        "login_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view/uni-view/uni-view[4]/uni-button[1]",
        "popup_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/section/uni-view[3]/uni-view/uni-view[3]/uni-view/uni-view/uni-view[1]/uni-view/uni-view[2]/uni-view[3]/uni-view[1]",
        "reset_button": "//uni-button[@class='u-button u-reset-button u-button--square u-button--small w-full font_archive base_font_color']",
        "amount_element": "//uni-text[@class='u-count-num']//span"
    },
    {
        "name": "kamate1.com",
        "url": "https://kamate1.com/#/pages/login/index",
        "main_url": "https://kamate1.com",
        "phone_field": "//input[@type='number']",
        "password_field": "//input[@type='password']",
        "login_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view/uni-view/uni-view[4]/uni-button[1]",
        "popup_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/section/uni-view[3]/uni-view/uni-view[3]/uni-view/uni-view/uni-view[1]/uni-view/uni-view[2]/uni-view[3]/uni-view[1]",
        "reset_button": "//uni-button[@class='u-button u-reset-button u-button--square u-button--small w-full font_archive base_font_color']",
        "amount_element": "//uni-text[@class='u-count-num']//span"
    },
    {
        "name": "wha2.net",
        "url": "https://wha2.net/#/pages/login/index",
        "main_url": "https://wha2.net",
        "phone_field": "//input[@type='number']",
        "password_field": "//input[@type='password']",
        "login_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view/uni-view/uni-view[4]/uni-button[1]",
        "popup_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/section/uni-view[3]/uni-view/uni-view[3]/uni-view/uni-view/uni-view[1]/uni-view/uni-view[2]/uni-view[3]/uni-view[1]",
        "reset_button": "//uni-button[@class='u-button u-reset-button u-button--square u-button--small w-full font_archive base_font_color']",
        "amount_element": "//uni-text[@class='u-count-num']//span"
    },
    {
        "name": "lootlelo.com",
        "url": "https://lootlelo.com/#/pages/login/index",
        "main_url": "https://lootlelo.com",
        "phone_field": "//input[@type='number']",
        "password_field": "//input[@type='password']",
        "login_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view/uni-view/uni-view[4]/uni-button[1]",
        "popup_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/section/uni-view[3]/uni-view/uni-view[3]/uni-view/uni-view/uni-view[1]/uni-view/uni-view[2]/uni-view[3]/uni-view[1]",
        "reset_button": "//uni-button[@class='u-button u-reset-button u-button--square u-button--small w-full font_archive base_font_color']",
        "amount_element": "//uni-text[@class='u-count-num']//span"
    }
]

def send_telegram_message(text):
    """Send message directly to Telegram"""
    try:
        # Get credentials from environment
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "8251061362:AAF0NHiKhVqvx8fMBsVNj9wwAjG4GtKiZk8")
        chat_id = os.getenv("TELEGRAM_CHAT_ID", "-1003095344192")
        
        if bot_token == "YOUR_BOT_TOKEN_HERE" or chat_id == "YOUR_CHAT_ID_HERE":
            print(f"📤 Telegram not configured. Would send: {text}")
            return False
            
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print(f"✅ Telegram message sent successfully")
            return True
        else:
            print(f"❌ Telegram failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")
        return False

async def login_to_site(page, site_config):
    """Login to a specific site with better timeout handling"""
    site_name = site_config["name"]
    print(f"🔐 Logging into {site_name}...")
    
    try:
        # Navigate to login page with longer timeout
        await page.goto(site_config["url"], timeout=60000)
        await page.wait_for_load_state("networkidle", timeout=60000)
        await asyncio.sleep(5)  # Increased wait time
        
        # Wait for elements to be visible with multiple attempts
        try:
            # Try multiple selectors for phone field
            phone_selectors = [
                site_config["phone_field"],
                "input[type='number']",
                "input[placeholder*='phone']",
                "input[placeholder*='mobile']",
                "input[name*='phone']"
            ]
            
            phone_field = None
            for selector in phone_selectors:
                try:
                    phone_field = page.locator(selector).first
                    await phone_field.wait_for(state="visible", timeout=10000)
                    print(f"✅ Found phone field with selector: {selector}")
                    break
                except:
                    continue
            
            if not phone_field:
                print(f"❌ No phone field found for {site_name}")
                return False
                
            await phone_field.fill("8974395024")
            print(f"📱 Phone entered for {site_name}")
        except Exception as e:
            print(f"❌ Phone field error for {site_name}: {e}")
            return False
        
        try:
            # Try multiple selectors for password field
            password_selectors = [
                site_config["password_field"],
                "input[type='password']",
                "input[placeholder*='password']",
                "input[name*='password']"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = page.locator(selector).first
                    await password_field.wait_for(state="visible", timeout=10000)
                    print(f"✅ Found password field with selector: {selector}")
                    break
                except:
                    continue
            
            if not password_field:
                print(f"❌ No password field found for {site_name}")
                return False
                
            await password_field.fill("53561106@Tojo")
            print(f"🔑 Password entered for {site_name}")
        except Exception as e:
            print(f"❌ Password field error for {site_name}: {e}")
            return False
        
        try:
            # Try multiple selectors for login button
            button_selectors = [
                site_config["login_button"],
                "button[type='submit']",
                "button:has-text('Login')",
                "button:has-text('Sign In')",
                "button:has-text('Log In')",
                ".login-button",
                ".btn-login",
                "button"
            ]
            
            login_button = None
            for selector in button_selectors:
                try:
                    login_button = page.locator(selector).first
                    await login_button.wait_for(state="visible", timeout=10000)
                    print(f"✅ Found login button with selector: {selector}")
                    break
                except:
                    continue
            
            if not login_button:
                print(f"❌ No login button found for {site_name}")
                return False
                
            await login_button.click()
            print(f"✅ Login button clicked for {site_name}")
        except Exception as e:
            print(f"❌ Login button error for {site_name}: {e}")
            return False
        
        # Wait for page load with longer timeout
        await asyncio.sleep(8)  # Increased wait time
        
        # Navigate to main page
        try:
            await page.goto(site_config["main_url"], timeout=60000)
            await page.wait_for_load_state("networkidle", timeout=60000)
            await asyncio.sleep(5)
        except Exception as e:
            print(f"⚠️ Main page navigation warning for {site_name}: {e}")
            # Continue anyway, might still work
        
        print(f"✅ Successfully logged into {site_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error logging into {site_name}: {e}")
        return False

async def get_amount(page, site_config):
    """Get current amount from the website"""
    site_name = site_config["name"]
    try:
        amount_element = page.locator(site_config["amount_element"]).first
        amount = await amount_element.text_content()
        if amount:
            amount = amount.strip()
            print(f"💰 {site_name} amount: {amount}")
            return amount
        else:
            print(f"❌ Could not get amount for {site_name}")
            return None
    except Exception as e:
        print(f"❌ Error getting amount for {site_name}: {e}")
        return None

async def check_reset_button(page, site_config):
    """Check if reset button is available"""
    site_name = site_config["name"]
    try:
        reset_button = page.locator(site_config["reset_button"]).first
        is_visible = await reset_button.is_visible()
        if is_visible:
            print(f"🎯 Reset button available for {site_name}")
            return True
        else:
            print(f"ℹ️ No reset button for {site_name}")
            return False
    except Exception as e:
        print(f"❌ Error checking reset button for {site_name}: {e}")
        return False

async def click_reset_button(page, site_config):
    """Click the reset button if available"""
    site_name = site_config["name"]
    try:
        reset_button = page.locator(site_config["reset_button"]).first
        await reset_button.scroll_into_view_if_needed()
        await asyncio.sleep(1)
        
        if await reset_button.is_visible():
            await reset_button.click()
            print(f"✅ Reset button clicked for {site_name}")
            return True
        else:
            print(f"⚠️ Reset button not visible for {site_name}")
            return False
    except Exception as e:
        print(f"❌ Error clicking reset button for {site_name}: {e}")
        return False

async def monitor_site(page, site_config):
    """Monitor a single site"""
    site_name = site_config["name"]
    print(f"👁️ Starting monitoring for {site_name}")
    
    # Login first
    if not await login_to_site(page, site_config):
        print(f"❌ Failed to login to {site_name}")
        # Send failure notification
        send_telegram_message(f"❌ <b>{site_name}</b>\n🔐 Login failed\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return
    
    # Send login success message
    send_telegram_message(f"✅ <b>{site_name}</b>\n🔐 Login successful\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get initial amount
    amount = await get_amount(page, site_config)
    if amount:
        send_telegram_message(f"💰 <b>{site_name}</b>\n💵 Amount: {amount}\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"⚠️ Could not get amount for {site_name}")
    
    # Check for reset button
    if await check_reset_button(page, site_config):
        if await click_reset_button(page, site_config):
            send_telegram_message(f"🎯 <b>{site_name}</b>\n✅ Reset button claimed\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Get amount after reset
            await asyncio.sleep(3)
            new_amount = await get_amount(page, site_config)
            if new_amount:
                send_telegram_message(f"💰 <b>{site_name}</b>\n💵 New Amount: {new_amount}\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Keep monitoring this site
    print(f"🔄 Continuing to monitor {site_name}...")
    while True:
        try:
            # Check amount every 5 minutes
            await asyncio.sleep(300)  # 5 minutes
            
            amount = await get_amount(page, site_config)
            if amount:
                send_telegram_message(f"💰 <b>{site_name}</b>\n💵 Amount Update: {amount}\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check for reset button every 2 hours
            if await check_reset_button(page, site_config):
                if await click_reset_button(page, site_config):
                    send_telegram_message(f"🎯 <b>{site_name}</b>\n✅ Reset button claimed\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    await asyncio.sleep(3)
                    new_amount = await get_amount(page, site_config)
                    if new_amount:
                        send_telegram_message(f"💰 <b>{site_name}</b>\n💵 New Amount: {new_amount}\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"❌ Error monitoring {site_name}: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying

async def monitor_site_safe(page, site_config):
    """Safe monitoring wrapper that handles errors gracefully"""
    site_name = site_config["name"]
    try:
        await monitor_site(page, site_config)
    except Exception as e:
        print(f"❌ Error in monitor_site_safe for {site_name}: {e}")
        # Send error notification
        send_telegram_message(f"❌ <b>{site_name}</b>\n⚠️ Monitoring error: {str(e)[:100]}\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

async def run_automation():
    """Real website monitoring automation"""
    print("🚀 Starting Real Website Monitoring...")
    
    try:
        from playwright.async_api import async_playwright
        print("✅ Playwright imported successfully")
    except ImportError:
        print("❌ Playwright not installed. Installing...")
        import subprocess
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            from playwright.async_api import async_playwright
            print("✅ Playwright installed successfully")
        except Exception as e:
            print(f"❌ Failed to install Playwright: {e}")
            # Fallback to simple monitoring without browser
            await run_simple_monitoring()
            return
    
    # Send startup message
    send_telegram_message("🚀 <b>Website Monitor Started</b>\n🌐 Monitoring 4 websites\n⏰ Time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Try to install browsers if not available
    try:
        import subprocess
        print("🔧 Checking Playwright browsers...")
        result = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ Playwright browsers installed successfully")
        else:
            print(f"⚠️ Browser installation had issues: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Could not install browsers: {e}")
        print("🔄 Will try to run anyway...")
    
    try:
        async with async_playwright() as p:
            # Check if Chromium is available
            try:
                print("🔍 Checking Chromium availability...")
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--allow-running-insecure-content',
                        '--disable-extensions',
                        '--disable-gpu',
                        '--window-size=1920,1080'
                    ]
                )
                print("✅ Chromium launched successfully")
            except Exception as browser_error:
                print(f"❌ Chromium launch failed: {browser_error}")
                if "Executable doesn't exist" in str(browser_error):
                    print("🔄 Chromium not found, falling back to simple monitoring...")
                    await run_simple_monitoring()
                    return
                else:
                    raise browser_error
        
            # Create context
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # Create pages for each website
            pages = {}
            for site in WEBSITES:
                page = await context.new_page()
                pages[site["name"]] = page
                print(f"📄 Created page for {site['name']}")
            
            # Monitor all sites with individual error handling
            tasks = []
            for site_config in WEBSITES:
                task = asyncio.create_task(monitor_site_safe(pages[site_config["name"]], site_config))
                tasks.append(task)
            
            # Wait for all monitoring tasks
            await asyncio.gather(*tasks, return_exceptions=True)
            
            await browser.close()
            
    except Exception as e:
        print(f"❌ Browser automation failed: {e}")
        print("🔄 Falling back to simple monitoring...")
        await run_simple_monitoring()

async def run_simple_monitoring():
    """Fallback monitoring without browser automation"""
    print("🔄 Running simple monitoring without browser...")
    
    # Import and run basic monitoring
    try:
        import subprocess
        print("🔄 Starting basic monitoring as fallback...")
        subprocess.run([sys.executable, "basic_monitoring.py"])
    except Exception as e:
        print(f"❌ Basic monitoring failed: {e}")
        # Ultimate fallback - just send periodic messages
        send_telegram_message("⚠️ <b>Fallback Monitor Started</b>\n🌐 Browser automation not available\n📱 Sending periodic updates\n⏰ Time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        counter = 0
        while True:
            try:
                counter += 1
                print(f"🔄 Fallback monitoring running... (cycle {counter})")
                
                # Send periodic update every 5 minutes
                if counter % 5 == 0:
                    message = f"🤖 <b>Fallback Monitor Update #{counter//5}</b>\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n🔄 Status: Running without browser automation\n🌐 Websites: kamkg.com, kamate1.com, wha2.net, lootlelo.com"
                    send_telegram_message(message)
                    print(f"📤 Sent fallback update: {message}")
                
                await asyncio.sleep(60)  # Wait 1 minute between cycles
                
            except Exception as e:
                print(f"❌ Error in fallback monitoring loop: {e}")
                await asyncio.sleep(30)  # Wait 30 seconds before retrying

if __name__ == "__main__":
    try:
        asyncio.run(run_automation())
    except KeyboardInterrupt:
        print("🛑 Automation stopped by user")
    except Exception as e:
        print(f"❌ Fatal error in automation: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
