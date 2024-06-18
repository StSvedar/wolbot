import subprocess

def check_status(ipv4_target, delay=2):
    response = subprocess.run(f"ping -w {delay} {ipv4_target}", shell=True)
    return response.returncode == 0

def wake_on_lan(mac_target):
    response = subprocess.run(f"wakeonlan {mac_target}", shell=True)
    return response.returncode == 0

def windows_shutdown(ipv4_target, user, password, delay=1):
    response = subprocess.run(f"net rpc -S {ipv4_target} -U {user}%{password} shutdown -f -t {delay}", shell=True)
    return response.returncode == 0