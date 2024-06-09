from datetime import datetime
import json
import os
import random
import socket
import sys

import requests

from JaysAppManager.functions.RunManager import RunManager




run_manager = RunManager()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org')
        external_ip = response.text
    except Exception:
        external_ip = 'Unable to get external IP'
    return external_ip

x = 0

def register(app_name):
    global x
    
    if not isinstance(app_name, str):
        return False
    
    run_manager.set_run_id()
    run_id = run_manager.get_run_id()
    local_ip = get_local_ip()
    external_ip = get_external_ip()
    now = datetime.now()

    print(f"run_id {run_id} | app_name {app_name} | local_ip {local_ip} | external_ip {external_ip}")

    # Prepare the data
    data = {
        "run_id": run_id,
        "app_name": app_name,
        "local_ip": local_ip,
        "external_ip": external_ip
    }

    # Convert the data to JSON
    json_data = json.dumps(data)

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Perform the POST request
    response = requests.post("http://admin.com/register", headers=headers, data=json_data)

    status_code = response.status_code

    if status_code == 201:
        os.environ['run_id'] = run_id
        # add_ping_entry(run_id, app_name, local_ip, external_ip, now, 'Registered')
        return True
    else:
        print(response.text)
        x += 1
        print(f"Attempt {x} failed")
        if x < 5:
            register()
        else:
            print("Cannot register app")
            sys.exit()


