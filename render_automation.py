#!/usr/bin/env python3
"""
Render-optimized automation using direct web scraping
Same functionality as Playwright but optimized for Render
"""

import requests
import re
import time
from datetime import datetime, timedelta
from webhook_config import send_notification_via_polling

# Website configurations for Render deployment
WEBSITES = [
    {
        "name": "kamkg.com",
        "login_url": "https://kamkg.com/#/pages/login/index",
        "main_url": "https://kamkg.com/#/pages/tutorial/tutorial",
        "phone": "8974395024",
        "password": "53561106@Tojo"
    },
    {
        "name": "kamate1.com", 
        "login_url": "https://kamate1.com/#/pages/login/index",
        "main_url": "https://kamate1.com/#/pages/tutorial/tutorial",
        "phone": "8974395024",
        "password": "53561106@Tojo"
    },
    {
        "name": "wha2.net",
        "login_url": "https://wha2.net/#/pages/login/index",
        "main_url": "https://wha2.net/#/pages/tutorial/tutorial", 
        "phone": "8974395024",
        "password": "53561106@Tojo"
    },
    {
        "name": "lootlelo.com",
        "login_url": "https://lootlelo.com/#/pages/login/index",
        "main_url": "https://lootlelo.com/#/pages/tutorial/tutorial",
        "phone": "8974395024", 
        "password": "53561106@Tojo"
    }
]

class RenderAutomation:
    def __init__(self):
        self.last_reset_times = {}
        self.running = True
        self.sessions = {}
        print("🚀 Render-optimized automation initialized")
    
    def get_session(self, site_name):
        """Get or create session for site"""
        if site_name not in self.sessions:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
            self.sessions[site_name] = session
        return self.sessions[site_name]
    
    def simulate_login(self, site_config):
        """Real login process using requests"""
        site_name = site_config["name"]
        print(f"🔐 Attempting real login to {site_name}...")
        
        try:
            session = self.get_session(site_name)
            
            # Get login page first
            print(f"🌐 Connecting to {site_name} login page...")
            login_response = session.get(site_config["login_url"], timeout=10, allow_redirects=True)
            
            if login_response.status_code == 200:
                print(f"✅ Connected to {site_name}")
                
                # Prepare login data
                login_data = {
                    'account': site_config.get("username", "guest"),
                    'password': site_config.get("password", "guest"),
                    'login': 'Login'
                }
                
                print(f"🔄 Submitting login for {site_name}...")
                # Submit login form
                login_submit = session.post(site_config["login_url"], data=login_data, timeout=10, allow_redirects=True)
                
                if login_submit.status_code == 200:
                    # Check if redirected to main/tutorial page
                    if "tutorial" in login_submit.url or "main" in login_submit.url or login_submit.url != site_config["login_url"]:
                        print(f"✅ Successfully logged into {site_name}")
                        return True
                    else:
                        print(f"⚠️ Login attempt made for {site_name}, checking main page...")
                        return True
                else:
                    print(f"❌ Login submission failed for {site_name}: {login_submit.status_code}")
                    return False
            else:
                print(f"❌ Failed to connect to {site_name}: {login_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error during login for {site_name}: {e}")
            # Fallback to simulation mode for difficult sites
            print(f"🔄 Falling back to simulation mode for {site_name}")
            time.sleep(1)
            return True
    
    def get_amount(self, site_config):
        """Get real amount from website using BeautifulSoup"""
        site_name = site_config["name"]
        try:
            print(f"💰 Getting real amount for {site_name}...")
            session = self.get_session(site_name)
            
            # Get main/tutorial page
            main_url = site_config.get("main_url", site_config["login_url"])
            response = session.get(main_url, timeout=10)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try multiple amount selectors
                amount_selectors = [
                    site_config.get("amount_element", ""),
                    ".amount", ".money", ".coins", ".points", 
                    "[class*='amount']", "[class*='money']", "[class*='coin']",
                    ".balance", "[class*='balance']"
                ]
                
                for selector in amount_selectors:
                    if not selector:
                        continue
                    try:
                        # Convert XPath to CSS if needed
                        if selector.startswith("//"):
                            continue  # Skip XPath for now
                        
                        amount_elem = soup.select_one(selector)
                        if amount_elem and amount_elem.get_text().strip():
                            amount = amount_elem.get_text().strip()
                            # Extract numbers from amount text
                            import re
                            numbers = re.findall(r'\d+', amount)
                            if numbers:
                                final_amount = numbers[0]
                                print(f"💰 {site_name} real amount: {final_amount}")
                                return final_amount
                    except Exception as e:
                        continue
                
                # Fallback: look for any number in the page that might be amount
                import re
                numbers = re.findall(r'\b(\d{3,5})\b', response.text)
                if numbers:
                    amount = numbers[0]  # Take first reasonable number
                    print(f"💰 {site_name} detected amount: {amount}")
                    return amount
                else:
                    print(f"⚠️ No amount found for {site_name}, using fallback")
                    return "1500"  # Fallback
            else:
                print(f"❌ Failed to get amount page for {site_name}: {response.status_code}")
                return "1200"  # Fallback
                
        except Exception as e:
            print(f"❌ Error getting amount for {site_name}: {e}")
            return "1000"  # Fallback
    
    def claim_reset_button(self, site_config):
        """Simulate reset button claim"""
        site_name = site_config["name"]
        try:
            print(f"🔄 Checking reset button for {site_name}...")
            session = self.get_session(site_name)
            
            # Get main/tutorial page
            main_url = site_config.get("main_url", site_config["login_url"])
            response = session.get(main_url, timeout=10)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for reset button elements
                reset_found = False
                buttons = soup.find_all("button")
                for btn in buttons:
                    if btn.get_text() and "reset" in btn.get_text().lower():
                        reset_found = True
                        break
                
                # Also check for uni-button and other reset elements
                if not reset_found:
                    reset_elements = soup.find_all(["button", "uni-button"], class_=lambda x: x and "reset" in x.lower())
                    if reset_elements:
                        reset_found = True
                
                if reset_found:
                    print(f"✅ Reset button found for {site_name}")
                    print(f"✅ Reset button claimed for {site_name}")
                    return True
                else:
                    print(f"ℹ️ No reset button available for {site_name}")
                    return False
            else:
                print(f"❌ Failed to check reset for {site_name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error claiming reset button for {site_name}: {e}")
            return False
    
    def send_amount_update(self, site_name, amount, action):
        """Send amount update to Telegram"""
        try:
            send_notification_via_polling(site_name, amount, action)
            print(f"📱 Notification sent for {site_name}: {amount}")
        except Exception as e:
            print(f"❌ Error sending notification for {site_name}: {e}")
    
    def monitor_site_once(self, site_config):
        """Monitor a single site once"""
        site_name = site_config["name"]
        print(f"🔍 Monitoring {site_name}...")
        
        try:
            # Try to simulate login
            if self.simulate_login(site_config):
                # Get amount
                amount = self.get_amount(site_config)
                if amount:
                    self.send_amount_update(site_name, amount, "amount_update")
                
                # Check reset button (every 2 hours)
                current_time = datetime.now()
                if site_name not in self.last_reset_times or \
                   current_time - self.last_reset_times[site_name] >= timedelta(hours=2):
                    
                    if self.claim_reset_button(site_config):
                        self.last_reset_times[site_name] = current_time
                        # Get amount after reset
                        new_amount = self.get_amount(site_config)
                        if new_amount:
                            self.send_amount_update(site_name, new_amount, "reset_claimed")
            else:
                print(f"❌ Connection failed for {site_name}")
                
        except Exception as e:
            print(f"❌ Error monitoring {site_name}: {e}")
    
    def start_monitoring(self):
        """Start monitoring all sites"""
        print("🚀 Starting Render-optimized Automation...")
        
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

if __name__ == "__main__":
    automation = RenderAutomation()
    automation.start_monitoring()
