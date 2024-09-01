import winreg

def find_chrome_path():
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            chrome_path, _ = winreg.QueryValueEx(key, "Path")
            return chrome_path
    except FileNotFoundError:
        return None