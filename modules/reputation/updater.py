from libs.botClasses import *
import re
from libs.botDBC import botDb as db
from libs.botConfig import botConfig as cfg
from libs.botLogger import botLogger
from query import dbquery as dbq


# Why is that black van out there?
log = botLogger("reputation-updater")
log.fileLogger("reputation.log")

#--------
# This is the function which will update the reputation of an identity
#--------
class update:
    def __init__(self, id: identity, events: event, dbc: dbinfo, CONFIG_FILE: str) -> None:
        self.score = 0
        self.id = id
        self.event = events
        self.retvars = retvars
        self.config = cfg(configPath=CONFIG_FILE)
        self.dbc = db(configfile=self.config)
        log.debug(f"Update object initiated for {self.id.id}")

    def twitch(self):
        dbScore = dbquery
        dbScore.columns = ["score"]
        dbScore.queryColumn = "event"
        match self.event.activity:
            case re.match(r"(re-)?subscription, self.event.activity"):
                if re.match(r"^tier 1"):
                    dbq.queryValue = "supporter"
                    value = self.dbc.webdbUpdate(query=dbq)
                    x = self.updateScore()
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

    def updateScore(self, scoreChange: float):
        dbScore = dbquery
        dbScore.columns = ["score"]
        dbScore.queryColumn = "event"
        dbScore.queryValue = self.event.activity
        dbScore.database = "waddlebot"
        dbScore.table = "reputation"
        dbScore.whereColumn = "userid"
        dbScore.whereValue = self.id.id
        dbScore.updateColumn = "score"
        dbScore.updateValue = scoreChange
        dbu = db.webdbUpdate(query=dbScore)
        if dbu == None:
            log.error("Failed to update score")
            return False
        else:
            log.debug(f"Score updated for {self.id.id}")
            return True