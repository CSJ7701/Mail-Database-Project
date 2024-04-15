import configparser
import os

class Config():
    def __init__(self, conf_file):
        self.c=configparser.ConfigParser()
        self.c.read(conf_file)
        print(f"Configuration file set to {os.path.abspath(conf_file)}")

    def appearance(self, key):
        return self.c.get('Appearance', key) 
        
    def initialize(self):
        self.c["Appearance"]={'color_mode': 'dark', 'color_scheme': os.path.join("themes", "CGA.json")}
        with open('config.ini', 'w') as file:
            self.c.write(file)
