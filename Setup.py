from Utils.Config_reader import Config, setupBot, CONFIG_FILE

config = Config()
setupBot(config)
config.save(CONFIG_FILE)
del config