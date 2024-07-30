from dataclasses import dataclass
@dataclass
class dbc:
    database: str
    dbhost: str
    dbport: int
    dbuser: str
    dbpassword: str


@dataclass
class webdb:
    webhost: str
    webport: int
    webuser: str
    webpassword: str
    database: str

