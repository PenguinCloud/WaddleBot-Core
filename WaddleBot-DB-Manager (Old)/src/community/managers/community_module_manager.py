import requests
from pydal import DAL, Field

class CommunityModuleManager:
    def __init__(self, db):
        self.db = db

        self.create_community_module_table()

    # Function to create the community module table
    def create_community_module_table(self):
        print("Creating the community modules table....")
        self.db.define_table('community_modules', 
                            Field('module_id', 'integer'),
                            Field('community_id', 'integer'),
                            Field('enabled', 'boolean', default=True),
                            Field('privilages', 'list:string'),)
        
        self.db.commit()

    # Function to add a new community module entry, if the community module already exists, it will return an error
    def create_community_module(self, data):
        # Before a new community module is created, we need to check if the community module already exists
        community_module = self.db((self.db.community_modules.module_id == data['module_id']) & (self.db.community_modules.community_id == data['community_id'])).select().first()
        if community_module:
            return "Community module already exists for that community."
        else:
            self.db.community_modules.insert(module_id=data['module_id'], community_id=data['community_id'])

            community_module = self.db((self.db.community_modules.module_id == data['module_id']) & (self.db.community_modules.community_id == data['community_id'])).select().first()

            if 'enabled' in data:
                community_module.update(enabled=data['enabled'])
            if 'privilages' in data:
                community_module.update(privilages=data['privilages'])

            self.db.commit()

            return "Community module added successfully to the community."
    
    # Function to remove a community module from a community
    def remove_community_module(self, module_id, community_id):
        # Check if the community module exists
        community_module = self.db((self.db.community_modules.module_id == module_id) & (self.db.community_modules.community_id == community_id)).select().first()
        if not community_module:
            return "Community module does not exist."

        # Remove the community module
        self.db((self.db.community_modules.module_id == module_id) & (self.db.community_modules.community_id == community_id)).delete()

        self.db.commit()

        return "Community module removed successfully"
    
    # Function to get a list of all community modules by community_id
    def get_community_modules_by_community_id(self, community_id):
        community_modules = self.db(self.db.community_modules.community_id == community_id).select()

        return community_modules.as_list()
    
    # Function to get a list of all community modules
    def get_community_modules(self):
        community_modules = self.db(self.db.community_modules).select()

        return community_modules.as_list()
    
    # Function to get a list of all community modules by module_id
    def get_community_modules_by_module_id(self, module_id):
        community_modules = self.db(self.db.community_modules.module_id == module_id).select()

        return community_modules.as_list()
    
    # Function to get a community module by module_id and community_id. Return a message if the community module does not exist
    def get_community_module_by_module_id_and_community_id(self, module_id, community_id):
        community_module = self.db((self.db.community_modules.module_id == module_id) & (self.db.community_modules.community_id == community_id)).select().first()

        if not community_module:
            return { 'error': 'Community module does not exist.'}
        return community_module.as_dict()
    
    # Function to update a community module, depending on the given fields, by module_id
    def update_community_module(self, module_id, data):
        community_module = self.db(self.db.community_modules.module_id == module_id).select().first()
        if not community_module:
            return "Community module does not exist."

        if 'community_id' in data:
            community_module.update_record(community_id=data['community_id'])
        if 'enabled' in data:
            community_module.update_record(enabled=data['enabled'])
        if 'privilages' in data:
            community_module.update_record(privilages=data['privilages'])
        
        self.db.commit()

        return "Community module updated successfully"
    
    
    
    
