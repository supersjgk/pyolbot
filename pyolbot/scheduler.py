import win32com.client
import argparse
from path_finder import find_python_path

"""
    In Progress...
"""

def create_task():
    scheduler = win32com.client.Dispatch('Scheduler.Service')
    scheduler.Connect()
    root_dir = scheduler.GetFolder('\\')

    taskDef = scheduler.NewTask(0)
    taskDef.RegistrationInfo.Description = 'Overleaf Bot'
    taskDef.Principal.UserId = 'System'
    taskDef.Principal.LogonType = 3

    trigger = taskDef.Triggers.Create(1) # run daily
    trigger.StartBoundary = '2024-09-03T00:30:00' # 12:30 am

    execAction = taskDef.Actions.Create(0) # execute
    execAction.path = find_python_path()
    execAction.arguments = 'script.py'

    # settings
    taskDef.Settings.StartWhenAvailable = True
    taskDef.Settings.AllowStartIfOnBatteries = True
    taskDef.Settings.DontStopIfGoingOnBatteries = True
    taskDef.Settings.DisallowStartIfOnBatteries = False
    taskDef.Settings.RunOnlyIfNetworkAvailable = False
    taskDef.Settings.RunWithHighestPrivileges = True
    
    root_dir.RegisterTaskDefinition(
        'Overleaf Bot',
        taskDef,
        6,  # Replace if exists
        None,  # current user
        None,  # current user
        3   # Logon interactively
    )
