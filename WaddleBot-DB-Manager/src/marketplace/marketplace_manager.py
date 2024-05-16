import requests
from pydal import DAL, Field

class MarketplaceManager:
    def __init__(self, db):
        self.db = db
        
    # Function to create the user table
    def create_marketplace_table(self):
        self.db.define_table('marketplace', 
                            Field('name'),
                            Field('description'),
                            Field('gateway_url', 'string'),
                            Field('module_type_id', 'integer'),
                            Field('metadata', 'json'))
        
        self.db.commit()

    # Function to create a new marketplace entry, if the marketplace already exists, it will return an error
    def create_marketplace(self, name, description, gateway_url, module_type_id, metadata): 
        # Before a new marketplace is created, we need to check if the marketplace already exists
        marketplace = self.get_marketplace_by_name(name)
        if marketplace:
            return "Marketplace already exists."
        else:
            self.db.marketplace.insert(name=name, description=description, gateway_url=gateway_url, module_type_id=module_type_id, metadata=metadata)

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

        return marketplaces
    
    # Function to get a marketplace by name
    def get_marketplace_by_name(self, name):
        marketplace = self.db(self.db.marketplace.name == name).select().first()

        return marketplace
