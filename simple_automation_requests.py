import requests
import time
import json
from datetime import datetime, timedelta
from webhook_config import send_notification_via_polling

# Website configurations for requests-based automation
WEBSITES = [
    {
        "name": "kamkg.com",
        "login_url": "https://kamkg.com/api/login",
        "main_url": "https://kamkg.com/api/user/dashboard", 
        "reset_url": "https://kamkg.com/api/user/claim-reset",
        "credentials": {"phone": "8974395024", "password": "53561106@Tojo"}
    },
    {
        "name": "kamate1.com", 
        "login_url": "https://kamate1.com/api/login",
        "main_url": "https://kamate1.com/api/user/dashboard",
        "reset_url": "https://kamate1.com/api/user/claim-reset", 
        "credentials": {"phone": "8974395024", "password": "53561106@Tojo"}
    },
    {
        "name": "wha2.net",
        "login_url": "https://wha2.net/api/login", 
        "main_url": "https://wha2.net/api/user/dashboard",
        "reset_url": "https://wha2.net/api/user/claim-reset",
        "credentials": {"phone": "8974395024", "password": "53561106@Tojo"}
    },
    {
        "name": "lootlelo.com",
        "login_url": "https://lootlelo.com/api/login",
        "main_url": "https://lootlelo.com/api/user/dashboard", 
        "reset_url": "https://lootlelo.com/api/user/claim-reset",
        "credentials": {"phone": "8974395024", "password": "53561106@Tojo"}
    }
]

class SimpleAutomation:
    def __init__(self):
        self.last_reset_times = {}
        self.running = True
        self.sessions = {}
        print("🚀 Simple Requests Automation initialized")
    
    def get_session(self, site_name):
        """Get or create session for site"""
        if site_name not in self.sessions:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json'
            })
            self.sessions[site_name] = session
        return self.sessions[site_name]
    
    def login_to_site(self, site_config):
        """Login to site using requests"""
        site_name = site_config["name"]
        print(f"🔐 Logging into {site_name} via API...")
        
        try:
            session = self.get_session(site_name)
            
            # Attempt login
            login_data = site_config["credentials"]
            response = session.post(site_config["login_url"], json=login_data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Successfully logged into {site_name}")
                return True
            else:
                print(f"❌ Login failed for {site_name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Login error for {site_name}: {e}")
            return False
    
    def get_amount(self, site_config):
        """Get amount from site"""
        site_name = site_config["name"]
        try:
            session = self.get_session(site_name)
            response = session.get(site_config["main_url"], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Try to extract amount from response
                amount = data.get('balance', data.get('amount', data.get('total', 'Unknown')))
                print(f"💰 {site_name} amount: {amount}")
                return str(amount)
            else:
                print(f"❌ Failed to get amount for {site_name}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting amount for {site_name}: {e}")
            return None
    
    def claim_reset_button(self, site_config):
        """Claim reset button"""
        site_name = site_config["name"]
        try:
            session = self.get_session(site_name)
            response = session.post(site_config["reset_url"], timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Reset button claimed for {site_name}")
                return True
            else:
                print(f"❌ Reset claim failed for {site_name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Reset claim error for {site_name}: {e}")
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
            # Try to login
            if self.login_to_site(site_config):
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
                print(f"❌ Login failed for {site_name}")
                
        except Exception as e:
            print(f"❌ Error monitoring {site_name}: {e}")
    
    def start_monitoring(self):
        """Start monitoring all sites"""
        print("🚀 Starting Simple Requests Automation...")
        
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
    automation = SimpleAutomation()
    automation.start_monitoring()
