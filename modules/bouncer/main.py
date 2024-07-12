from regex import match
import csv
from dataclasses import dataclass


@dataclass
class dbconnect:
    #Class for keeping track of an item in inventory.
    dbhost: str
    dbport: str
    dbmethod: str
    dbname: str
    def __init__(self, dbhost = "localhost", dbport = "", dbmethod= "csv", dbname = "reputation"):
        self.dbhost = dbhost
        self.dbport = dbport
        self.dbmethod = dbmethod
        self.dbname = dbname    

@dataclass
class dbquery:
    
    collumns: list
    qcollumns: str
    rowselector: str
    def __init__(self, collumns = ["*"],qcollumns = "*", rowselector = "*"):
        self.collumns = collumns
        self.rowselector = rowselector
        self.qcollumns = qcollumns



class Rep_Manager:
   
   
    def __init__(self, userid):
        self.userid = userid
        self.score = 600.0
    

    def __queryscore(self,platfom: str,activity:str):
        dbc = dbconnect()
        dbc.dbname = platform+"-scores"
        return self.__readdb(dbc, ["score"],activity)
   
   
    def youtube(self):
        readscore = self.__queryscore("youtube") 
        self.score += readscore["score"]

   
    def discord(self):
        readscore = self.__queryscore("discord") 
        self.score += readscore["score"]  
    
   
    def twitch(self, text:str, userid:str):
        activity = "none"
        amount = 1.0
        if userid == "system":
            if match(r"now banned from this channel\.$", text):
                activity = "ban"
                amount = -50.0
            elif match (r"has just (re)?subscribed\!$", text):
                activity = "moneyevent"
                amount = 5.0
            #elif match(r"has just donated \$\d+\.\d+\!", text):
                #activity = "moneyevent"
                #amount = 10.0
            elif match(r"timed out for () seconds\.$", text):
                activity = "timeout"
                amount = -0.25
            elif match(r"has just cheered \d+ bits\!$", text):
                activity = "moneyevent"
                amount = 0.01
            elif match(r"has just followed\!$", text):
                activity = "follow"
                amount = 50.0
            elif match(r"has just raided with \d+ viewers\!$", text):
                activity = "raid"
                amount = 5.0
            
            readscore = self.__queryscore("twitch") 
            self.score += readscore["score"]        
   
    def __readdb(self,dbc: dbconnect,dbq: dbquery):

        if dbc.dbmethod == "csv":
            df = pandas.read_csv(dbc.dbname+".csv")
            results = df.query(dbq.rowselector)
            return results
        else:
            print("Database method not supported")
            return None
   
   
    def querybyid(self):
        x = dbconnect()
        results = self.__readdb(x, ["score"])
        return results
    


def onevent(platform,userid,text):
    x = Rep_Manager(userid)
    if platform == "youtube":
        x.youtube()
    elif platform == "discord":
        x.discord()
    elif platform == "twitch":
        x.twitch()
    else:
        return 0
    return 1


if name == "main":
  x = Rep_Manager("1")
  x.db["dbname"] = "reputation"
  y = x.queryscore() 

 