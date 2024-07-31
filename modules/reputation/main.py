#!/usr/bin/python3
from libs.botclasses import *
import logging
import re


configfile = "config.yml"
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
                x.ms
    
    return msg, media, stdout

class query:
    def __init__(self, userid: identity) -> None:
        self.score = 0
        self.id = userid
        self.retvars = retvars
    def idLookup(self):
        lookCol = "userid"
        database = "waddlebot"

class update:
    def __init__(self, id: identity, events: event, dbc: webdb) -> None:
        self.score = 0
        self.id = id
        self.event = events
        self.retvars = retvars
    def twitch(self):
        match self.event.activity:
            case re.match(r"^(re-)?subscription, self.event.activity"):
                pass
            case "follow":
                pass
            case "bits":
                pass
            case "raffle":
                pass
            case "giveaway":
                pass
            case "donation":
                pass
    def discord(self):
        match self.event.activity:
            case re.match(r"^(re-)?subscription, self.event.activity"):
                pass
            case "join":
                pass
            case "boost":
                pass
            case "raffle":
                pass
            case "giveaway":
                pass
            case "donation":
                pass

    def youtube(self):
        match self.event.activity:
            case re.match(r"^(re-)?subscription, self.event.activity"):
                pass
            case "join":
                pass
            case "super-text":
                pass
            case "raffle":
                pass
            case "giveaway":
                pass
            case "donation":
                pass

    def slack(self):
        match self.event.activity:
            case re.match(r"^(re-)?subscription, self.event.activity"):
                pass
            case "join":
                pass
            case "raffle":
                pass
            case "giveaway":
                pass
            case "donation":
                pass

    def mattermost(self):
        match self.event.activity:
            case re.match(r"^(re-)?subscription, self.event.activity"):
                pass
            case "join":
                pass
            case "raffle":
                pass
            case "giveaway":
                pass
            case "donation":
                pass

class __botDb:
    def __init__(self):
        self.db = webdb
        self.columns = None
        self.config = None
    def importDBC(self):
        try:
            import yaml
            with open(configfile,'r') as thefile:
                c = yaml.load(thefile)
                thefile.close
        except Exception as err:
            logging.error(err)
        self.config = c
        return c
    def importColumns(self):
        c = self.importDBC()
        self.columns = c["columns"]
        self.columns.update(c["foreignKeys"])
    def dbc2DBMgrQ(self):
        import requests
        import json
        req = requests.get()
    def dbc2DBMgrU(self):
        import requests
        import json
        pass