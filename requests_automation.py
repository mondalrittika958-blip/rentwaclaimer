import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from webhook_config import send_notification_via_polling

# Website configurations
WEBSITES = [
    {
        "name": "kamkg",
        "url": "https://kamkg.com",
        "login_url": "https://kamkg.com/login",
        "dashboard_url": "https://kamkg.com/dashboard",
        "amount_selectors": [
            "span.amount",
            ".balance",
            "#amount",
            ".wallet-balance",
            "[class*='amount']",
            "[class*='balance']"
        ],
        "reset_selectors": [
            "button[class*='reset']",
            "button[class*='claim']",
            ".reset-btn",
            ".claim-btn",
            "button:contains('Reset')",
            "button:contains('Claim')"
        ]
    },
    {
        "name": "kamate1",
        "url": "https://kamate1.com",
        "login_url": "https://kamate1.com/login",
        "dashboard_url": "https://kamate1.com/dashboard",
        "amount_selectors": [
            "span.amount",
            ".balance",
            "#amount",
            ".wallet-balance",
            "[class*='amount']",
            "[class*='balance']"
        ],
        "reset_selectors": [
            "button[class*='reset']",
            "button[class*='claim']",
            ".reset-btn",
            ".claim-btn",
            "button:contains('Reset')",
            "button:contains('Claim')"
        ]
    },
    {
        "name": "wha2",
        "url": "https://wha2.net",
        "login_url": "https://wha2.net/login",
        "dashboard_url": "https://wha2.net/dashboard",
        "amount_selectors": [
            "span.amount",
            ".balance",
            "#amount",
            ".wallet-balance",
            "[class*='amount']",
            "[class*='balance']"
        ],
        "reset_selectors": [
            "button[class*='reset']",
            "button[class*='claim']",
            ".reset-btn",
            ".claim-btn",
            "button:contains('Reset')",
            "button:contains('Claim')"
        ]
    },
    {
        "name": "lootlelo",
        "url": "https://lootlelo.com",
        "login_url": "https://lootlelo.com/login",
        "dashboard_url": "https://lootlelo.com/dashboard",
        "amount_selectors": [
            "span.amount",
            ".balance",
            "#amount",
            ".wallet-balance",
            "[class*='amount']",
            "[class*='balance']"
        ],
        "reset_selectors": [
            "button[class*='reset']",
            "button[class*='claim']",
            ".reset-btn",
            ".claim-btn",
            "button:contains('Reset')",
            "button:contains('Claim')"
        ]
    }
]

class RequestsAutomation:
    def __init__(self):
        self.session = requests.Session()
        self.last_reset_times = {}
        self.running = True
        
        # Set headers to mimic real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        print("🚀 Requests + BeautifulSoup Real Website Automation initialized")
        
    def login_to_site(self, site_config):
        """Login to website using requests"""
        site_name = site_config["name"]
        login_url = site_config["login_url"]
        
        try:
            print(f"🔐 Attempting login to {site_name}...")
            
            # Get login page
            response = self.session.get(login_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find login form
            form = soup.find('form')
            if not form:
                print(f"❌ No login form found on {site_name}")
                return False
                
            # Extract form data
            form_data = {}
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                if name:
                    form_data[name] = value
                    
            # Set login credentials (you'll need to update these)
            form_data['username'] = 'your_username'  # Update with real credentials
            form_data['password'] = 'your_password'  # Update with real credentials
            form_data['email'] = 'your_email'        # Update with real credentials
            
            # Submit login form
            action_url = form.get('action', login_url)
            if action_url.startswith('/'):
                action_url = site_config["url"] + action_url
                
            login_response = self.session.post(action_url, data=form_data, timeout=10)
            login_response.raise_for_status()
            
            # Check if login successful
            if 'dashboard' in login_response.url or 'welcome' in login_response.text.lower():
                print(f"✅ Successfully logged in to {site_name}")
                return True
            else:
                print(f"❌ Login failed for {site_name}")
                return False
                
        except Exception as e:
            print(f"❌ Login error for {site_name}: {e}")
            return False
            
    def get_amount(self, site_config):
        """Extract amount from website using BeautifulSoup"""
        site_name = site_config["name"]
        dashboard_url = site_config["dashboard_url"]
        
        try:
            print(f"💰 Getting amount from {site_name}...")
            
            # Get dashboard page
            response = self.session.get(dashboard_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple selectors to find amount
            amount = None
            for selector in site_config["amount_selectors"]:
                try:
                    element = soup.select_one(selector)
                    if element:
                        amount_text = element.get_text(strip=True)
                        # Extract numbers from text
                        import re
                        numbers = re.findall(r'[\d,]+', amount_text)
                        if numbers:
                            amount = numbers[0].replace(',', '')
                            break
                except:
                    continue
                    
            if amount:
                print(f"💰 {site_name} amount: {amount}")
                return int(amount)
            else:
                print(f"❌ Could not find amount for {site_name}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting amount from {site_name}: {e}")
            return None
            
    def check_reset_button(self, site_config):
        """Check if reset button is available"""
        site_name = site_config["name"]
        dashboard_url = site_config["dashboard_url"]
        
        try:
            response = self.session.get(dashboard_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check multiple selectors for reset button
            for selector in site_config["reset_selectors"]:
                try:
                    element = soup.select_one(selector)
                    if element and element.get_text(strip=True):
                        print(f"✅ Reset button found on {site_name}")
                        return True
                except:
                    continue
                    
            print(f"❌ No reset button found on {site_name}")
            return False
            
        except Exception as e:
            print(f"❌ Error checking reset button on {site_name}: {e}")
            return False
            
    def click_reset_button(self, site_config):
        """Click reset button using requests"""
        site_name = site_config["name"]
        dashboard_url = site_config["dashboard_url"]
        
        try:
            print(f"🔄 Clicking reset button on {site_name}...")
            
            # Get dashboard page first
            response = self.session.get(dashboard_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find reset button
            reset_button = None
            for selector in site_config["reset_selectors"]:
                try:
                    element = soup.select_one(selector)
                    if element and element.get_text(strip=True):
                        reset_button = element
                        break
                except:
                    continue
                    
            if not reset_button:
                print(f"❌ Reset button not found on {site_name}")
                return False
                
            # Extract form data for reset button
            form = reset_button.find_parent('form')
            if form:
                form_data = {}
                for input_tag in form.find_all('input'):
                    name = input_tag.get('name')
                    value = input_tag.get('value', '')
                    if name:
                        form_data[name] = value
                        
                # Add reset button value
                button_name = reset_button.get('name')
                button_value = reset_button.get('value', '')
                if button_name:
                    form_data[button_name] = button_value
                    
                # Submit form
                action_url = form.get('action', dashboard_url)
                if action_url.startswith('/'):
                    action_url = site_config["url"] + action_url
                    
                reset_response = self.session.post(action_url, data=form_data, timeout=10)
                reset_response.raise_for_status()
                
                print(f"✅ Reset button clicked on {site_name}")
                return True
            else:
                print(f"❌ Reset button not in form on {site_name}")
                return False
                
        except Exception as e:
            print(f"❌ Error clicking reset button on {site_name}: {e}")
            return False
            
    def monitor_site(self, site_config):
        """Monitor a single site"""
        site_name = site_config["name"]
        
        try:
            print(f"🔍 Monitoring {site_name}...")
            
            # Try to login first
            if not self.login_to_site(site_config):
                print(f"❌ Login failed for {site_name}, skipping...")
                return
                
            # Get current amount
            amount = self.get_amount(site_config)
            if amount is None:
                print(f"❌ Could not get amount for {site_name}")
                return
                
            # Check if it's time to reset
            now = datetime.now()
            last_reset = self.last_reset_times.get(site_name)
            
            if last_reset is None or (now - last_reset).total_seconds() >= 3600:  # 1 hour
                print(f"⏰ Time to reset for {site_name}")
                
                if self.check_reset_button(site_config):
                    if self.click_reset_button(site_config):
                        self.last_reset_times[site_name] = now
                        print(f"✅ Reset successful for {site_name}")
                        
                        # Send notification
                        message = f"🔄 Reset claimed for {site_name} - Amount: {amount}"
                        send_notification_via_polling(message, site_name, amount, "reset_claimed")
                    else:
                        print(f"❌ Reset failed for {site_name}")
                else:
                    print(f"❌ No reset button available for {site_name}")
            else:
                print(f"💰 {site_name} amount: {amount} (Next reset in {3600 - (now - last_reset).total_seconds():.0f}s)")
                
        except Exception as e:
            print(f"❌ Error monitoring {site_name}: {e}")
            
    def start_monitoring(self):
        """Start monitoring all websites"""
        print("🚀 Starting Requests + BeautifulSoup monitoring...")
        
        while self.running:
            try:
                for site_config in WEBSITES:
                    self.monitor_site(site_config)
                    time.sleep(5)  # Small delay between sites
                    
                print("⏰ Waiting 1 hour before next check...")
                time.sleep(3600)  # Wait 1 hour
                
            except KeyboardInterrupt:
                print("🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(60)  # Wait 1 minute before retry
                
        print("✅ Monitoring stopped")
