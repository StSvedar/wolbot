
from Utils.Config_reader import Config, Target

config = Config()
target = Target()

with open("setup.txt", "r") as steup:
    for line in steup:
        if not line.startswith("#") and not line.strip() == "":
            key, value = line.split("->")
            if key.strip() == "prefix":
                config.prefix = value.strip()
            elif key.strip() == "token":
                config.token = value.strip()
            elif key.strip() == "mac_address":
                target.mac_address = value.strip()
            elif key.strip() == "ipv4":
                target.ipv4 = value.strip()
            elif key.strip() == "user":
                target.user = value.strip()
            elif key.strip() == "password":
                target.password = value.strip()
            else:
                print("Invalid key: ", key)

config.add_target(target)
Config.save(config, "config.json")
print("Config file saved")