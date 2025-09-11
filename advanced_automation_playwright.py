from playwright.sync_api import sync_playwright
import time
import threading
import requests
import json
import os
from datetime import datetime, timedelta
from webhook_config import send_webhook_notification, send_notification_via_polling

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

class AdvancedAutomation:
    def __init__(self):
        self.browser = None
        self.context = None
        self.pages = {}
        self.last_reset_times = {}
        self.running = True
        self.setup_browser()
        
    def setup_browser(self):
        """Setup Playwright browser with multiple pages"""
        self.playwright = sync_playwright().start()
        
        # Launch browser with options
        self.browser = self.playwright.chromium.launch(
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
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Create pages for each website
        for site in WEBSITES:
            page = self.context.new_page()
            self.pages[site["name"]] = page
            print(f"📄 Created page for {site['name']}")
        
        print("🚀 Browser setup completed with 4 pages")
    
    def switch_to_page(self, site_name):
        """Switch to a specific site's page"""
        if site_name in self.pages:
            self.current_page = self.pages[site_name]
            return True
        return False
    
    def login_to_site(self, site_config):
        """Login to a specific site"""
        site_name = site_config["name"]
        print(f"🔐 Logging into {site_name}...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Login attempt {attempt + 1}/{max_retries} for {site_name}")
                
                if not self.switch_to_page(site_name):
                    print(f"❌ Could not switch to {site_name} page")
                    return False
                
                # Navigate to login page
                self.current_page.goto(site_config["url"])
                self.current_page.wait_for_load_state("networkidle")
                time.sleep(3)
                
                # Fill phone number
                try:
                    phone_field = self.current_page.locator(site_config["phone_field"]).first
                    phone_field.fill("8974395024")
                    print(f"📱 Phone entered for {site_name}")
                except Exception as e:
                    print(f"❌ Error filling phone for {site_name}: {e}")
                    continue
                
                # Fill password
                try:
                    password_field = self.current_page.locator(site_config["password_field"]).first
                    password_field.fill("53561106@Tojo")
                    print(f"🔑 Password entered for {site_name}")
                except Exception as e:
                    print(f"❌ Error filling password for {site_name}: {e}")
                    continue
                
                # Click login button
                try:
                    login_button = self.current_page.locator(site_config["login_button"]).first
                    login_button.click()
                    print(f"✅ Login button clicked for {site_name}")
                except Exception as e:
                    print(f"❌ Error clicking login button for {site_name}: {e}")
                    continue
                
                # Wait for page load
                time.sleep(5)
                
                # Handle popup if present
                self.handle_popup_if_present(site_config)
                
                # Navigate to main page
                self.current_page.goto(site_config["main_url"])
                self.current_page.wait_for_load_state("networkidle")
                time.sleep(3)
                
                # Verify login
                current_url = self.current_page.url
                print(f"🔍 Login verification for {site_name} - Current URL: {current_url}")
                
                if "login" not in current_url.lower():
                    print(f"✅ Successfully logged into {site_name}")
                    
                    # Get initial amount
                    amount = self.get_amount(site_config)
                    if amount:
                        print(f"💰 {site_name} amount: {amount}")
                        self.send_amount_update(site_name, amount, "login_success")
                    
                    return True
                else:
                    print(f"❌ Login failed for {site_name}")
                    continue
                    
            except Exception as e:
                print(f"❌ Error logging into {site_name} (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                else:
                    print(f"❌ Failed to login to {site_name} after {max_retries} attempts")
                    return False
        
        return False
    
    def handle_popup_if_present(self, site_config):
        """Handle popup if present during login"""
        site_name = site_config["name"]
        try:
            # Try to find popup with multiple selectors
            popup_selectors = [
                site_config["popup_button"],
                "//*[contains(text(), 'I Know')]",
                "//*[contains(text(), 'I know')]",
                "//*[contains(text(), 'OK')]",
                "//*[contains(text(), 'ok')]",
                "//button[contains(text(), 'I Know')]",
                "//button[contains(text(), 'I know')]",
                "//button[contains(text(), 'OK')]",
                "//button[contains(text(), 'ok')]"
            ]
            
            for selector in popup_selectors:
                try:
                    popup_element = self.current_page.locator(selector).first
                    if popup_element.is_visible():
                        popup_element.click()
                        print(f"📋 Popup handled for {site_name} using selector: {selector}")
                        time.sleep(2)
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling popup for {site_name}: {e}")
            return False
    
    def check_logout(self, site_config):
        """Check if user is logged out by checking for actual logout indicators"""
        site_name = site_config["name"]
        try:
            current_url = self.current_page.url
            print(f"🔍 Checking {site_name} - Current URL: {current_url}")
            
            # Check if we're on login page (actual logout)
            if "login" in current_url.lower() and "pages/login" in current_url:
                print(f"⚠️ {site_name} on login page - Re-logging in...")
                return self.login_to_site(site_config)
            
            # First check if there's a popup that needs to be handled
            popup_handled = self.handle_popup_if_present(site_config)
            if popup_handled:
                print(f"📋 Popup handled for {site_name} during logout check")
            
            # Check if we can access amount element (if not, might be logged out)
            try:
                amount_element = self.current_page.locator(site_config["amount_element"]).first
                if amount_element.is_visible():
                    print(f"✅ {site_name} is logged in and accessible")
                    return True
                else:
                    print(f"⚠️ {site_name} amount element not accessible - might be logged out")
                    return self.login_to_site(site_config)
            except:
                print(f"⚠️ {site_name} amount element not found - might be logged out")
                return self.login_to_site(site_config)
                
        except Exception as e:
            print(f"❌ Error checking logout for {site_name}: {e}")
            return False
    
    def get_amount(self, site_config):
        """Get current amount from the website"""
        site_name = site_config["name"]
        try:
            amount_element = self.current_page.locator(site_config["amount_element"]).first
            amount = amount_element.text_content()
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
    
    def send_amount_update(self, site_name, amount, action="amount_update"):
        """Send amount update notification"""
        try:
            send_notification_via_polling(site_name, amount, action)
        except Exception as e:
            print(f"❌ Error sending notification for {site_name}: {e}")
    
    def claim_reset_button(self, site_config):
        """Claim the reset button"""
        site_name = site_config["name"]
        try:
            print(f"🔄 Attempting to claim reset button for {site_name}")
            
            # Scroll to reset button
            reset_button = self.current_page.locator(site_config["reset_button"]).first
            reset_button.scroll_into_view_if_needed()
            time.sleep(2)
            
            # Try to click reset button
            if reset_button.is_visible():
                reset_button.click()
                print(f"✅ Reset button claimed for {site_name}")
                time.sleep(3)
                
                # Get amount after reset
                amount = self.get_amount(site_config)
                if amount:
                    self.send_amount_update(site_name, amount, "reset_claimed")
                
                return True
            else:
                print(f"⚠️ Reset button not visible for {site_name}")
                return False
                
        except Exception as e:
            print(f"❌ Error claiming reset button for {site_name}: {e}")
            return False
    
    def should_reset(self, site_name):
        """Check if it's time to reset (every 2 hours)"""
        current_time = datetime.now()
        if site_name not in self.last_reset_times:
            self.last_reset_times[site_name] = current_time
            return True
        
        time_diff = current_time - self.last_reset_times[site_name]
        return time_diff >= timedelta(hours=2)
    
    def monitor_site(self, site_config):
        """Monitor a single site continuously"""
        site_name = site_config["name"]
        print(f"👁️ Starting monitoring for {site_name}")
        
        while self.running:
            try:
                if not self.switch_to_page(site_name):
                    print(f"❌ Could not switch to {site_name} page")
                    time.sleep(30)
                    continue
                
                # First handle any popup that might be present
                popup_handled = self.handle_popup_if_present(site_config)
                if popup_handled:
                    print(f"📋 Popup handled for {site_name} during monitoring")
                
                # Check if logged out (only if really needed)
                logout_check = self.check_logout(site_config)
                if not logout_check:
                    print(f"⚠️ {site_name} logout detected, re-logging in...")
                    # Force re-login
                    if self.login_to_site(site_config):
                        print(f"✅ {site_name} re-login successful")
                    else:
                        print(f"❌ {site_name} re-login failed, will retry later")
                        time.sleep(60)
                        continue
                else:
                    print(f"✅ {site_name} is logged in and working normally")
                
                # Check if it's time to reset
                if self.should_reset(site_name):
                    print(f"⏰ Time to reset for {site_name}")
                    self.claim_reset_button(site_config)
                    self.last_reset_times[site_name] = datetime.now()
                
                # Regular amount check
                amount = self.get_amount(site_config)
                if amount:
                    self.send_amount_update(site_name, amount, "amount_check")
                
                # Wait before next check
                time.sleep(300)  # 5 minutes
                
            except Exception as e:
                print(f"❌ Error monitoring {site_name}: {e}")
                time.sleep(60)
    
    def start_monitoring(self):
        """Start monitoring all sites"""
        print("🚀 Starting Advanced Automation with Telegram Bot...")
        
        # Login to all sites first
        for site_config in WEBSITES:
            if self.login_to_site(site_config):
                print(f"✅ {site_config['name']} login successful")
            else:
                print(f"❌ {site_config['name']} login failed")
            time.sleep(2)
        
        # Start monitoring threads
        threads = []
        for site_config in WEBSITES:
            thread = threading.Thread(target=self.monitor_site, args=(site_config,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            print(f"🧵 Started monitoring thread for {site_config['name']}")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("🛑 Stopping automation...")
            self.running = False
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

if __name__ == "__main__":
    automation = AdvancedAutomation()
    automation.start_monitoring()
