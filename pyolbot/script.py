import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import win32cred
from driver_manager import get_set_chromedriver
from chrome_session import persistent_chrome_session

def setup_driver(chromedriver_path, chrome_port):
    get_set_chromedriver()
    chrome_options = Options()
    chrome_port_val = "localhost:" + str(chrome_port)
    chrome_options.add_experimental_option("debuggerAddress", chrome_port_val)
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def open_persistent_chrome(config):
    persistent_chrome_session()
    
def check_login(driver):
    def get_credentials(target_name):
        try:
            cred = win32cred.CredRead(target_name, win32cred.CRED_TYPE_GENERIC)
            email = cred['UserName']
            passwd = cred['CredentialBlob'].decode('utf-8')
            return email, passwd
        except Exception as e:
            raise ValueError(f"Error: {e}")

    wait = WebDriverWait(driver, 2)
    target_name = "OverleafBot"

    try:
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@class='secondary']/a[contains(@href, '/login')]")))
        print("Logged out...")
        login_btn.click()
        time.sleep(1)

        email, passwd = get_credentials(target_name)

        email_field = wait.until(EC.element_to_be_clickable(driver.find_element(By.ID, "email")))
        email_field.click()
        email_field.send_keys(email)
        time.sleep(1)

        password_field = wait.until(EC.element_to_be_clickable(driver.find_element(By.ID, "password")))
        password_field.click()
        password_field.send_keys(passwd)
        time.sleep(1)

        click_login = wait.until(EC.element_to_be_clickable(By.XPATH, "//button[contains(@class='btn-primary') and contains(@type='submit')]"))
        click_login.click()
        time.sleep(1)

    except Exception as e:
        print(f"Logged in or exception {e} during login")
        
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
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(cur_dir, f"config.json")

    with open(config_path, 'r') as f:
        config = json.load(f)

    open_persistent_chrome(config)

    driver = setup_driver(config["chromedriver_path"], config["chrome_port"])
    min_cursor_change, max_cursor_change = config["min_cursor_change"], config["max_cursor_change"]
    
    try:
        driver.get("https://www.overleaf.com")
        check_login(driver)
        print("Logged in successfully...")
        time.sleep(2)
        # click_randomly(driver, min_cursor_change, max_cursor_change)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
