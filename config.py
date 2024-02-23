import configparser
import os

class Config():
    def __init__(self, conf_file):
        self.c=configparser.ConfigParser()
        self.c.read("conf_file")
        print(f"Configuration file set to {os.path.abspath(conf_file)}")
        print(self.c.sections())


    def appearance(self, key):
        return self.c.get('Appearance', key) 
        
        
