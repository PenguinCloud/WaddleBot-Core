import requests
from pydal import DAL, Field

class CommunityManager:
    def __init__(self, db):
        self.db = db

        self.create_community_table()
        
    # Function to create the user table
    def create_community_table(self):
        print("Creating the communities table....")
        self.db.define_table('communities', 
                            Field('community_name'),
                            Field('community_description'))
        self.db.commit()

    # Function to create a new community entry, if the community already exists, it will return an error
    def create_community(self, community_data): 
        # Check if the community already exists
        community = self.get_community_by_name(community_data['community_name'])
        
        if 'error' not in community:
            return "Community already exists."
        
        description = ''

        if 'community_description' in community_data:
            description = community_data['community_description']

        # Insert the community into the communities table
        self.db.communities.insert(community_name=community_data['community_name'], community_description=description)
        self.db.commit()

        return "Community created successfully"

    
    # Function to remove a community by community name, if it exists
    def delete_community(self, communityname):
        community = self.db(self.db.communities.community_name == communityname).select().first()

        if community:
            self.db(self.db.communities.community_name == communityname).delete()
            self.db.commit()

            return "Community removed successfully"
        else:
            return "Community does not exist."
    
    # Function to retrieve a list of all communities. Return an empty list if no communities exist.
    def get_communities(self):
        communities = self.db(self.db.communities).select()

        return communities.as_list()

    # Function to retrieve a specific community by communityname. Return a message if the community does not exist.
    def get_community_by_name(self, communityname):
        community = self.db(self.db.communities.community_name == communityname).select().first()

        if not community:
            return {"error": "Community does not exist."}
        return community.as_dict()

    # Function to update a community by communityname, depending on the given fields
    def update_community(self, communityname, data):
        community = self.db(self.db.communities.community_name == communityname).select().first()

        if community:
            if 'community_name' in data:
                community.update_record(community_name=data['community_name'])
            if 'community_description' in data:
                community.update_record(community_description=data['community_description'])

            self.db.commit()

            return "Community updated successfully"
        else:
            return "Community does not exist."
        
    # Function to update the description of a community
    def update_community_description(self, communityname, description):
        community = self.db(self.db.communities.community_name == communityname).select().first()

        if community:
            community.update_record(community_description=description)
            self.db.commit()

            return "Community description updated successfully"
        else:
            return "Community does not exist."
    