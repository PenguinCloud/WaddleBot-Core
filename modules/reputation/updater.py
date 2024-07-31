from libs.botClasses import *
import re
from libs.botDBC import botDb as db
from libs.botConfig import botConfig as cfg

#Const
CONFIG_FILE = pathlib.Path(__file__).parent.resolve() + "config.yml"

class update:
    def __init__(self, id: identity, events: event, dbc: dbinfo) -> None:
        self.score = 0
        self.id = id
        self.event = events
        self.retvars = retvars
        self.config = cfg(configPath=CONFIG_FILE)
        self.dbc = db(configfile=self.config)
    def twitch(self):
        dbScore = dbquery
        dbScore.columns = ["score"]
        dbScore.queryColumn = "event"
        match self.event.activity:
            case re.match(r"(re-)?subscription, self.event.activity"):
                if re.match(r"^tier 1"):
                    
                    dbq.queryValue = "supporter"
                    value = self.dbc.webdbUpdate(query=dbq)
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

