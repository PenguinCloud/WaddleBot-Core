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
    def create_identity(self, name, country, ip_address, browser_fingerprints): 
        # Before a new identity is created, we need to check if the identity already exists
        identity = self.get_identity_by_name(name)
        if identity:
            return "Identity already exists."
        else:
            self.db.identity.insert(name=name, country=country, ip_address=ip_address, browser_fingerprints=browser_fingerprints)

            self.db.commit()

            return "Identity created successfully"
        
    # Function to retrieve a specific identity by name
    def get_identity_by_name(self, name):
        identity = self.db(self.db.identity.name == name).select().first()

        return identity
    
    # Function to retrieve all identities
    def get_all_identities(self):
        identities = self.db(self.db.identity).select()

        return identities
    
    # Function to delete an identity by ID
    def delete_identity(self, identity_id):
        self.db(self.db.identity.id == identity_id).delete()

        self.db.commit()

        return "Identity deleted successfully"
    
    # Function to update an identity by ID, depending on the given fields
    def update_identity(self, identity_id, data):
        identity = self.db(self.db.identity.id == identity_id).select().first()

        if identity:
            if 'name' in data:
                identity.update_record(name=data['name'])
            if 'country' in data:
                identity.update_record(country=data['country'])
            if 'ip_address' in data:
                identity.update_record(ip_address=data['ip_address'])
            if 'browser_fingerprints' in data:
                identity.update_record(browser_fingerprints=data['browser_fingerprints'])

            self.db.commit()

            return "Identity updated successfully"
        else:
            return "Identity does not exist."
