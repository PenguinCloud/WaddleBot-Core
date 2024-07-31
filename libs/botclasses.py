from dataclasses import dataclass
'''@dataclass
class dbc:
    database: str
    dbhost: str
    dbport: int
    dbuser: str
    dbpassword: str '''

@dataclass
class webdb:
    webhost: str
    webport: int
    webuser: str
    webpassword: str
    database: str

@dataclass
class identity:
    id: str
    reputation: float
    
@dataclass
class event:
    activity: str
    amount: float   
    namespace: str
    platform: str
    interface: str
    subInterface: str
    rawText: str


@dataclass
class column:
    name: str
    datatype: str
    foreignKeyTable: str
    foreignKeyColumn: str
