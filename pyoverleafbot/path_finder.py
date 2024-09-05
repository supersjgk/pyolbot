import winreg
import os
import json
    
def find_chrome_path():
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            chrome_path, _ = winreg.QueryValueEx(key, "Path")
            return chrome_path
    except FileNotFoundError:
        return None
    finally:
        curdir = os.getcwd()
        config_path = os.path.join(curdir, f"config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        config["chrome_path"] = chrome_path
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    
def find_python_path():
    try:
        key_path = r"SOFTWARE\Python\PythonCore"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            i = 0
            versions = []
            while True:
                try:
                    version = winreg.EnumKey(key, i)
                    versions.append(version)
                    i += 1
                except OSError:
                    break
        for version in versions:
            try:
                version_path = f"{key_path}\\{version}\\InstallPath"
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, version_path) as version_key:
                    install_path, _ = winreg.QueryValueEx(version_key, "")
                    python_path = os.path.join(install_path, "python.exe")
                    if os.path.isfile(python_path):
                        return python_path

            except Exception as e:
                continue
        return None
    except Exception as e:
        print(f'{e}')
    finally:
        curdir = os.getcwd()
        config_path = os.path.join(curdir, f"config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        config["python_path"] = python_path
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

# print(find_python_path())