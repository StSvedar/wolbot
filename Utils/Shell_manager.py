import subprocess
import re

def check_status(ipv4_target, delay=2):
    response = subprocess.run(f"ping -w {delay} {ipv4_target}", shell=True)
    return response.returncode == 0

def wake_on_lan(mac_target):
    response = subprocess.run(f"wakeonlan {mac_target}", shell=True)
    return response.returncode == 0

def windows_shutdown(ipv4_target, user, password, delay=1):
    response = subprocess.run(f"net rpc -S {ipv4_target} -U {user}%{password} shutdown -f -t {delay}", shell=True)
    return response.returncode == 0

def resolve_ip(mac_target):
    # Get the arp table
    response = subprocess.run(f"arp -a", shell=True, capture_output=True)
    lines = response.stdout.decode().split("\n")    # TODO: doesn't work on windows (find the right place to raise an exception)

    # Find the line that contains the mac address
    found = False
    for line in lines:
        if mac_target.lower() in line:
            found = True
            break

    # Extract the ip address from the line
    pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    match = pattern.search(line)

    return match.group(0) if found else None