import inspect
import os
from libs.botClasses import *

abs_path = os.path.abspath((inspect.stack()[0])[1])
directory_of_1py = os.path.dirname(abs_path)

class botConfig:
    def __init__(self, configType:str = "yaml", configPath:str = "config.yml"):
        self.cpath = configPath
        match configType:
            case "yaml":
                self.config = self.__importyaml()
            case _:
                self.config = self.__importyaml()

    def __importyaml(self):
        try:
            import yaml
            with open(self.cpath,'r') as thefile:
                c = yaml.load(thefile)
                thefile.close
        except Exception as err:
            print(err)
        return c