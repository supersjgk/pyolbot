import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import keyring
from driver_manager import get_set_chromedriver
import re
import csv
import argparse
# from chrome_session import persistent_chrome_session

def setup_driver(config, update=False):
    chromedriver_path = config["chromedriver_path"]
    chrome_profile_dir = config["chrome_profile_dir"]
    
    if "chromedriver.exe" not in chromedriver_path or update:
        get_set_chromedriver()
    chrome_options = Options()

    # to connect to an existing chrome tab
    # chrome_port_val = "127.0.0.1:" + str(chrome_port)
    # print(chrome_port_val)
    # chrome_options.add_experimental_option("debuggerAddress", chrome_port_val)
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument(f"user-data-dir={chrome_profile_dir}")

    # Disable Chrome's Save Password popup
    pref = {
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False
    }
    
    chrome_options.add_experimental_option("prefs", pref)

    service = Service(chromedriver_path)
    # global driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Uncomment if you want to use an already opened chrome browser tab
# def open_persistent_chrome(config):
#     persistent_chrome_session()
    
def check_login():
    def get_credentials(target_name):
        try:
            cred = keyring.get_credential(target_name, "")
            email = cred.username
            passwd = cred.password
            return email, passwd
        except Exception as e:
            raise ValueError(f"Error: {e}")

    wait = WebDriverWait(driver, 2)
    target_name = "OverleafBot"

    try:
        cookie = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/button[1]')))
        cookie.click()
        time.sleep(0.5)
    except:
        print("Cookies enabled...")

    try:
        login_btn = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, "//li[@class='secondary']/a[contains(@href, '/login')]")))
        print("Logged out...")
        login_btn.click()
        time.sleep(1)

        email, passwd = get_credentials(target_name)

        email_field = wait.until(EC.element_to_be_clickable(driver.find_element(By.ID, "email")))
        email_field.click()
        email_field.send_keys(email)
        time.sleep(0.5)

        password_field = wait.until(EC.element_to_be_clickable(driver.find_element(By.ID, "password")))
        password_field.click()
        password_field.send_keys(passwd)
        time.sleep(0.5)

        click_login = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/form/div[5]/button')))
        click_login.click()
        print("Logged in successfully...")
        time.sleep(1)

    except:
        print(f"Logged in already...")

def get_shared_projects():
    wait = WebDriverWait(driver, 2)
    shared_prj = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//*[@id="project-list-root"]/div/div[1]/div[1]/aside/ul/li[3]/button')))
    shared_prj.click()

    prj_table_path = '//*[@id="project-list-root"]/div/div[2]/div[6]/div/div/table/tbody'
    table_body = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, prj_table_path)))
    rows = table_body.find_elements(By.TAG_NAME, 'tr')
    data = []
    i = 1
    for row in rows:
        project_cell = row.find_element(By.CLASS_NAME, 'dash-cell-name')
        link = project_cell.find_element(By.TAG_NAME, 'a')
        project_name = link.text
        project_id = re.search(r'/project/([^/]+)', link.get_attribute('href')).group(1)
        data.append([i, project_name, project_id])
        i += 1

    with open('projects.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Project Number', 'Project Name', 'Project ID'])
        writer.writerows(data)
    print("Project List extracted to projects.csv...")

def select_project():
    prj = []
    with open('projects.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            prj.append(row)
        
    print("Available shared projects:")
    for i, prj_name, prj_id in prj:
        print(f"Project Number {i}: Project Name {prj_name}, Project ID {prj_id}")
    while True:
        try:
            choice = int(input("\nEnter the Project Number:"))
            if 1 <= choice <= len(prj):
                return prj[choice-1]
            else:
                print("Choose a valid project number (eg. 1,2,3...)")
        except ValueError:
            print("Enter integer...")

def open_project(current_overleaf_project_id):
    wait = WebDriverWait(driver, 2)

    prj_table_path = '//*[@id="project-list-root"]/div/div[2]/div[6]/div/div/table/tbody'
    table_body = wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, prj_table_path)))
    rows = table_body.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        project_cell = row.find_element(By.CLASS_NAME, 'dash-cell-name')
        link = project_cell.find_element(By.TAG_NAME, 'a')
        project_id = re.search(r'/project/([^/]+)', link.get_attribute('href')).group(1)
        if project_id == current_overleaf_project_id:
            link.click()
            time.sleep(1)
            break
    print("Project Opened successfully...")

# Gets only the line numbers, not the content
def get_lines():
    wait = WebDriverWait(driver, 1)
    line_num_element = wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, '#ide-root > div.ide-react-main > div > div > div:nth-child(3) > div > div.ide-react-panel > div > div:nth-child(1) > div > div > div > div > div > div.cm-scroller > div.cm-gutters > div.cm-gutter.cm-lineNumbers')))
    line_nums = line_num_element.find_elements(By.CLASS_NAME, 'cm-gutterElement')
    num_lines = len(line_nums)-1
    print(f"Total number of lines in this project: {num_lines}")
    return line_nums, num_lines

# Selects the beginning of a random line number
def select_random_number_line(line_nums, num_lines):
    choice = random.randint(1, num_lines)
    print(f"Selected line number {choice}...")
    line_nums[choice].click()

# Gets the lines with content
def get_content():
    wait = WebDriverWait(driver, 1)
    body_element = wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, '#ide-root > div.ide-react-main > div > div > div:nth-child(3) > div > div.ide-react-panel > div > div:nth-child(1) > div > div > div > div > div > div.cm-scroller > div.cm-content.cm-lineWrapping')))
    lines_element = body_element.find_elements(By.CLASS_NAME, 'cm-line')
    num_lines = len(lines_element)
    non_empty_lines = [line for line in lines_element if line.text.strip()]
    return non_empty_lines, num_lines

# Selects random position of a random line
def select_random_line_content(non_empty_lines, num_lines):
    choice = random.randint(0, num_lines - 1)
    selected_line = non_empty_lines[choice]
    print(f"Selected line {choice+1}...")

    script = """
    var range = document.createRange();
    var selection = window.getSelection();
    var textNode = arguments[0].childNodes[0];
    var length = textNode.textContent.length;
    var randonOffset = Math.floor(Math.random() * length);
    range.setStart(textNode, randomOffset);
    range.collapse(true);
    selection.removeAllRanges();
    seletion.addRange(range);
    """
    driver.execute_script(script, selected_line)
    print(f"Movied on line {choice+1}")

def click_randomly():
    pass

def load_config():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(cur_dir, f"config.json")

    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def update_config(config):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(cur_dir, f"config.json")

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    print("Config.json updated...")

def main():
    parser = argparse.ArgumentParser(description='Overleaf automation.')
    parser.add_argument('--project_id', required=False, help='Overleaf Project ID')
    parser.add_argument('--duration', required=False, help='Period of time to appear active (in minutes)')
    parser.add_argument('--min_change_time', required=False, default=5, type=int, help='Minimum number of seconds after which line will change')
    parser.add_argument('--max_change_time', required=False, default=10, type=int, help='Maximum number of seconds after which line will change')
    args = parser.parse_args()
    config = load_config()    

    # open_persistent_chrome(config)
    global driver
    driver = setup_driver(config, update=False)
    duration = 60*args.duration if args.duration else 300
    
    try:
        driver.get("https://www.overleaf.com")
        check_login()
        time.sleep(1)
        get_shared_projects()
        if args.project_id:
            config["current_overleaf_project_id"] = args.project_id
        else:
            _, _, project_id = select_project()
            config["current_overleaf_project_id"] = project_id
        
        update_config(config)
        time.sleep(0.5)
        open_project(config["current_overleaf_project_id"])
        # line_nums, num_lines = get_lines()
        # cur_time = time.time()
        # while time.time() < cur_time + float(duration):
        #     select_random_number_line(line_nums, num_lines)
        #     time.sleep(random.randint(args.min_change_time, args.max_change_time))

        non_empty_lines, num_lines = get_content()
        cur_time = time.time()
        while time.time() < cur_time + float(duration):
            select_random_line_content(non_empty_lines, num_lines)
            time.sleep(random.randint(args.min_change_time, args.max_change_time))
        # print("done...")
        # time.sleep(20)

    except Exception as e:
        print(f"Error: {e}")
    # finally:
    #     driver.quit()

if __name__ == "__main__":
    """
        Usage: 
        - If you want to be prompted to select the projects in terminal:
            python script.py
        - If you know the Overleaf project ID, run:
            python script.py --project_id <Project ID>
        - To run it for <x> minutes (default 5), use argument:
            --duration <x>
        - This code repeatedly selects a random line (every 5 to 10 seconds) to appear active/busy. To override default values, use arguments:
            --min_change_time <min_seconds> --max_change_time <max_seconds>
    """
    main()
