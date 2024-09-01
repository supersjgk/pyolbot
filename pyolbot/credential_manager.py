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
    cred = keyring.get_credential(target_name, "")
    username = cred.username
    keyring.delete_password(target_name, username)
    print("Credentials deleted...")

def main():
    parser = argparse.ArgumentParser(description="Credential Manager for Overleaf Bot")
    subparsers = parser.add_subparsers(dest="command")
    #setting subparser
    setp = subparsers.add_parser('set', help='Set Credentials')
    setp.add_argument('target_name')
    #deleting subparser
    delp = subparsers.add_parser('delete', help='Delete Credentials')
    delp.add_argument('target_name')

    args = parser.parse_args()

    if args.command == 'set':
        set_creds(args.target_name)
    elif args.command == 'delete':
        delete_creds(args.target_name)
    else:
        args.print_help()

if __name__ == "__main__":
    # target_name = "OverleafBot"
    """
        Usage: python credential_manager.py set/delete OverleafBot
    """
    main()
