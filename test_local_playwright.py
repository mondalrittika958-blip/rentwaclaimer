#!/usr/bin/env python3
"""
Test Playwright automation locally
"""

import time
import logging
from advanced_automation_playwright import AdvancedAutomation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_playwright_automation():
    """Test Playwright automation locally"""
    try:
        logger.info("🚀 Starting local Playwright test...")
        
        # Create automation instance
        automation = AdvancedAutomation()
        
        # Test single site first - use the correct format from WEBSITES
        test_site = {
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
        }
        
        logger.info(f"🔍 Testing site: {test_site['name']}")
        
        # Test login
        login_success = automation.login_to_site(test_site)
        if login_success:
            logger.info("✅ Login successful!")
            
            # Test amount getting
            amount = automation.get_amount(test_site)
            if amount:
                logger.info(f"💰 Amount found: {amount}")
            else:
                logger.warning("⚠️ No amount found")
                
            # Test popup handling
            automation.handle_popup_if_present(test_site)
            
            # Test reset button
            if automation.check_reset_button(test_site):
                logger.info("🔄 Reset button found!")
                automation.click_reset_button(test_site)
            else:
                logger.info("ℹ️ No reset button available")
                
        else:
            logger.error("❌ Login failed!")
            
        # Close browser
        automation.stop_monitoring()
        logger.info("✅ Test completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_playwright_automation()
