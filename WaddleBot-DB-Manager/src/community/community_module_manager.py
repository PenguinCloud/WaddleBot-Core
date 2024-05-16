import requests
from pydal import DAL, Field

class CommunityModuleManager:
    def __init__(self, db):
        self.db = db

    # Function to create the community module table
    def create_community_module_table(self):
        self.db.define_table('community_modules', 
                            Field('module_id', 'integer'),
                            Field('community_id', 'integer'),
                            Field('enabled', 'boolean', default=True),
                            Field('privilages', 'list:string'),)
        
        self.db.commit()

    # Function to add a new community module entry, if the community module already exists, it will return an error
    def create_community_module(self, module_id, community_id): 
        # Before a new community module is created, we need to check if the module already exists
        community_module = self.get_community_module_by_module_id_and_community_id(module_id, community_id)
        if community_module:
            return "Community module already exists."
        else:
            self.db.community_modules.insert(module_id=module_id, community_id=community_id)

            self.db.commit()

            return "Community module created successfully"
        
    # Function to get a community module by module id and community id
    def get_community_module_by_module_id_and_community_id(self, module_id, community_id):
        community_module = self.db((self.db.community_modules.module_id == module_id) & (self.db.community_modules.community_id == community_id)).select().first()

        return community_module
    
    # Function to remove a community module from a community
    def remove_community_module(self, module_id, community_id):
        # Check if the community module exists
        community_module = self.get_community_module_by_module_id_and_community_id(module_id, community_id)
        if not community_module:
            return "Community module does not exist."

        # Remove the community module
        self.db((self.db.community_modules.module_id == module_id) & (self.db.community_modules.community_id == community_id)).delete()

        self.db.commit()

        return "Community module removed successfully"