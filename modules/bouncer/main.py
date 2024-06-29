import csv
from dataclasses import dataclass


@dataclass
class dbconnect:
    """Class for keeping track of an item in inventory."""
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
    """Class for keeping"""
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
    
   
    def twitch(self,activity:str = "follow", amount:float = 0.0):
        if activity is in ["bits","sub","donate"]:
            readscore = self.__queryscore("twitch") 
        else:
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
    

    

if name == "main":
  x = Rep_Manager("1")
  x.db["dbname"] = "reputation"
  y = x.queryscore() 

 