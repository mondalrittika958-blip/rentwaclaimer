import time
import os
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webhook_config import send_notification_via_polling

# Website configurations
WEBSITES = [
    {
        "name": "kamkg",
        "login_url": "https://kamkg.com/login",
        "main_url": "https://kamkg.com/tutorial",
        "amount_element": "//span[contains(@class, 'number')]",
        "username": "guest",
        "password": "guest"
    },
    {
        "name": "kamate1", 
        "login_url": "https://kamate1.com/login",
        "main_url": "https://kamate1.com/tutorial",
        "amount_element": "//span[contains(@class, 'amount')]",
        "username": "guest",
        "password": "guest"
    },
    {
        "name": "wha2",
        "login_url": "https://wha2.net/login", 
        "main_url": "https://wha2.net/tutorial",
        "amount_element": "//div[contains(@class, 'money')]",
        "username": "guest",
        "password": "guest"
    },
    {
        "name": "lootlelo",
        "login_url": "https://lootlelo.com/login",
        "main_url": "https://lootlelo.com/tutorial", 
        "amount_element": "//span[contains(@class, 'coins')]",
        "username": "guest",
        "password": "guest"
    }
]

class SeleniumAutomation:
    def __init__(self):
        self.driver = None
        self.last_reset_times = {}
        self.running = True
        print("🚀 Selenium Real Website Automation initialized")
        
    def setup_driver(self):
        """Setup Chrome WebDriver with WebDriver Manager"""
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            chrome_options = Options()
            
            # Check if running on Render
            is_render = os.environ.get('PORT') is not None
            
            if is_render:
                print("🔧 Setting up Chrome for Render deployment...")
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--disable-setuid-sandbox")
                chrome_options.add_argument("--remote-debugging-port=9222")
                chrome_options.add_argument("--disable-web-security")
                chrome_options.add_argument("--allow-running-insecure-content")
            else:
                print("🔧 Setting up Chrome for local development...")
                chrome_options.add_argument("--window-size=1366,768")
                chrome_options.add_argument("--start-maximized")
            
            # Common options
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Use WebDriver Manager to handle ChromeDriver
            print("🔧 Downloading/updating ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            
            # Create driver with timeout
            print("🔧 Creating WebDriver instance...")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup Chrome WebDriver: {e}")
            print("🔄 Falling back to Playwright...")
            return False
    
    def login_to_site(self, site_config):
        """Login to website using real browser automation"""
        site_name = site_config["name"]
        
        try:
            print(f"🔐 Logging into {site_name}...")
            
            # Navigate to login page
            self.driver.get(site_config["login_url"])
            time.sleep(3)
            
            # Fill login form
            try:
                username_field = self.driver.find_element(By.NAME, "account")
                password_field = self.driver.find_element(By.NAME, "password")
                login_button = self.driver.find_element(By.NAME, "login")
                
                username_field.clear()
                username_field.send_keys(site_config["username"])
                
                password_field.clear()
                password_field.send_keys(site_config["password"])
                
                login_button.click()
                time.sleep(5)
                
                # Check if login successful
                current_url = self.driver.current_url
                if "tutorial" in current_url or "main" in current_url:
                    print(f"✅ Successfully logged into {site_name}")
                    return True
                else:
                    print(f"⚠️ Login attempt completed for {site_name}")
                    return True
                    
            except NoSuchElementException:
                print(f"⚠️ Login form not found for {site_name}, proceeding...")
                return True
                
        except Exception as e:
            print(f"❌ Error logging into {site_name}: {e}")
            return False
    
    def get_amount(self, site_config):
        """Get real amount from website"""
        site_name = site_config["name"]
        
        try:
            print(f"💰 Getting amount for {site_name}...")
            
            # Try to find amount element
            try:
                amount_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, site_config["amount_element"]))
                )
                amount_text = amount_element.text.strip()
                
                # Extract numbers from text
                import re
                numbers = re.findall(r'\d+', amount_text)
                if numbers:
                    amount = numbers[0]
                    print(f"💰 {site_name} real amount: {amount}")
                    return amount
                    
            except TimeoutException:
                print(f"⚠️ Amount element not found for {site_name}, trying alternatives...")
                
                # Try alternative selectors
                selectors = [
                    "span[class*='amount']",
                    "div[class*='money']", 
                    "span[class*='coins']",
                    "div[class*='balance']"
                ]
                
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            text = element.text.strip()
                            numbers = re.findall(r'\d+', text)
                            if numbers and len(numbers[0]) >= 3:
                                amount = numbers[0]
                                print(f"💰 {site_name} detected amount: {amount}")
                                return amount
                    except:
                        continue
                
                # Fallback - look for any 3-4 digit numbers on page
                page_text = self.driver.page_source
                numbers = re.findall(r'\b(\d{3,4})\b', page_text)
                if numbers:
                    amount = numbers[0]
                    print(f"💰 {site_name} found amount: {amount}")
                    return amount
                
            print(f"⚠️ No amount found for {site_name}")
            return None
            
        except Exception as e:
            print(f"❌ Error getting amount for {site_name}: {e}")
            return None
    
    def check_reset_button(self, site_config):
        """Check for reset button"""
        site_name = site_config["name"]
        
        try:
            # Try multiple reset button selectors
            reset_selectors = [
                "//uni-button[contains(@class, 'reset')]",
                "//button[contains(@class, 'reset')]",
                "//button[contains(text(), 'Reset')]",
                "//uni-button[contains(text(), 'Reset')]"
            ]
            
            for selector in reset_selectors:
                try:
                    reset_button = self.driver.find_element(By.XPATH, selector)
                    if reset_button.is_displayed():
                        print(f"✅ Reset button found for {site_name}")
                        reset_button.click()
                        time.sleep(2)
                        print(f"✅ Reset button claimed for {site_name}")
                        return True
                except:
                    continue
            
            print(f"ℹ️ No reset button available for {site_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error checking reset for {site_name}: {e}")
            return False
    
    def monitor_site_once(self, site_config):
        """Monitor a single site"""
        site_name = site_config["name"]
        print(f"🔍 Monitoring {site_name}...")
        
        try:
            # Login to site
            if self.login_to_site(site_config):
                # Get amount
                amount = self.get_amount(site_config)
                if amount:
                    send_notification_via_polling(site_name, amount, "amount_update")
                
                # Check reset button (every 2 hours)
                current_time = datetime.now()
                if site_name not in self.last_reset_times or \
                   current_time - self.last_reset_times[site_name] >= timedelta(hours=2):
                    
                    if self.check_reset_button(site_config):
                        self.last_reset_times[site_name] = current_time
                        # Get amount after reset
                        new_amount = self.get_amount(site_config)
                        if new_amount:
                            send_notification_via_polling(site_name, new_amount, "reset_claimed")
            
        except Exception as e:
            print(f"❌ Error monitoring {site_name}: {e}")
    
    def start_monitoring(self):
        """Start the monitoring process"""
        print("🚀 Starting Selenium Real Website Automation...")
        
        if not self.setup_driver():
            print("❌ Failed to setup WebDriver")
            return
        
        try:
            while self.running:
                for site_config in WEBSITES:
                    if not self.running:
                        break
                    
                    self.monitor_site_once(site_config)
                    time.sleep(5)  # Delay between sites
                
                # Wait before next round
                print("⏳ Waiting 1 hour before next monitoring round...")
                time.sleep(3600)  # 1 hour
                
        except KeyboardInterrupt:
            print("🛑 Stopping automation...")
            self.running = False
        finally:
            if self.driver:
                self.driver.quit()
                print("🔧 WebDriver closed")

if __name__ == "__main__":
    automation = SeleniumAutomation()
    automation.start_monitoring()
