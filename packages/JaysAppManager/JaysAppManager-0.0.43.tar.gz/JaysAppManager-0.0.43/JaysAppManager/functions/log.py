from datetime import datetime
import inspect
import os
import sys
import time
import requests
import json
from .register import run_manager, get_external_ip, get_local_ip

def log(log_level, logtitle, descriptions):
    
    
    if log_level is None:
        log_level = "INFO"
    elif "debug" in log_level.lower():  
        log_level = "DEBUG"
    elif "error" in log_level.lower():  
        log_level = "ERROR"
    elif "warn" in log_level.lower():  
        log_level = "WARNING"
        
    # Get the previous frame in the stack, otherwise it would be this function
    previous_frame = inspect.currentframe().f_back
    (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)

    # Get the current time
    now = datetime.now().strftime("%m/%d %I:%M %p")

    # Extract the file name from the full path
    file_name = os.path.basename(filename)

    # Print the log message
    print(f"{now} {file_name}:{line_number} {log_level} {logtitle} {descriptions}")
    
    
    # Prepare the data
    data = {
        "logtitle": logtitle,
        "descriptions": descriptions,
        "file": filename,
        "application": "SallyBot",
        "app_version": "0.0.0", # TODO: NEed to set, but do config first.
        "python_version": sys.version,
        "log_level": log_level,
        "run_id": run_manager.get_run_id()
    }

    # Convert the data to JSON
    json_data = json.dumps(data)

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Perform the POST request
    response = requests.post("http://admin.com/log", headers=headers, data=json_data)



def ping(status=None):
    if status is None:
        status = "active"
    url = "http://admin.com/ping"
    headers = {"Content-Type": "application/json"}
    data = {
        "run_id": run_manager.get_run_id(),
        "app_name": "SallyBot",
        "local_ip": get_local_ip(),
        "external_ip": get_external_ip(),
        "status": status
    }

    while True:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        time.sleep(600)  # sleep for 10 minutes | TODO: ADd to config