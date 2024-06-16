import os
import subprocess

def ping(host):
    response = subprocess.run(f"ping -c 1 {host}", stdout=subprocess.PIPE, shell=True)
    return response.returncode == 0

def wake_on_lan(mac_address):
    os.system(f"wakeonlan {mac_address}")