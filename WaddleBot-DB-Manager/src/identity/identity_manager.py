import requests
from pydal import DAL, Field

class IdentityManager:
    def __init__(self, db):
        self.db = db
        
    # Function to create the user table
    def create_identity_table(self):
        self.db.define_table('identity', 
                            Field('name', 'string'),
                            Field('country', 'string'),
                            Field('ip_address', 'string'),
                            Field('browser_fingerprints', 'list:string'),)
        self.db.commit()

    # Function to create a new identity entry, if the identity already exists, it will return an error
    def create_identity(self, name): 
        # Before a new identity is created, we need to check if the identity already exists
        identity = self.get_identity_by_name(name)
        if identity:
            return "Identity already exists."
        else:
            self.db.identity.insert(name=name)

            self.db.commit()

            return "Identity created successfully"
        
    # Function to retrieve a specific identity by name
    def get_identity_by_name(self, name):
        identity = self.db(self.db.identity.name == name).select().first()

        return identity
