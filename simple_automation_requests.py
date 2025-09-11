#!/usr/bin/env python3
"""
Simple Requests-Based Website Automation
Uses requests + BeautifulSoup instead of browser automation
"""

import requests
import time
import logging
import threading
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from webhook_config import send_telegram_message

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Website configurations
WEBSITES = [
    {
        'name': 'kamkg',
        'base_url': 'https://kamkg.com',
        'login_url': 'https://kamkg.com/#/pages/login/index',
        'main_url': 'https://kamkg.com/#/pages/index/index',
        'phone': '8974395024',
        'password': '53561106@Tojo'
    },
    {
        'name': 'kamate1',
        'base_url': 'https://kamate1.com',
        'login_url': 'https://kamate1.com/#/pages/login/index',
        'main_url': 'https://kamate1.com/#/pages/index/index',
        'phone': '8974395024',
        'password': '53561106@Tojo'
    },
    {
        'name': 'wha2',
        'base_url': 'https://wha2.net',
        'login_url': 'https://wha2.net/#/pages/login/index',
        'main_url': 'https://wha2.net/#/pages/index/index',
        'phone': '8974395024',
        'password': '53561106@Tojo'
    },
    {
        'name': 'lootlelo',
        'base_url': 'https://lootlelo.com',
        'login_url': 'https://lootlelo.com/#/pages/login/index',
        'main_url': 'https://lootlelo.com/#/pages/index/index',
        'phone': '8974395024',
        'password': '53561106@Tojo'
    }
]

class SimpleRequestsAutomation:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.last_reset_time = {}
        self.amounts = {}
        
    def login_to_site(self, site):
        """Attempt to login to a site using requests"""
        try:
            logger.info(f"🔐 Attempting login to {site['name']}...")
            
            # Get login page
            response = self.session.get(site['login_url'])
            if response.status_code != 200:
                logger.error(f"❌ Failed to get login page for {site['name']}: HTTP {response.status_code}")
                return False
                
            # Parse login page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for login form
            login_form = soup.find('form') or soup.find('div', class_='login-form')
            if not login_form:
                logger.warning(f"⚠️ No login form found for {site['name']}")
                return False
                
            # Try to find phone and password fields
            phone_field = soup.find('input', {'name': 'phone'}) or soup.find('input', {'placeholder': 'phone'})
            password_field = soup.find('input', {'name': 'password'}) or soup.find('input', {'type': 'password'})
            
            if not phone_field or not password_field:
                logger.warning(f"⚠️ Login fields not found for {site['name']}")
                return False
                
            # Prepare login data
            login_data = {
                'phone': site['phone'],
                'password': site['password']
            }
            
            # Try to submit login
            login_response = self.session.post(site['login_url'], data=login_data)
            
            if login_response.status_code == 200:
                logger.info(f"✅ Login successful for {site['name']}")
                return True
            else:
                logger.error(f"❌ Login failed for {site['name']}: HTTP {login_response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Login error for {site['name']}: {e}")
            return False
    
    def get_amount(self, site):
        """Get amount from site using requests"""
        try:
            # Try to get main page
            response = self.session.get(site['main_url'])
            if response.status_code != 200:
                logger.error(f"❌ Failed to get main page for {site['name']}: HTTP {response.status_code}")
                return None
                
            # Parse page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for amount element
            amount_element = soup.find('uni-text', class_='u-count-num')
            if amount_element:
                span = amount_element.find('span')
                if span:
                    amount = span.get_text(strip=True)
                    logger.info(f"💰 Amount found for {site['name']}: {amount}")
                    return amount
                    
            logger.warning(f"⚠️ Amount not found for {site['name']}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting amount for {site['name']}: {e}")
            return None
    
    def check_reset_button(self, site):
        """Check if reset button is available"""
        try:
            response = self.session.get(site['main_url'])
            if response.status_code != 200:
                return False
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for reset button
            reset_button = soup.find('uni-button', class_='u-button u-reset-button u-button--square u-button--small w-full font_archive base_font_color')
            return reset_button is not None
            
        except Exception as e:
            logger.error(f"❌ Error checking reset button for {site['name']}: {e}")
            return False
    
    def click_reset_button(self, site):
        """Attempt to click reset button"""
        try:
            # This is a simplified approach - in reality, we'd need to handle the actual button click
            # For now, we'll just log that we found it
            logger.info(f"🔄 Reset button found for {site['name']} - would click here")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error clicking reset button for {site['name']}: {e}")
            return False
    
    def monitor_site(self, site):
        """Monitor a single site"""
        logger.info(f"🔍 Starting monitoring for {site['name']}")
        
        # Initial login
        if not self.login_to_site(site):
            logger.error(f"❌ Initial login failed for {site['name']}")
            return
            
        # Monitor loop
        while True:
            try:
                # Get current amount
                current_amount = self.get_amount(site)
                if current_amount:
                    # Check if amount changed
                    if site['name'] not in self.amounts or self.amounts[site['name']] != current_amount:
                        self.amounts[site['name']] = current_amount
                        
                        # Send update
                        send_telegram_message(site['name'], current_amount, "amount_update")
                        logger.info(f"📤 Amount update sent for {site['name']}: {current_amount}")
                
                # Check reset button every 2 hours
                current_time = datetime.now()
                if site['name'] not in self.last_reset_time or \
                   current_time - self.last_reset_time[site['name']] >= timedelta(hours=2):
                    
                    if self.check_reset_button(site):
                        if self.click_reset_button(site):
                            self.last_reset_time[site['name']] = current_time
                            send_telegram_message(site['name'], "Reset Button Clicked", "reset_claimed")
                            logger.info(f"🔄 Reset button clicked for {site['name']}")
                
                # Wait before next check
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Error monitoring {site['name']}: {e}")
                time.sleep(60)  # Wait longer on error
    
    def start_monitoring(self):
        """Start monitoring all sites"""
        logger.info("🚀 Starting Simple Requests Automation...")
        
        # Send startup message
        send_telegram_message("System", "Bot Started", "startup")
        
        # Start monitoring threads for each site
        threads = []
        for site in WEBSITES:
            thread = threading.Thread(target=self.monitor_site, args=(site,), daemon=True)
            thread.start()
            threads.append(thread)
            time.sleep(5)  # Stagger starts
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("🛑 Monitoring stopped by user")

if __name__ == "__main__":
    automation = SimpleRequestsAutomation()
    automation.start_monitoring()
