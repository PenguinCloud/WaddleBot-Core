import requests
from pydal import DAL, Field

class IdentityManager:
    def __init__(self, db):
        self.db = db

        self.create_identity_table()
        
    # Function to create the user table
    def create_identity_table(self):
        print("Creating identity table")
        self.db.define_table('identity', 
                            Field('name', 'string'),
                            Field('country', 'string'),
                            Field('ip_address', 'string'),
                            Field('browser_fingerprints', 'list:string'),)
        self.db.commit()

    # Function to create a new identity entry, if the identity already exists, it will return an error
    def create_identity(self, data): 
        # Before a new identity is created, we need to check if the identity already exists
        identity = self.db(self.db.identity.name == data['name']).select().first()
        if identity:
            return "Identity already exists."
        else:
            self.db.identity.insert(name=data['name'])

            identity = self.db(self.db.identity.name == data['name']).select().first()

            if 'country' in data:
                identity.update_record(country=data['country'])
            if 'ip_address' in data:
                identity.update_record(ip_address=data['ip_address'])
            if 'browser_fingerprints' in data:
                identity.update_record(browser_fingerprints=data['browser_fingerprints'])

            self.db.commit()

            return "Identity created successfully"
        
    # Function to retrieve a specific identity by name
    def get_identity_by_name(self, name):
        identity = self.db(self.db.identity.name == name).select().first()

        if not identity:
            return { 'error': 'Identity does not exist.'}
        return identity.as_dict()
    
    # Function to retrieve all identities
    def get_all_identities(self):
        identities = self.db(self.db.identity).select()

        return identities.as_list()
    
    # Function to delete an identity by Name. If the identity does not exist, it will return an error
    def delete_identity(self, name):
        identity = self.db(self.db.identity.name == name).select().first()

        if identity:
            self.db(self.db.identity.name == name).delete()
            self.db.commit()

            return "Identity deleted successfully"
        else:
            return "Identity does not exist."
    
    # Function to update an identity by ID, depending on the given fields
    def update_identity(self, name, data):
        identity = self.db(self.db.identity.name == name).select().first()

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
