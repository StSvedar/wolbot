import os
import subprocess

def check_status(host, delay=2):
    response = subprocess.run(f"ping -w {delay} {host}", stdout=subprocess.PIPE, shell=True)
    return response.returncode == 0

def wake_on_lan(mac_address):
    response = subprocess.run(f"wakeonlan {mac_address}", shell=True)
    return response.returncode == 0

def windows_shutdown(host, user, password, delay=0):
    response = subprocess.run(f"net rpc -S {host} -U {user}%{password} shutdown -f -t {delay}", shell=True)
    return response.returncode == 0