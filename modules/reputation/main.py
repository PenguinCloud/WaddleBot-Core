#!/usr/bin/python3
from libs.botclasses import *
import pathlib
import re
from libs.botDBC import botDb as dbc
from libs.botConfig import botConfig as bc
from updater import update

#Const
CONFIG_FILE = pathlib.Path(__file__).parent.resolve() + "config.yml"

#TODO - setup the logger

def receiving(activity, userid, platform, interface, text: str = None, namespace:str ="global", subinterface: str = None, amount: float = 0):
    # Why are we even here bruh?
    ee = event
    ee.activity = activity
    ee.amount = amount
    ee.platform = platform
    ee.interface = interface
    ee.subInterface = subinterface
    ee.namespace = namespace
    ee.rawText = text

    # Setup dat identity yo
    id = identity
    id.id = userid
    id.platform = [platform]

    # Returning something variable phool
    msg = None
    media = None
    stdout = "dm"

    # Do we seek truth?
    if platform == "query":
        x = query(id)
        msg = x.idLookup()
    else:
        match platform:
            case "twitch":
                x = update
                x.twitch()
    
    return msg, media, stdout

class query:
    def __init__(self, userid: identity) -> None:
        self.score = 0
        self.id = userid
        self.retvars = retvars
        self.config = bc(configPath=CONFIG_FILE)
        self.config
        self.dbc = dbc(config=self.config)
    def idLookup(self):
        lookCol = "userid"
        database = "waddlebot"
    def repAlias(self, score:float=600):
        pass

