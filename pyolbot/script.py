# import argparse
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def setup_driver(chromedriver_path):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def check_login(driver):
    try:
        login_btn = driver.find_element(By.XPATH, "//li[@class='secondary']/a[contains(@href, '/login')]")
        print("Logged out")

        driver.get("https://www.overleaf.com/login")

        google_login = driver.find_element(By.XPATH, "//a[contains(@href, '/auth/google?intent=sign_in')]")
        print("Logging with Google")

        google_login.click()

        time.sleep(10)

    except Exception as e:
        print(f"Logged in or exception {e}")
        
def click_randomly(driver, min_cursor_change, max_cursor_change):
    body = driver.find_element(By.TAG_NAME, 'body')
    actions = ActionChains(driver)
    viewport_width = driver.execute_script("return window.innerWidth")
    viewport_height = driver.execute_script("return window.innerHeight")

    while True:
        x = random.randint(0, viewport_width-1)
        y = random.randint(0, viewport_height-1)
        actions.move_to_element_with_offset(body, x, y).click().perform()

        time.sleep(random.uniform(min_cursor_change, max_cursor_change))

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--config', type=str, required=True, help="Path to config file")
    # args = parser.parse_args()
    # config = load_config(args.config)
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(cur_dir, f"config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)

    driver = setup_driver(config["chromedriver_path"])
    min_cursor_change, max_cursor_change = config["min_cursor_change"], config["max_cursor_change"]
    
    try:
        driver.get("https://www.overleaf.com")
        check_login(driver)
        time.sleep(10)
        click_randomly(driver, min_cursor_change, max_cursor_change)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

