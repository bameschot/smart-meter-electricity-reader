import configparser
import json

configFile = "config.ini"

class ConfigManager:
    def __init__(self):
        self.httpServerEnabled = True
        self.refreshRateMs = 2000
        self.apiKey = None
        
    def load(self):
        config = configparser.ConfigParser()
        config.read(configFile)
        self.httpServerEnabled = bool(config['SR']['httpServerEnabled'])
        self.refreshRateMs = int(config['SR']['refreshRateMs'])
        self.apiKey = config['SR']['apiKey']
        
        print("Loaded config")
        print(json.dumps(self.__dict__,indent=2))
    
    
    