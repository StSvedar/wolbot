import os

def wake_on_lan(mac_address):
    os.system(f"wakeonlan {mac_address}")