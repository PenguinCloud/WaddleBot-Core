import requests
from pydal import DAL, Field

class CommunityMembersManager:
    def __init__(self, db):
        self.db = db
        
    # Function to create the user table
    def create_community_members_table(self):
        self.db.define_table('community_members', 
                            Field('community_id', 'integer'),
                            Field('member_id', 'integer'),
                            Field('role_id', 'integer'),
                            Field('currency', 'integer', default=0),
                            Field('reputation', 'integer', default=0),)
        self.db.commit()

    # Function to create a new community member entry, if the community member already exists, it will return an error
    def create_community_member(self, community_id, member_id, role): 
        # Before a new community member is created, we need to check if the community member already exists
        community_member = self.get_community_member_by_community_id_and_member_id(community_id, member_id)
        if community_member:
            return "Community member already exists."
        else:
            self.db.community_members.insert(community_id=community_id, member_id=member_id, role=role)

            self.db.commit()

            return "Community member created successfully"
        
    # Function to remove a community member
    def remove_community_member(self, community_id, member_id):
        # Check if the community member exists
        community_member = self.get_community_member_by_community_id_and_member_id(community_id, member_id)
        if not community_member:
            return "Community member does not exist."

        # Remove the community member
        self.db((self.db.community_members.community_id == community_id) & (self.db.community_members.member_id == member_id)).delete()

        self.db.commit()

        return "Community member removed successfully"
    