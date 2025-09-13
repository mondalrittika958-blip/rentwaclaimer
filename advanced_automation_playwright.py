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
        self.last_reset_times = {}
        self.running = True
        print("🚀 Automation initialized, browsers will be created per thread")
    
    # Removed switch_to_page method as each thread has its own context
    
    def login_to_site(self, site_config):
        """Login to a specific site"""
        site_name = site_config["name"]
        print(f"🔐 Logging into {site_name}...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Login attempt {attempt + 1}/{max_retries} for {site_name}")
                
                # Navigate to login page (current_page is set in monitor_site)
                try:
                    self.current_page.goto(site_config["url"], timeout=60000)
                    
                    # Wait for page load with fallback
                    try:
                        self.current_page.wait_for_load_state("networkidle", timeout=30000)
                    except:
                        print(f"⚠️ Network idle timeout, using domcontentloaded")
                        self.current_page.wait_for_load_state("domcontentloaded", timeout=15000)
                    
                    time.sleep(3)
                except Exception as e:
                    print(f"❌ Navigation error in login: {e}")
                    continue
                
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
                
                # Navigate to main page only if not already there
                current_url = self.current_page.url
                if site_config["main_url"] not in current_url:
                    try:
                        self.current_page.goto(site_config["main_url"], timeout=60000)
                        try:
                            self.current_page.wait_for_load_state("networkidle", timeout=30000)
                        except:
                            print(f"⚠️ Network idle timeout for main page, using domcontentloaded")
                            self.current_page.wait_for_load_state("domcontentloaded", timeout=15000)
                        time.sleep(3)
                    except Exception as e:
                        print(f"❌ Main page navigation error: {e}")
                        # Continue anyway, might still work
                
                # Verify login - tutorial page is actually the main page after login
                current_url = self.current_page.url
                print(f"🔍 Login verification for {site_name} - Current URL: {current_url}")
                
                # After login, we're redirected to tutorial page which is the main page
                if site_config["tutorial_url"] in current_url or "tutorial" in current_url:
                    print(f"✅ Successfully logged into {site_name} - on tutorial/main page")
                    
                    # Handle popup again after navigation
                    self.handle_popup_if_present(site_config)
                    
                    # Get initial amount
                    amount = self.get_amount(site_config)
                    if amount:
                        print(f"💰 {site_name} amount: {amount}")
                        self.send_amount_update(site_name, amount, "initial_check")
                    
                    return True
                elif "login" in current_url.lower():
                    print(f"❌ Login failed for {site_name} - still on login page")
                    continue
                else:
                    print(f"✅ Successfully logged into {site_name}")
                    return True
                    
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
        """Handle popup if it appears after login or page reload"""
        site_name = site_config["name"]
        try:
            # Wait a bit for popup to appear
            time.sleep(1)
            
            popup_button = self.current_page.locator(site_config["popup_button"]).first
            if popup_button.is_visible():
                popup_button.click()
                print(f"📋 Popup 'I Know' button clicked for {site_name}")
                time.sleep(2)
                return True
            else:
                print(f"ℹ️ No popup visible for {site_name}")
                return False
        except Exception as e:
            print(f"ℹ️ No popup found for {site_name}: {e}")
            return False
    
    def get_amount(self, site_config):
        """Get amount from the page"""
        site_name = site_config["name"]
        try:
            amount_element = self.current_page.locator(site_config["amount_element"]).first
            if amount_element.is_visible():
                amount = amount_element.text_content()
                print(f"💰 {site_name} amount: {amount}")
                return amount
            else:
                print(f"ℹ️ Amount element not visible for {site_name}")
                return None
        except Exception as e:
            print(f"❌ Error getting amount for {site_name}: {e}")
            return None
    
    def send_amount_update(self, site_name, amount, action):
        """Send amount update to Telegram"""
        try:
            from telegram_bot import TelegramBot
            bot = TelegramBot()
            
            # Create detailed message based on action
            if action == "reset_claimed":
                message = f"🔄 {site_name}\n✅ Action: Reset Button Claimed\n💵 Amount: {amount}\n⏰ Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n🎉 Reset button successfully clicked!"
            elif action == "reset_not_found":
                message = f"🔄 {site_name}\n❌ Action: Reset Button Not Found\n💵 Amount: {amount}\n⏰ Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\nℹ️ No reset button available at this time"
            else:
                message = f"💰 {site_name}\n🔄 Action: {action}\n💵 Amount: {amount}\n⏰ Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            bot.send_message(message)
        except Exception as e:
            print(f"❌ Error sending notification for {site_name}: {e}")
    
    def check_reset_button(self, site_config):
        """Check if reset button is available"""
        site_name = site_config["name"]
        try:
            # Try multiple selectors for reset button
            reset_selectors = [
                "//uni-button[contains(@class, 'reset')]",
                "//button[contains(@class, 'reset')]", 
                "//uni-button[contains(text(), 'Reset')]",
                "//button[contains(text(), 'Reset')]",
                "//*[contains(@class, 'reset')]",
                "//uni-button[contains(@class, 'u-reset-button')]",
                "//*[contains(text(), 'reset')]",
                "//*[contains(text(), 'Reset')]"
            ]
            
            for selector in reset_selectors:
                try:
                    reset_button = self.current_page.locator(selector).first
                    if reset_button.is_visible():
                        print(f"✅ Reset button found with selector: {selector}")
                        return True
                except:
                    continue
            
            print(f"ℹ️ No reset button found for {site_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error checking reset button for {site_name}: {e}")
            return False
    
    def click_reset_button(self, site_config):
        """Click the reset button if available"""
        site_name = site_config["name"]
        print(f"🔍 [click_reset_button] Starting reset button search for {site_name}")
        try:
            # Try multiple selectors for reset button
            reset_selectors = [
                "//uni-button[contains(@class, 'reset')]",
                "//button[contains(@class, 'reset')]", 
                "//uni-button[contains(text(), 'Reset')]",
                "//button[contains(text(), 'Reset')]",
                "//*[contains(@class, 'reset')]",
                "//uni-button[contains(@class, 'u-reset-button')]",
                "//*[contains(text(), 'reset')]",
                "//*[contains(text(), 'Reset')]"
            ]
            
            print(f"🔍 [click_reset_button] Trying {len(reset_selectors)} selectors for {site_name}")
            for i, selector in enumerate(reset_selectors, 1):
                try:
                    print(f"🔍 [click_reset_button] [{i}/{len(reset_selectors)}] Trying selector: {selector}")
                    reset_button = self.current_page.locator(selector).first
                    print(f"🔍 [click_reset_button] Found element with selector: {selector}")
                    if reset_button.is_visible():
                        print(f"✅ [click_reset_button] Reset button is visible with selector: {selector}")
                        print(f"🎯 [click_reset_button] Attempting to click reset button for {site_name}")
                        
                        # Scroll into view
                        reset_button.scroll_into_view_if_needed()
                        time.sleep(1)
                        
                        # Try normal click
                        try:
                            print(f"🖱️ [click_reset_button] Attempting normal click for {site_name}")
                            reset_button.click()
                            print(f"✅ [click_reset_button] Reset button clicked successfully for {site_name}")
                            return True
                        except Exception as e:
                            print(f"⚠️ [click_reset_button] Normal click failed for {site_name}: {e}")
                            
                            # Try JavaScript click
                            try:
                                print(f"🖱️ [click_reset_button] Attempting JavaScript click for {site_name}")
                                page.evaluate("arguments[0].click()", reset_button.element_handle())
                                print(f"✅ [click_reset_button] JavaScript click successful for {site_name}")
                                return True
                            except Exception as e2:
                                print(f"❌ [click_reset_button] JavaScript click failed for {site_name}: {e2}")
                                continue
                                
                except Exception as e:
                    print(f"❌ Selector error: {e}")
                    continue
            
            print(f"ℹ️ [click_reset_button] No clickable reset button found for {site_name}")
            return False
                
        except Exception as e:
            print(f"❌ [click_reset_button] Error clicking reset button for {site_name}: {e}")
            return False

    def claim_reset_button(self, site_config):
        """Claim the reset button"""
        site_name = site_config["name"]
        try:
            print(f"🔄 Attempting to claim reset button for {site_name}")
            
            # Use the improved click_reset_button method
            if self.click_reset_button(site_config):
                print(f"✅ Reset button claimed for {site_name}")
                time.sleep(3)
                
                # Get amount after reset
                amount = self.get_amount(site_config)
                if amount:
                    self.send_amount_update(site_name, amount, "reset_claimed")
                
                return True
            else:
                print(f"ℹ️ No reset button available for {site_name}")
                return False
                
        except Exception as e:
            print(f"❌ Error claiming reset button for {site_name}: {e}")
            return False
    
    def monitor_site(self, site_config):
        """Monitor a single site with its own playwright instance"""
        site_name = site_config["name"]
        print(f"🔍 Starting monitoring for {site_name}")
        
        # Create complete playwright instance for this thread
        playwright = None
        browser = None
        context = None
        page = None
        
        try:
            # Each thread gets its own playwright instance
            playwright = sync_playwright().start()
            
            # Launch browser for this thread
            browser = playwright.chromium.launch(
                headless=False,  # Set to False for local testing
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-gpu',
                    '--window-size=1366,768',
                    '--start-maximized'
                ]
            )
            
            # Create context for this thread
            context = browser.new_context(
                viewport={'width': 375, 'height': 667},  # Mobile viewport
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            )
            
            # Create page for this thread
            page = context.new_page()
            
            # Set longer timeout for page operations
            page.set_default_timeout(60000)  # 60 seconds
            page.set_default_navigation_timeout(60000)  # 60 seconds
            
            # Set current page for login functions
            self.current_page = page
            print(f"📄 Created complete browser instance for {site_name}")
            
        except Exception as e:
            print(f"❌ Error creating browser for {site_name}: {e}")
            return
        
        # Track if we're already logged in to avoid unnecessary reloads
        logged_in = False
        last_amount_check = None
        
        while self.running:
            try:
                
                # Only check login status if we haven't confirmed login yet
                if not logged_in:
                    try:
                        # Start from login page
                        print(f"🌐 Navigating to {site_config['url']}")
                        self.current_page.goto(site_config["url"], timeout=60000)
                        
                        # Wait for page load with timeout
                        try:
                            self.current_page.wait_for_load_state("networkidle", timeout=30000)
                        except:
                            print(f"⚠️ Network idle timeout for {site_name}, continuing...")
                            self.current_page.wait_for_load_state("domcontentloaded", timeout=15000)
                        
                        time.sleep(3)
                        
                        current_url = self.current_page.url
                        print(f"🔍 Initial page for {site_name}: {current_url}")
                        
                        # Try to login
                        if self.login_to_site(site_config):
                            print(f"✅ Login successful for {site_name}")
                            logged_in = True
                        else:
                            print(f"❌ Login failed for {site_name}")
                            time.sleep(3600)  # Wait 1 hour on login failure
                            continue
                            
                    except Exception as e:
                        print(f"❌ Navigation error for {site_name}: {e}")
                        time.sleep(3600)  # Wait 1 hour on navigation error
                        continue
                
                # Now we're logged in, just monitor without reloading
                if logged_in:
                    # Handle popup if present (might appear after some time)
                    popup_handled = self.handle_popup_if_present(site_config)
                    if popup_handled:
                        time.sleep(2)  # Wait a bit after popup
                    
                    # Get current amount
                    amount = self.get_amount(site_config)
                    if amount:
                        # Only send update if amount changed or it's been a while
                        if last_amount_check != amount:
                            self.send_amount_update(site_name, amount, "amount_update")
                            print(f"💰 {site_name} amount: {amount}")
                            last_amount_check = amount
                    else:
                        # If we suddenly can't get amount, just retry (tutorial page is normal)
                        current_url = self.current_page.url
                        if "login" in current_url.lower() and site_config["tutorial_url"] not in current_url:
                            print(f"⚠️ Logged out detected for {site_name}")
                            logged_in = False  # Will trigger re-login on next iteration
                        else:
                            print(f"⚠️ Temporary amount issue for {site_name}, will retry")
                            # Try popup handling again
                            self.handle_popup_if_present(site_config)
                    
                    # Check reset button every 2 hours
                    current_time = datetime.now()
                    if site_name not in self.last_reset_times or \
                       current_time - self.last_reset_times[site_name] >= timedelta(hours=2):
                        
                        if self.claim_reset_button(site_config):
                            self.last_reset_times[site_name] = current_time
                            print(f"🔄 Reset button claimed for {site_name}")
                
                # Wait before next check (longer wait since we're not reloading)
                time.sleep(3600)  # Check every hour instead of 1 minute
                
            except Exception as e:
                print(f"❌ Error monitoring {site_name}: {e}")
                logged_in = False  # Reset login status on error
                time.sleep(3600)  # Wait 1 hour on error
        
        # Cleanup browser resources for this thread
        try:
            if page:
                page.close()
            if context:
                context.close()
            if browser:
                browser.close()
            if playwright:
                playwright.stop()
            print(f"🧹 Cleaned up browser resources for {site_name}")
        except Exception as e:
            print(f"⚠️ Cleanup error for {site_name}: {e}")
        
        print(f"🛑 Monitoring stopped for {site_name}")
    
    def monitor_site_once(self, site_config):
        """Monitor a single site once (no threading)"""
        site_name = site_config["name"]
        print(f"🔍 [monitor_site_once] Starting monitoring for {site_name}")
        
        # Create complete playwright instance
        playwright = None
        browser = None
        context = None
        page = None
        
        try:
            print(f"🎭 [monitor_site_once] Creating playwright instance for {site_name}")
            # Create playwright instance
            playwright = sync_playwright().start()
            
            # Launch browser
            print(f"🌐 [monitor_site_once] Launching browser for {site_name}")
            browser = playwright.chromium.launch(
                headless=True,  # Set to True for Render
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-gpu',
                    '--window-size=1366,768',
                    '--start-maximized'
                ]
            )
            print(f"✅ [monitor_site_once] Browser launched for {site_name}")
            
            # Create context
            print(f"📱 [monitor_site_once] Creating context for {site_name}")
            context = browser.new_context(
                viewport={'width': 375, 'height': 667},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            )
            print(f"✅ [monitor_site_once] Context created for {site_name}")
            
            # Create page
            print(f"📄 [monitor_site_once] Creating page for {site_name}")
            page = context.new_page()
            page.set_default_timeout(60000)
            page.set_default_navigation_timeout(60000)
            print(f"✅ [monitor_site_once] Page created for {site_name}")
            
            # Set current page for login functions
            self.current_page = page
            
            # Navigate to login page
            print(f"🌐 [monitor_site_once] Navigating to {site_config['url']} for {site_name}")
            page.goto(site_config["url"], timeout=60000)
            print(f"✅ [monitor_site_once] Navigation completed for {site_name}")
            
            # Wait for page load
            try:
                page.wait_for_load_state("networkidle", timeout=30000)
            except:
                print(f"⚠️ Network idle timeout, using domcontentloaded")
                page.wait_for_load_state("domcontentloaded", timeout=15000)
            
            time.sleep(3)
            
            # Try to login
            print(f"🔐 [monitor_site_once] Attempting login for {site_name}")
            if self.login_to_site(site_config):
                print(f"✅ [monitor_site_once] Login successful for {site_name}")
                
                # Handle popup
                print(f"🔍 [monitor_site_once] Checking for popups on {site_name}")
                self.handle_popup_if_present(site_config)
                
                # Get amount
                print(f"💰 [monitor_site_once] Getting amount for {site_name}")
                amount = self.get_amount(site_config)
                if amount:
                    print(f"✅ [monitor_site_once] Amount retrieved for {site_name}: {amount}")
                    self.send_amount_update(site_name, amount, "amount_update")
                    print(f"📱 [monitor_site_once] Telegram notification sent for {site_name}")
                else:
                    print(f"❌ [monitor_site_once] No amount found for {site_name}")
                
                # Check reset button every 1 hour
                current_time = datetime.now()
                print(f"🔄 [monitor_site_once] Checking reset button eligibility for {site_name}")
                if site_name not in self.last_reset_times or \
                   current_time - self.last_reset_times[site_name] >= timedelta(hours=1):
                    
                    print(f"🔄 [monitor_site_once] Reset button is eligible for {site_name}")
                    if self.claim_reset_button(site_config):
                        self.last_reset_times[site_name] = current_time
                        print(f"✅ [monitor_site_once] Reset button claimed for {site_name}")
                        # Send notification for successful reset button claim
                        self.send_amount_update(site_name, "Reset button claimed", "reset_claimed")
                        print(f"📱 [monitor_site_once] Reset button claim notification sent for {site_name}")
                    else:
                        print(f"❌ [monitor_site_once] Reset button claim failed for {site_name}")
                        # Send notification for failed reset button claim
                        self.send_amount_update(site_name, "Reset button not found", "reset_not_found")
                        print(f"📱 [monitor_site_once] Reset button not found notification sent for {site_name}")
                else:
                    print(f"⏰ [monitor_site_once] Reset button not yet eligible for {site_name}")
            else:
                print(f"❌ [monitor_site_once] Login failed for {site_name}")
                
        except Exception as e:
            print(f"❌ Error monitoring {site_name}: {e}")
            
        finally:
            # Cleanup
            try:
                if page:
                    page.close()
                if context:
                    context.close()
                if browser:
                    browser.close()
                if playwright:
                    playwright.stop()
                print(f"🧹 Cleaned up browser for {site_name}")
            except Exception as e:
                print(f"⚠️ Cleanup error for {site_name}: {e}")
    
    def start_monitoring(self):
        """Start monitoring all sites sequentially (no threading)"""
        print("🚀 Starting Advanced Automation with Telegram Bot...")
        print(f"📊 Will monitor {len(WEBSITES)} websites:")
        for site in WEBSITES:
            print(f"  - {site['name']}")
        
        # Monitor sites sequentially to avoid threading issues
        try:
            while self.running:
                print(f"\n🔄 [start_monitoring] Starting monitoring round...")
                for i, site_config in enumerate(WEBSITES, 1):
                    if not self.running:
                        break
                    
                    print(f"\n🔍 [start_monitoring] [{i}/{len(WEBSITES)}] Monitoring {site_config['name']}...")
                    print(f"🌐 [start_monitoring] URL: {site_config['url']}")
                    print(f"🔑 [start_monitoring] Username: {site_config.get('username', 'N/A')}")
                    print(f"🔐 [start_monitoring] Password: {'*' * len(site_config.get('password', ''))}")
                    self.monitor_site_once(site_config)
                    
                    # Small delay between sites
                    print(f"⏳ Waiting 5 seconds before next site...")
                    time.sleep(5)
                
                # Wait before next round
                print(f"\n⏳ Round completed. Waiting 1 hour before next monitoring round...")
                time.sleep(3600)
                
        except KeyboardInterrupt:
            print("🛑 Stopping automation...")
            self.running = False
        except Exception as e:
            print(f"❌ Error in monitoring loop: {e}")
            import traceback
            traceback.print_exc()
            # Continue monitoring even if there's an error
            print("🔄 Continuing monitoring after error...")
            time.sleep(60)  # Wait 1 minute before retrying
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
        print("🛑 Stopping all monitoring threads...")

if __name__ == "__main__":
    automation = AdvancedAutomation()
    automation.start_monitoring()