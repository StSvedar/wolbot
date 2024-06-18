import json
from Shell_manager import resolve_ip

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
            self.targets = [Target(target["user"], target["password"], target["mac_address"], target["ipv4"]) for target in data["targets"]]

    def add_target(self, target):
        self.targets.append(target)
            

class Target:
    def __init__(self=None, user=None, password=None, mac_address=None, ipv4=None):
        self.user = user
        self.password = password
        self.mac_address = mac_address
        if self.ipv4 is None and mac_address is not None:
            self.ipv4 = resolve_ip(mac_address)
        else:
            self.ipv4 = ipv4
        
    def __str__(self):
        return f"ipv4: {self.ipv4}, mac_address: {self.mac_address}, user: {self.user}, password: {self.password}"
    
    def __repr__(self):
        return f"Target({self.ipv4}, {self.mac_address}, {self.user}, {self.password})"
