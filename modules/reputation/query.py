from libs.botClasses import *
from libs.botDBC import botDb as dbc
from libs.botConfig import botConfig as bc

class query:
    def __init__(self, userid: identity) -> None:
        self.score = 0
        self.id = userid
        self.retvars = retvars
        self.config = bc(configPath=CONFIG_FILE)
        self.dbc = dbc(config=self.config)
    # Lookup an ID's reputation
    def idRep(self):
        lookCol = "userid"
        database = "waddlebot"
    # Return the alias name for the current score
    def repAlias(self, score:float=600):
        for alias, range in self.config["reputation-alias"]:
            if score > range[0] and score < range[1]:
                return alias
        return "no alias found!"
    # Check what the adjustment based on general type should be
    def scoreAdjust(self, eventType: str, eventAmount: float = 1.0):
        scoreDBQ = dbquery
        scoreDBQ.columns = "adjustment"
        scoreDBQ.queryColumn = "event"
        scoreDBQ.queryValue = eventType
        x = dbc
        y = x.webdbRead(query=scoreDBQ)