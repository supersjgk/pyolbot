import winreg

def find_chrome_path():
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            chrome_path, _ = winreg.QueryValueEx(key, "Path")
            return chrome_path
    except FileNotFoundError:
        return None
    
def find_python_path():
    pass
    """
    try:
        key_path = r"SOFTWARE\Python\PythonCore"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            version_path = winreg.EnumKey(key, 0)

    except:
    """