import inspect
import os
from libs.botClasses import *
from libs.botLogger import botLogger

# Why is that black van out there?
log = botLogger("waddlebot-dbc")
log.fileLogger("waddlebot-dbc.log")

abs_path = os.path.abspath((inspect.stack()[0])[1])
directory_of_1py = os.path.dirname(abs_path)

class botConfig:
    def __init__(self, configType:str = "yaml", configPath:str = "config.yml"):
        self.cpath = configPath
        match configType:
            case "yaml":
                self.config = self.__importyaml()
                log.debug("Config type is yaml")
            case _:
                self.config = self.__importyaml()

    def __importyaml(self):
        try:
            import yaml
            with open(self.cpath,'r') as thefile:
                log.debug(f"Importing {self.cpath}")
                c = yaml.load(thefile)
                thefile.close
        except Exception as err:
            log.error(err)
        return c