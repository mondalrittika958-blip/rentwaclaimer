from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import threading
import requests
import json
import os
import platform
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
        self.driver = None
        self.tabs = {}
        self.last_reset_times = {}
        self.running = True
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with multiple tabs"""
        # Determine ChromeDriver path
        system = platform.system().lower()
        if system == "windows":
            chromedriver_path = "./chromedriver.exe"
        else:
            chromedriver_path = "./chromedriver"
        
        # Check if ChromeDriver exists, if not try to download
        if not os.path.exists(chromedriver_path):
            print("🔧 ChromeDriver not found, attempting to download...")
            try:
                from setup_chromedriver import download_chromedriver
                if not download_chromedriver():
                    print("❌ Failed to download ChromeDriver")
                    return
            except Exception as e:
                print(f"❌ Error downloading ChromeDriver: {e}")
                return
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless")  # Run in headless mode for server
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Create tabs for each website
        for i, site in enumerate(WEBSITES):
            if i == 0:
                # Use the first tab
                self.tabs[site["name"]] = self.driver.current_window_handle
            else:
                # Create new tabs
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[i])
                self.tabs[site["name"]] = self.driver.current_window_handle
        
        print("🚀 Browser setup completed with 4 tabs")
    
    def switch_to_tab(self, site_name):
        """Switch to specific website tab"""
        if site_name in self.tabs:
            self.driver.switch_to.window(self.tabs[site_name])
            return True
        return False
    
    def login_to_site(self, site_config):
        """Login to a specific website"""
        site_name = site_config["name"]
        print(f"\n🔐 Logging into {site_name}...")
        
        if not self.switch_to_tab(site_name):
            print(f"❌ Could not switch to {site_name} tab")
            return False
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Login attempt {attempt + 1}/{max_retries} for {site_name}")
                
                # Navigate to login page
                self.driver.get(site_config["url"])
                wait = WebDriverWait(self.driver, 30)
                time.sleep(5)
                
                # Fill phone field
                phone_field = wait.until(EC.presence_of_element_located((By.XPATH, site_config["phone_field"])))
                phone_field.clear()
                phone_field.send_keys("8974395024")
                print(f"📱 Phone entered for {site_name}")
                
                # Fill password field
                password_field = wait.until(EC.presence_of_element_located((By.XPATH, site_config["password_field"])))
                password_field.clear()
                password_field.send_keys("53561106@Tojo")
                print(f"🔑 Password entered for {site_name}")
                
                # Click login button
                login_button = wait.until(EC.element_to_be_clickable((By.XPATH, site_config["login_button"])))
                login_button.click()
                print(f"✅ Login button clicked for {site_name}")
                
                time.sleep(5)
                
                # Handle popup (with multiple attempts)
                popup_handled = False
                for popup_attempt in range(3):
                    try:
                        popup_wait = WebDriverWait(self.driver, 5)
                        popup_element = popup_wait.until(EC.element_to_be_clickable((By.XPATH, site_config["popup_button"])))
                        popup_element.click()
                        print(f"📋 Popup handled for {site_name} (attempt {popup_attempt + 1})")
                        popup_handled = True
                        time.sleep(2)
                        break
                    except TimeoutException:
                        print(f"ℹ️ No popup for {site_name} (attempt {popup_attempt + 1})")
                        time.sleep(1)
                
                if not popup_handled:
                    print(f"ℹ️ No popup appeared for {site_name}")
                
                # Navigate to main page
                self.driver.get(site_config["main_url"])
                time.sleep(5)
                
                # Verify login success by checking if we're not on login page
                current_url = self.driver.current_url
                print(f"🔍 Login verification for {site_name} - Current URL: {current_url}")
                
                # More lenient verification - just check we're not on login page
                if "login" not in current_url.lower():
                    print(f"✅ Successfully logged into {site_name}")
                    
                    # Get initial amount after login
                    time.sleep(3)
                    amount = self.get_amount(site_config)
                    if amount:
                        print(f"💰 Initial amount for {site_name}: {amount}")
                        self.send_amount_update(site_name, amount, "login_success")
                    else:
                        self.send_amount_update(site_name, "Login Successful", "login_success")
                    
                    return True
                else:
                    print(f"⚠️ Still on login page for {site_name}, retrying...")
                    time.sleep(3)
                    continue
                
            except Exception as e:
                print(f"❌ Error logging into {site_name} (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    print(f"🔄 Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"❌ Failed to login to {site_name} after {max_retries} attempts")
                    return False
        
        return False
    
    def check_logout(self, site_config):
        """Check if user is logged out by checking for actual logout indicators"""
        site_name = site_config["name"]
        try:
            current_url = self.driver.current_url
            print(f"🔍 Checking {site_name} - Current URL: {current_url}")
            
            # Only check for actual logout indicators, not tutorial page
            # Tutorial page is normal after login, not a logout indicator
            
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
                amount_element = self.driver.find_element(By.XPATH, site_config["amount_element"])
                if amount_element and amount_element.is_displayed():
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
    
    def handle_popup_if_present(self, site_config):
        """Handle popup if present during monitoring"""
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
                    popup_wait = WebDriverWait(self.driver, 2)
                    popup_element = popup_wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    if popup_element and popup_element.is_displayed():
                        popup_element.click()
                        print(f"📋 Popup handled for {site_name} using selector: {selector}")
                        time.sleep(2)
                        return True
                except TimeoutException:
                    continue
                except Exception as e:
                    print(f"⚠️ Error with popup selector {selector}: {e}")
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Error handling popup for {site_name}: {e}")
            return False
    
    def get_amount(self, site_config):
        """Get current amount from the website"""
        site_name = site_config["name"]
        try:
            amount_element = self.driver.find_element(By.XPATH, site_config["amount_element"])
            amount = amount_element.text.strip()
            print(f"💰 {site_name} amount: {amount}")
            return amount
        except Exception as e:
            print(f"❌ Could not get amount for {site_name}: {e}")
            return None
    
    def send_amount_update(self, site_name, amount, action="amount_update"):
        """Send amount update to channel via polling method"""
        print(f"📤 Sending update for {site_name}: {amount}")
        try:
            # Try polling method first
            send_notification_via_polling(site_name, amount, action)
        except Exception as e:
            print(f"❌ Polling method failed: {e}")
            # Fallback to webhook method
            send_webhook_notification(site_name, amount, action)
    
    def claim_reset_button(self, site_config):
        """Claim reset button if available"""
        site_name = site_config["name"]
        print(f"🎯 Checking reset button for {site_name}...")
        
        try:
            # Check if reset button is available
            reset_wait = WebDriverWait(self.driver, 5)
            reset_button = reset_wait.until(EC.presence_of_element_located((By.XPATH, site_config["reset_button"])))
            
            # Scroll to button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", reset_button)
            time.sleep(1)
            
            # Try to click
            try:
                reset_button.click()
                print(f"🎉 Reset button claimed for {site_name}!")
                
                # Get amount after claiming
                time.sleep(3)
                amount = self.get_amount(site_config)
                if amount:
                    self.send_amount_update(site_name, amount, "reset_claimed")
                
                # Update last reset time
                self.last_reset_times[site_name] = datetime.now()
                return True
                
            except Exception as click_error:
                print(f"❌ Could not click reset button for {site_name}: {click_error}")
                return False
                
        except TimeoutException:
            print(f"ℹ️ Reset button not available for {site_name} (cooldown)")
            return False
        except Exception as e:
            print(f"❌ Error checking reset button for {site_name}: {e}")
            return False
    
    def should_reset(self, site_name):
        """Check if it's time to reset (2 hours)"""
        if site_name not in self.last_reset_times:
            return True
        
        last_reset = self.last_reset_times[site_name]
        now = datetime.now()
        time_diff = now - last_reset
        
        return time_diff >= timedelta(hours=2)
    
    def monitor_site(self, site_config):
        """Monitor a single site continuously"""
        site_name = site_config["name"]
        print(f"👁️ Starting monitoring for {site_name}")
        
        while self.running:
            try:
                if not self.switch_to_tab(site_name):
                    print(f"❌ Could not switch to {site_name} tab")
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
                else:
                    # Regular amount check (every 5 minutes)
                    if not hasattr(self, 'last_amount_check'):
                        self.last_amount_check = {}
                    
                    current_time = datetime.now()
                    last_check = self.last_amount_check.get(site_name, current_time - timedelta(minutes=10))
                    
                    if current_time - last_check >= timedelta(minutes=5):
                        amount = self.get_amount(site_config)
                        if amount:
                            print(f"💰 Current amount for {site_name}: {amount}")
                            self.send_amount_update(site_name, amount, "amount_check")
                        self.last_amount_check[site_name] = current_time
                
                # Wait before next check
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"❌ Error monitoring {site_name}: {e}")
                # Try to recover by re-login
                try:
                    if self.login_to_site(site_config):
                        print(f"✅ {site_name} recovered after error")
                    else:
                        print(f"❌ {site_name} recovery failed")
                except:
                    print(f"❌ {site_name} recovery attempt failed")
                time.sleep(30)
    
    def start_monitoring(self):
        """Start monitoring all sites"""
        print("🚀 Starting advanced automation...")
        
        # Login to all sites first
        for site_config in WEBSITES:
            self.login_to_site(site_config)
            time.sleep(5)
        
        print("✅ All sites logged in successfully!")
        print("🔄 Starting continuous monitoring...")
        
        # Start monitoring threads for each site
        threads = []
        for site_config in WEBSITES:
            thread = threading.Thread(target=self.monitor_site, args=(site_config,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(60)
                print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Monitoring active...")
        except KeyboardInterrupt:
            print("\n🛑 Stopping automation...")
            self.running = False
    
    def stop(self):
        """Stop the automation"""
        self.running = False
        if self.driver:
            self.driver.quit()

def main():
    automation = AdvancedAutomation()
    try:
        automation.start_monitoring()
    except KeyboardInterrupt:
        print("\n🛑 Automation stopped by user")
    finally:
        automation.stop()

if __name__ == "__main__":
    main()
