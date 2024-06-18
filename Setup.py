from Utils.Config_reader import Config, Target

config = Config()
target = Target()

with open("setup.txt", "r") as steup:
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
            elif key == "user":
                target.user = value
            elif key == "password":
                target.password = value
            elif key == "mac_address":
                target.mac_address = value
            elif key == "ipv4":
                if value.upper() == "AUTO":
                    target.set_auto_ip()
                else:
                    target.ipv4 = value
            else:
                print("Invalid key: ", key)

config.add_target(target)
Config.save(config, "config.json")
print("Config file saved")