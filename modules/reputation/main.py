#!/usr/bin/python3
from dataclasses.py import dbc, webdb

class reputation:
    def __init__(self) -> None:
        self.score = 0
        self.userid = None
        self.platform = None
        self.interface = None
        self.subinterface = None
        self.database = dbc
        self.webdb = webdb
