import json
import re
from Utils.Shell_manager import resolve_ip, IP_resolution_error

SETUP_FILE = "setup.txt"
CONFIG_FILE = "config.json"

def check_mac(mac: str):
    if not re.match(r"([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})", mac):
        raise ValueError(f"Invalid mac address : {mac} (format : 00:00:00:00:00:00)")

def check_ipv4(ipv4: str):
    if not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ipv4):
        raise ValueError(f"Invalid ipv4 address : {ipv4}")
    
def check_os(os: str):
    if os.upper() not in ["WINDOWS", "LINUX"]:
        raise ValueError(f"Invalid os : {os} (chose between windows and linux)")

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
        if self._ipv4.upper() == "AUTO":
            if not self._mac_address:
                raise ValueError("No mac address to resolve ipv4")
            try:
                ipv4 = resolve_ip(self._mac_address)
            except IP_resolution_error as e:
                raise ValueError(e)
            check_ipv4(ipv4)
            return ipv4
        return self._ipv4
    
    @ipv4.setter
    def ipv4(self, value:str):
        if value.upper() == "AUTO":
            self._ipv4 = value
            return
        check_ipv4(value)
        self._ipv4 = value

    @property
    def mac_address(self):
        return self._mac_address
    
    @mac_address.setter
    def mac_address(self, value:str):
        check_mac(value)
        self._mac_address = value

    @property
    def os(self):
        return self._os
    
    @os.setter
    def os(self, value:str):
        check_os(value)
        self._os = value

    def __str__(self):
        return f"name: {self.name}, os: {self.os}, ipv4: {self.ipv4}, mac_address: {self.mac_address}, user: {self.user}, password: {self.password}"
    
    def __repr__(self):
        return f"Target({self.name}, {self.os}, {self.ipv4}, {self.mac_address}, {self.user}, {self.password})"
        
    def is_complete(self):
        return all([self.name, self.os, self.user, self.password, self.mac_address, self.ipv4])

class Config:
    def __init__(self, prefix=None, token=None):
        self.prefix = prefix
        self.token = token
        self.default_target:Target = None
        self.targets:Target = []

    def __str__(self):
        return f"prefix: {self.prefix}, token: {self.token}, targets: {self.targets}"
    
    def __repr__(self):
        return f"Config({self.prefix}, {self.token}, {self.targets})"
    
    def save(self, file_name):
        with open(file_name, "w") as file:
            data = {
                "prefix": self.prefix,
                "token": self.token,
                "default_target": self.default_target.name if self.default_target else "None",
                "targets": [target.__dict__ for target in self.targets]
            }
            json.dump(data, file, indent=4)

    def load(self, file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
            self.prefix = data["prefix"]
            self.token = data["token"]
            default_target_name = data["default_target"]
            self.targets = [Target(target["name"], target["user"], target["_os"], target["password"], target["_mac_address"], target["_ipv4"]) for target in data["targets"]]
        if default_target_name != "None":
            self.default_target = self.get_target_by_name(default_target_name)

    def add_target(self, target):
        self.targets.append(target)

    def remove_target(self, target:Target):
        if target is self.default_target:
            self.default_target = None
        self.targets.remove(target)

    def set_default_target(self, target_name):
        target = self.get_target_by_name(target_name)
        if target is None:
            raise ValueError(f"Deault target not found : {target_name}")
        self.default_target = target

    def get_target(self, index):
        return self.targets[index]
    
    def get_target_by_name(self, name):
        for target in self.targets:
            if target.name == name:
                return target
        return None
    
    def is_complete(self):
        return all([self.prefix, self.token]) and all([target.is_complete() for target in self.targets])
