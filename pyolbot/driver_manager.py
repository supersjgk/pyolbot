import os
import sys
import io
from selenium import webdriver
import platform
import zipfile
import requests
import platform
import json

def get_chrome_version():
    try:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        version = driver.capabilities['browserVersion']
        driver.quit()
        return version
    except Exception as e:
        print(e)
        return None
    
def get_chromedriver_url():
    chrome_version = get_chrome_version()
    base_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}"
    _system_name, _system_arch = platform.system().lower(), platform.architecture()[0]
    if "win" in _system_name and "64" in _system_arch:
        syst = "win64"
    elif "win" in _system_name and "32" in _system_arch:
        syst = "win32"
    elif "linux" in _system_name:
        syst = "linux64"
    elif "mac" in _system_name and "arm" in _system_arch:
        syst = "mac-arm64"
    elif "mac" in _system_name and "x" in _system_arch:
        syst = "mac-x64"
    else:
        print("Error getting platform info..")
        sys.exit(1)
    # print(syst)
    driver_url = f"{base_url}/{syst}/chromedriver-{syst}.zip"
    return syst, driver_url

def get_set_chromedriver():
    syst, driver_url = get_chromedriver_url()
    download_dir = os.path.dirname(os.path.abspath(__file__))
    
    response = requests.get(driver_url)
    response.raise_for_status()
    
    zip_file_path = os.path.join(download_dir, f"chromedriver_{syst}.zip")
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)
    
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        z.extractall(download_dir)
    
    os.remove(zip_file_path)
    
    chromedriver_folder = os.path.join(download_dir, f"chromedriver-{syst}")
    chromedriver_filename = "chromedriver.exe" if syst.startswith("win") else "chromedriver"
    chromedriver_path = os.path.join(chromedriver_folder, chromedriver_filename)
    
    if platform.system() != "Windows":
        os.chmod(chromedriver_path, 0o755)
    
    print(f"Chromedriver installed at {chromedriver_path}...")
    
    config_path = os.path.join(download_dir, "config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    config["chromedriver_path"] = chromedriver_path
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    print("config.json updated...")


def main():
    get_set_chromedriver()

if __name__ == "__main__":
    main()