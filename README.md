# Overleaf Automation Bot (pyolbot)

### Overview
pyolbot is built to help users appear active on collaborative Overleaf projects. It automates iinteractions with Overleaf.

### Tech Stack
- Python
- Selenium

### What can this be used for?
- **For PhD Students:** Helps manage stress
- **Coffee Break:** Set up the bot to run during breaks to keep your presence active.
- **Scheduled Runs:** Schedule the bot to run at specific times to maintain activity on projects.

### Why use Selenium rather than simple pyautogui?
- Selenium is an automation tool
- Selenium can interact directly with web applications in any browser
- Selenium provides high level interaction with the web elements
- Selenium can be used for web scraping
- Selenium scripts can be used in Headless Mode

### Implementations
- Platforms:
    - [x] Windows
        - Robust Login:
            - [x] Windows Credential Manager + Store session information for faster login
            - [ ] Gmail
        - Broswers:
            - [x] Chrome
            - [ ] Others
        - Scheduling:
            - [ ] Scheduled Runs when power on (logged in/logged out)
            - [ ] Scheduled Runs when power off
        - Functionalities:
            - [x] Fully automated
            - [x] Manage credentials securely
            - [x] Select project you want to work on
            - [x] Appear active
    - [ ] Linux (in progress)
    - [ ] Mac (who uses Mac?)
