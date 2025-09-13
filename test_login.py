#!/usr/bin/env python3
"""
Test script to debug login issues
"""
import asyncio
import sys
import os
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
    },
    {
        "name": "kamate1.com", 
        "url": "https://kamate1.com/#/pages/login/index",
        "main_url": "https://kamate1.com",
        "phone_field": "//input[@type='number']",
        "password_field": "//input[@type='password']",
        "login_button": "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[2]/uni-view/uni-view/uni-view[4]/uni-button[1]",
    }
]

async def test_site_login(site_config):
    """Test login for a specific site with detailed debugging"""
    site_name = site_config["name"]
    print(f"\n🔍 Testing {site_name}...")
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=False,  # Show browser for debugging
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
            
            page = await context.new_page()
            
            # Navigate to login page
            print(f"🌐 Navigating to {site_config['url']}...")
            await page.goto(site_config["url"], timeout=60000)
            await page.wait_for_load_state("networkidle", timeout=60000)
            await asyncio.sleep(5)
            
            # Take screenshot
            await page.screenshot(path=f"{site_name}_login_page.png")
            print(f"📸 Screenshot saved: {site_name}_login_page.png")
            
            # Check what elements are available
            print(f"🔍 Looking for phone field: {site_config['phone_field']}")
            phone_elements = await page.locator(site_config["phone_field"]).count()
            print(f"📱 Found {phone_elements} phone field(s)")
            
            print(f"🔍 Looking for password field: {site_config['password_field']}")
            password_elements = await page.locator(site_config["password_field"]).count()
            print(f"🔑 Found {password_elements} password field(s)")
            
            print(f"🔍 Looking for login button: {site_config['login_button']}")
            login_elements = await page.locator(site_config["login_button"]).count()
            print(f"🔘 Found {login_elements} login button(s)")
            
            # Try alternative selectors
            print(f"🔍 Trying alternative selectors...")
            
            # Alternative phone selectors
            alt_phone_selectors = [
                "input[type='number']",
                "input[placeholder*='phone']",
                "input[placeholder*='mobile']",
                "input[name*='phone']",
                "input[name*='mobile']"
            ]
            
            for selector in alt_phone_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"✅ Found {count} element(s) with selector: {selector}")
            
            # Alternative password selectors
            alt_password_selectors = [
                "input[type='password']",
                "input[placeholder*='password']",
                "input[name*='password']"
            ]
            
            for selector in alt_password_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"✅ Found {count} element(s) with selector: {selector}")
            
            # Alternative button selectors
            alt_button_selectors = [
                "button[type='submit']",
                "button:has-text('Login')",
                "button:has-text('Sign In')",
                "button:has-text('Log In')",
                ".login-button",
                ".btn-login"
            ]
            
            for selector in alt_button_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"✅ Found {count} element(s) with selector: {selector}")
            
            # Get page content for analysis
            content = await page.content()
            print(f"📄 Page content length: {len(content)} characters")
            
            # Look for specific text patterns
            if "login" in content.lower():
                print("✅ Page contains 'login' text")
            if "phone" in content.lower():
                print("✅ Page contains 'phone' text")
            if "password" in content.lower():
                print("✅ Page contains 'password' text")
            
            await browser.close()
            print(f"✅ Test completed for {site_name}")
            
    except Exception as e:
        print(f"❌ Error testing {site_name}: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Run tests for all sites"""
    print("🚀 Starting login debugging tests...")
    
    for site_config in WEBSITES:
        await test_site_login(site_config)
        await asyncio.sleep(2)  # Wait between tests
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
