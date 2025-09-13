"""
Async wrapper for Playwright automation to avoid asyncio conflicts
"""
import asyncio
import subprocess
import sys
import os
import time
import threading
from datetime import datetime

class AsyncAutomationWrapper:
    def __init__(self):
        self.process = None
        self.running = False
        
    def start_automation(self):
        """Start automation in a separate process"""
        try:
            print("🚀 Starting automation in separate process...")
            
            # Create a simple automation script
            automation_script = """
import asyncio
from playwright.async_api import async_playwright
import time
import requests
import json
from datetime import datetime, timedelta
from webhook_config import send_notification_via_polling

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
        "amount_element": "//uni-text[@class='u-count-num']//span",
        "tutorial_url": "https://kamkg.com/#/pages/tutorial/tutorial"
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
        "amount_element": "//uni-text[@class='u-count-num']//span",
        "tutorial_url": "https://kamate1.com/#/pages/tutorial/tutorial"
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
        "amount_element": "//uni-text[@class='u-count-num']//span",
        "tutorial_url": "https://wha2.net/#/pages/tutorial/tutorial"
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
        "amount_element": "//uni-text[@class='u-count-num']//span",
        "tutorial_url": "https://lootlelo.com/#/pages/tutorial/tutorial"
    }
]

async def run_automation():
    print("🚀 Starting Async Automation...")
    
    async with async_playwright() as p:
        # Launch browser
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
        
        # Login to all sites
        for site_config in WEBSITES:
            try:
                await login_to_site(pages[site_config["name"]], site_config)
            except Exception as e:
                print(f"❌ Error with {site_config['name']}: {e}")
        
        # Keep running
        while True:
            await asyncio.sleep(300)  # Check every 5 minutes
            print("🔄 Automation running...")

async def login_to_site(page, site_config):
    site_name = site_config["name"]
    print(f"🔐 Logging into {site_name}...")
    
    try:
        # Navigate to login page
        await page.goto(site_config["url"])
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        
        # Fill phone number
        phone_field = page.locator(site_config["phone_field"]).first
        await phone_field.fill("8974395024")
        print(f"📱 Phone entered for {site_name}")
        
        # Fill password
        password_field = page.locator(site_config["password_field"]).first
        await password_field.fill("53561106@Tojo")
        print(f"🔑 Password entered for {site_name}")
        
        # Click login button
        login_button = page.locator(site_config["login_button"]).first
        await login_button.click()
        print(f"✅ Login button clicked for {site_name}")
        
        # Wait for page load
        await asyncio.sleep(5)
        
        # Navigate to main page
        await page.goto(site_config["main_url"])
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        
        print(f"✅ Successfully logged into {site_name}")
        
    except Exception as e:
        print(f"❌ Error logging into {site_name}: {e}")

if __name__ == "__main__":
    asyncio.run(run_automation())
"""
            
            # Write the script to a temporary file
            with open("temp_automation.py", "w") as f:
                f.write(automation_script)
            
            # Start the automation process
            self.process = subprocess.Popen([
                sys.executable, "temp_automation.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.running = True
            print("✅ Automation process started")
            
        except Exception as e:
            print(f"❌ Error starting automation: {e}")
    
    def stop_automation(self):
        """Stop the automation process"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.running = False
            print("🛑 Automation process stopped")
    
    def is_running(self):
        """Check if automation is running"""
        return self.running and self.process and self.process.poll() is None
