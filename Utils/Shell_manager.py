import subprocess
import re

def check_status(ipv4_target: str, delay=2):
    response = subprocess.run(f"ping -w {delay} {ipv4_target}", shell=True)
    return response.returncode == 0

def wake_on_lan(mac_target: str):
    response = subprocess.run(f"wakeonlan {mac_target}", shell=True)
    return response.returncode == 0

def windows_shutdown(ipv4_target: str, user: str, password: str, delay=1):
    response = subprocess.run(f"net rpc -S {ipv4_target} -U {user}%{password} shutdown -f -t {delay}", shell=True)
    return response.returncode == 0

def resolve_ip(mac_target: str):
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

class IP_resolution_error(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"IP_resolution_error: {self.message}"