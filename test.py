import os
import subprocess

def ping(host):
    response = subprocess.run(f"ping -c 1 {host}", stdout=subprocess.PIPE, shell=True)
    if response.returncode != 0:
        raise Exception(f"Error: returned {response.returncode}")
    print(response.stdout)
    return "1 received" in response.stdout.decode()

try:
    if ping("192.168.0.130"):
        print("Host is up")
    else:
        print("Host is down")
except Exception as e:
    print(e)