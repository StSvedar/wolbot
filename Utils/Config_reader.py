import json
import re
from Utils.Shell_manager import resolve_ip

SETUP_FILE = "setup.txt"
CONFIG_FILE = "config.json"

def check_mac(mac):
    if not re.match(r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})", mac):
        raise ValueError("Invalid mac address : {mac} (format : 00:00:00:00:00:00)")

def check_ipv4(ipv4):
    if not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ipv4):
        raise ValueError("Invalid ipv4 address : {ipv4}")
    
def check_os(os):
    if os.upper() not in ["WINDOWS", "LINUX"]:
        raise ValueError("Invalid os : {os} (chose between windows and linux)")

class Config:
    def __init__(self, prefix=None, token=None):
        self.prefix = prefix
        self.token = token
        self.targets = []

    def __str__(self):
        return f"prefix: {self.prefix}, token: {self.token}, targets: {self.targets}"
    
    def __repr__(self):
        return f"Config({self.prefix}, {self.token}, {self.targets})"
    
    def save(self, file_name):
        with open(file_name, "w") as file:
            data = {
                "prefix": self.prefix,
                "token": self.token,
                "targets": [target.__dict__ for target in self.targets]
            }
            json.dump(data, file, indent=4)

    def load(self, file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
            self.prefix = data["prefix"]
            self.token = data["token"]
            self.targets = [Target(target["name"], target["os"], target["user"], target["password"], target["mac_address"], target["_ipv4"]) for target in data["targets"]]

    def add_target(self, target):
        self.targets.append(target)

    def remove_target(self, target):
        self.targets.remove(target)

    def get_target(self, index):
        return self.targets[index]
    
    def is_complete(self):
        return all([self.prefix, self.token]) and all([target.is_complete() for target in self.targets])
            

class Target:   # TODO : check inputs with regex
    def __init__(self=None, name=None, user=None, os=None, password=None, mac_address=None, ipv4=None):
        self.name = name
        self.os = os
        self.user = user
        self.password = password
        self.mac_address = mac_address
        self.ipv4 = ipv4

    @property
    def ipv4(self):
        return self._ipv4
    
    @ipv4.setter
    def ipv4(self, value):
        if value == "AUTO":
            self.set_auto_ip()
        else:
            self._ipv4 = value

    def __str__(self):
        return f"name: {self.name}, os: {self.os}, ipv4: {self.ipv4}, mac_address: {self.mac_address}, user: {self.user}, password: {self.password}"
    
    def __repr__(self):
        return f"Target({self.name}, {self.os}, {self.ipv4}, {self.mac_address}, {self.user}, {self.password})"
    
    def set_auto_ip(self):
        if self.mac_address == None:
            raise IP_resolution_error("IP address cannot be resolved without mac address")
        self.ipv4 = resolve_ip(self.mac_address)
        if self.ipv4 == None:
            raise IP_resolution_error("Could not resolve the ip address")
        
    def is_complete(self):
        return all([self.name, self.os, self.user, self.password, self.mac_address, self.ipv4])

class IP_resolution_error(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"IP_resolution_error: {self.message}"
    
def setupBot(config: Config): 
    target = Target()
    with open(SETUP_FILE, "r") as steup:
        for line in steup:
            if not line.startswith("#") and not line.strip() == "":
                key, value = line.split("->")
                key = key.strip()
                value = value.strip()
                if value.upper() == "NONE" or value == "":
                    value = None
                
                # Set the values
                if key == "prefix":
                    config.prefix = value

                elif key == "token":
                    config.token = value

                elif key == "name":
                    target.name = value


                elif key == "os":
                    check_os(value)
                    target.os = value

                elif key == "user":
                    target.user = value

                elif key == "password":
                    target.password = value

                elif key == "mac_address":
                    check_mac(value)
                    target.mac_address = value

                elif key == "ipv4":
                    if value.upper() == "AUTO":
                        target.ipv4 = value.upper()
                    else:
                        check_ipv4(value)
                        target.ipv4 = value
                else:
                    raise ValueError(f"Invalid key : {key}")
    config.add_target(target)
    config.save(CONFIG_FILE)