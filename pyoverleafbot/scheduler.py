import win32com.client
import argparse
from path_finder import find_python_path
import os

"""
    In progress...
"""

def create_task(project_id):
    try:
        # Connect to Task Scheduler
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        root_dir = scheduler.GetFolder('\\')

        # Define the task
        task_def = scheduler.NewTask(0)
        task_def.RegistrationInfo.Description = 'Overleaf Bot'
        task_def.Principal.UserId = 'SYSTEM'
        task_def.Principal.LogonType = 3  # Logon as a service

        # Create daily trigger
        trigger = task_def.Triggers.Create(1)  # 1 for Daily trigger
        trigger.StartBoundary = '2024-09-05T01:07:00'  # Set to the desired start time

        # Define script path and action
        cur_dir = os.getcwd()
        script_path = os.path.join(cur_dir, 'script.py')
        python_path = find_python_path()

        exec_action = task_def.Actions.Create(0)  # 0 for Execute action
        exec_action.Path = python_path
        exec_action.Arguments = f"{script_path} --project_id {project_id}"

        # Configure task settings
        settings = task_def.Settings
        settings.StartWhenAvailable = True
        settings.StopIfGoingOnBatteries = False
        settings.DisallowStartIfOnBatteries = False
        settings.RunOnlyIfNetworkAvailable = True # connect
        # settings.RunWithHighestPrivileges = True

        # Register the task
        root_dir.RegisterTaskDefinition(
            'Overleaf Bot',
            task_def,
            6,  # Replace if exists
            None,  # SYSTEM (no password needed for SYSTEM account)
            None,  # No password required for SYSTEM account
            3  # Logon as a service
        )
        print('Task created successfully.')

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_id', required=True, help='Enter your Overleaf Project ID')
    args = parser.parse_args()
    create_task(args.project_id)
