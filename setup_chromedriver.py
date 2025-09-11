import os
import requests
import zipfile
import platform
from pathlib import Path

def download_chromedriver():
    """Download ChromeDriver for the current platform"""
    print("🔧 Setting up ChromeDriver...")
    
    # Check if chromedriver already exists
    if os.path.exists("chromedriver.exe") or os.path.exists("chromedriver"):
        print("✅ ChromeDriver already exists")
        return True
    
    try:
        # Determine platform
        system = platform.system().lower()
        if system == "windows":
            driver_name = "chromedriver.exe"
            platform_name = "win32"
        elif system == "linux":
            driver_name = "chromedriver"
            platform_name = "linux64"
        elif system == "darwin":  # macOS
            driver_name = "chromedriver"
            platform_name = "mac64"
        else:
            print(f"❌ Unsupported platform: {system}")
            return False
        
        # Get latest ChromeDriver version
        print("📥 Getting latest ChromeDriver version...")
        version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        response = requests.get(version_url)
        if response.status_code != 200:
            print("❌ Failed to get ChromeDriver version")
            return False
        
        version = response.text.strip()
        print(f"📦 ChromeDriver version: {version}")
        
        # Download ChromeDriver
        download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_{platform_name}.zip"
        print(f"📥 Downloading from: {download_url}")
        
        response = requests.get(download_url)
        if response.status_code != 200:
            print("❌ Failed to download ChromeDriver")
            return False
        
        # Save and extract
        with open("chromedriver.zip", "wb") as f:
            f.write(response.content)
        
        print("📦 Extracting ChromeDriver...")
        with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
            zip_ref.extractall(".")
        
        # Make executable on Unix systems
        if system != "windows":
            os.chmod(driver_name, 0o755)
        
        # Clean up
        os.remove("chromedriver.zip")
        
        print(f"✅ ChromeDriver setup completed: {driver_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up ChromeDriver: {e}")
        return False

if __name__ == "__main__":
    download_chromedriver()
