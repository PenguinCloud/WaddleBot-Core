import requests
from pydal import DAL, Field

class CommunityManager:
    def __init__(self, db):
        # self.connectionString = connectionString
        # self.db = DAL(connectionString,pool_size=0)
        self.db = db
        
    # Function to create the user table
    def create_community_table(self):
        self.db.define_table('communities', 
                            Field('communityname'),
                            Field('communitydescription'))
        self.db.commit()

    # Function to create a new community entry, if the community already exists, it will return an error
    def create_community(self, communityname): 
        # Before a new community is created, we need to check if the community already exists
        community = self.get_community_by_name(communityname)
        if community:
            return "Community already exists."
        else:
            self.db.communities.insert(communityname=communityname)

            # # Remove spaces from the community name
            # communityname = communityname.replace(" ", "_")

            # # Create a new table for the community
            # self.db.define_table(communityname, 
            #                 Field('member'),
            #                 Field('role', default='member'))

            self.db.commit()

            return "Community created successfully"

    # Function to add a user to a community
    def add_user_to_community(self, communityname, username):
        # Check if the community exists
        community = self.get_community_by_name(communityname)
        if not community:
            return "Community does not exist."

        # Check if the user exists
        user = self.db(self.db.users.username == username).select().first()
        if not user:
            return "User does not exist."

        # Check if the user is already a member of the community
        member = self.db(self.db[communityname].member == username).select().first()
        if member:
            return "User is already a member of the community."

        # Add the user to the community
        self.db[communityname].insert(member=username)

        self.db.commit()

        return "User added to community successfully" 
    
    # Function to remove a community
    def remove_community(self, communityname):
        # Check if the community exists
        community = self.get_community_by_name(communityname)
        if not community:
            return "Community does not exist."

        # Remove the community
        # self.db(self.db.communities.communityname == communityname).delete()

        # Remove the community record from the communities table
        self.db(self.db.communities.communityname == communityname).delete()

        print(f"Community removed successfully from the communities table. Deleting the {communityname} table....")

        # # Remove spaces from the community name
        # communityname = communityname.replace(" ", "")
        # self.db['users'].drop()

        self.db.commit()

        return "Community removed successfully"
    
    # Function to retrieve a list of all communities
    def get_communities(self):
        communities = self.db(self.db.communities).select()

        return communities

    # Function to retrieve a specific community by communityname
    def get_community_by_name(self, communityname):
        community = self.db(self.db.communities.communityname == communityname).select().first()

        return community
    
    # Function to add a description to a community
    def add_description_to_community(self, communityname, communitydescription):
        # Check if the community exists
        community = self.get_community_by_name(communityname)
        if not community:
            return "Community does not exist."

        # Update the description of the community
        self.db(self.db.communities.communityname == communityname).update(communitydescription=communitydescription)
        self.db.commit()

        return "Description added to community successfully"
