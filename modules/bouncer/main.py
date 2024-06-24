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
class Rep_Manager:
    def __init__(self, userid):
        self.userid = userid
        self.score = 600.0
    

    def __queryscore(self,platfom: str):
        dbc = dbconnect()
        dbc.dbname = platform+"-scores"
        return self.__readdb(dbc, ["score"])
    
      
      
    
    def twitch(self):
        readscore = self.__queryscore("twitch") 
        return self.score + 250.0

    def follow(self):
        return self.score + 100.0

    def timeout(self):
        return self.score + -50.0

    def ban(self):
        return self.score + -1000.0

    def rank(self):
        good = self.score <= 700.0
        ok = self.score == 400.0-699.99
        bad = self.score >= 399.99
    def __readdb(self,dbc: dbconnect,collumns = ["score"]):

        if dbc.dbmethod == "csv":
            results = {}
            with open(dbc.dbmethod["dbname"] + ".csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row["userid"] == self.userid:
                       for  col in collumns:
                            results[col] = row[col]
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

 