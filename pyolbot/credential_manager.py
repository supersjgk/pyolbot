import keyring
import getpass
import argparse

def set_creds(target_name):
    username = input("Enter your Overleaf email (e.g., your_email@example.com): ")
    password = getpass.getpass("Enter your Overleaf password: ")

    # Store credentials in keyring
    keyring.set_password(target_name, username, password)
    print("Credentials stored in keyring...")

def delete_creds(target_name):
    pass

if __name__ == "__main__":
    target_name = "OverleafBot"
    set_creds(target_name)
