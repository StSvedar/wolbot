import json
from Utils.Shell_manager import resolve_ip

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

    def remove_target(self, target):
        self.targets.remove(target)

    def get_target(self, index):
        return self.targets[index]
    
    def is_complete(self):
        return self.prefix is not None and self.token is not None and all([target.is_complete() for target in self.targets])
            

class Target:
    def __init__(self=None, user=None, password=None, mac_address=None, ipv4=None):
        self.user = user
        self.password = password
        self.mac_address = mac_address
        self.ipv4 = ipv4
        if self.ipv4 is None and mac_address is not None:
            self.set_auto_ip()
        
    def __str__(self):
        return f"ipv4: {self.ipv4}, mac_address: {self.mac_address}, user: {self.user}, password: {self.password}"
    
    def __repr__(self):
        return f"Target({self.ipv4}, {self.mac_address}, {self.user}, {self.password})"
    
    def set_auto_ip(self):
        self.ipv4 = resolve_ip(self.mac_address)
        if self.ipv4 == None:
            raise IP_resolution_error("Could not resolve the ip address")
        
    def is_complete(self):
        return self.user is not None and self.password is not None and self.mac_address is not None and self.ipv4 is not None

class IP_resolution_error(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"IP_resolution_error: {self.message}"