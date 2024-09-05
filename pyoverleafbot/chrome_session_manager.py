from path_finder import find_chrome_path
import json
import os
import subprocess

def persistent_chrome_session():
    chrome_path = find_chrome_path()
    cur_dir = os.getcwd()
    chrome_profile_dir = os.path.join(cur_dir, r'chromeprofile')
    if not os.path.exists(chrome_profile_dir):
        os.makedirs(chrome_profile_dir)

    config_path = os.path.join(cur_dir, f"config.json")

    with open(config_path, 'r') as f:
        config = json.load(f)

    config["chrome_path"] = chrome_path
    config["chrome_profile_dir"] = chrome_profile_dir
    chrome_port = config["chrome_port"]
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    # print(config)
    cmd = [
        os.path.join(chrome_path, "chrome.exe"), 
        f"--remote-debugging-port={chrome_port}", 
        f"--user-data-dir={chrome_profile_dir}"
        ]
    try:
        subprocess.Popen(cmd)
    except Exception as e:
        print(f"Error: {e}")    

# persistent_chrome_session()