import os
from config import mac_address

def wake_on_lan(mac_address):
    print(f"Waking up {mac_address}")
    os.system(f"wakeonlan {mac_address}")