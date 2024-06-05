import requests
from pydal import DAL, Field
import os

# The connectionString is the path to the database.
connectionString = 'sqlite://src/db/test.db'

class MarketplaceDBManager:
    def __init__(self):
        self.db = DAL(connectionString, pool_size=0)

        self.create_marketplace_table()
        
    # Function to create the user table
    def create_marketplace_table(self):
        print("Creating marketplace table...")
        self.db.define_table('marketplace', 
                            Field('name', 'string'),
                            Field('description', 'string'),
                            Field('gateway_url', 'string'),
                            Field('module_type_id', 'integer'),
                            Field('metadata', 'json'))
        
        self.db.commit()

    # Function to create a new marketplace entry, if the marketplace already exists, it will return an error
    def create_marketplace(self, data): 
        # Before a new marketplace is created, we need to check if the marketplace already exists
        marketplace = self.db(self.db.marketplace.name == data['name']).select().first()
        if marketplace:
            return "Marketplace already exists."
        else:
            self.db.marketplace.insert(name=data['name'])

            marketplaceModule = self.db(self.db.marketplace.name == data['name']).select().first()

            if 'description' in data:
                marketplaceModule.update_record(description=data['description'])
            if 'gateway_url' in data:
                marketplaceModule.update_record(gateway_url=data['gateway_url'])
            if 'module_type_id' in data:
                marketplaceModule.update_record(module_type_id=data['module_type_id'])
            if 'metadata' in data:
                marketplaceModule.update_record(metadata=data['metadata'])

            self.db.commit()

            return "Marketplace created successfully"
        
    # Function to remove a marketplace
    def remove_marketplace(self, name):
        # Check if the marketplace exists
        marketplace = self.get_marketplace_by_name(name)
        if not marketplace:
            return "Marketplace does not exist."

        # Remove the marketplace
        self.db(self.db.marketplace.name == name).delete()

        self.db.commit()

        return "Marketplace removed successfully"
    
    # Function to retrieve a list of all marketplace Modules
    def get_marketplace_modules(self):
        marketplaces = self.db(self.db.marketplace).select()

        return marketplaces.as_list()
    
    # Function to get a marketplace by name
    def get_marketplace_by_name(self, name):
        marketplace = self.db(self.db.marketplace.name == name).select().first()

        if not marketplace:
            return { 'error': 'Marketplace does not exist.'}
        return marketplace.as_dict()
    
    # Function to get a marketplace module by URL
    def get_marketplace_by_url(self, url):
        marketplace = self.db(self.db.marketplace.gateway_url == url).select().first()

        if not marketplace:
            return { 'error': 'Marketplace does not exist.'}
        return marketplace.as_dict()
    
    # Function to get a marketplace by ID
    def get_marketplace_by_id(self, id):
        marketplace = self.db(self.db.marketplace.id == id).select().first()

        return marketplace
    
    # Function to update a marketplace, depending on the given fields in a data dictionary
    def update_marketplace(self, name, data):
        # Check if the marketplace exists
        marketplace = self.get_marketplace_by_name(name)
        if not marketplace:
            return "Marketplace does not exist."
        
        # Update the marketplace
        if 'name' in data:
            marketplace.name = data['name']
        if 'description' in data:
            marketplace.description = data['description']
        if 'gateway_url' in data:
            marketplace.gateway_url = data['gateway_url']
        if 'module_type_id' in data:
            marketplace.module_type_id = data['module_type_id']
        if 'metadata' in data:
            marketplace.metadata = data['metadata']

        marketplace.update_record()

        self.db.commit()

        return "Marketplace updated successfully"

