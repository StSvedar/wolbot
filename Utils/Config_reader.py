import json

class Config:
    def __init__(self, prefix=None, token=None):
        self.prefix = prefix
        self.token = token
        self.targets = []

    def load(self, file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
            self.prefix = data["prefix"]
            self.token = data["token"]
            self.targets = [Target(target["ipv4"], target["mac_address"], target["user"], target["password"]) for target in data["targets"]]

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

    def add_target(self, target):
        self.targets.append(target)
            

class Target:
    def __init__(self=None, ipv4=None, mac_address=None, user=None, password=None):
        self.ipv4 = ipv4
        self.mac_address = mac_address
        self.user = user
        self.password = password
        
    def __str__(self):
        return f"ipv4: {self.ipv4}, mac_address: {self.mac_address}, user: {self.user}, password: {self.password}"
    
    def __repr__(self):
        return f"Target({self.ipv4}, {self.mac_address}, {self.user}, {self.password})"
