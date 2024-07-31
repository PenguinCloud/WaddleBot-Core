from libs.botClasses import *
import re
from libs.botDBC import botDb as dbc
from libs.botConfig import botConfig as bc
from updater import update


#Const
CONFIG_FILE = pathlib.Path(__file__).parent.resolve() + "config.yml"

class update:
    def __init__(self, id: identity, events: event, db: dbinfo) -> None:
        self.score = 0
        self.id = id
        self.event = events
        self.retvars = retvars
        self.config = bc(configPath=CONFIG_FILE)
        self.dbc = dbc(configfile=self.config)
        self.db = db
    def twitch(self):
        match self.event.activity:
            case re.match(r"(re-)?subscription, self.event.activity"):
                if re.match(r"^tier 1"):
                    self.dbc.webdbUpdate()
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

