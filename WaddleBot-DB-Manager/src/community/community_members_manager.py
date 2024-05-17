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
    def create_community_member(self, community_id, member_id, role_id, currency, reputation):
        # Check if the community member already exists
        community_member = self.get_community_member_by_community_id_and_member_id(community_id, member_id)
        if community_member:
            return "Community member already exists."

        # Create the community member
        self.db.community_members.insert(community_id=community_id, member_id=member_id, role_id=role_id, currency=currency, reputation=reputation)
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
    
    # Function to get a community member by community_id and member_id
    def get_community_member_by_community_id_and_member_id(self, community_id, member_id):
        community_member = self.db((self.db.community_members.community_id == community_id) & (self.db.community_members.member_id == member_id)).select().first()

        return community_member
    
    # Function to get a list of all community members by community_id
    def get_community_members_by_community_id(self, community_id):
        community_members = self.db(self.db.community_members.community_id == community_id).select()

        return community_members
    
    # Function to get a list of all community members
    def get_community_members(self):
        community_members = self.db(self.db.community_members).select()

        return community_members
    
    # Function to get a community member by member_id
    def get_community_member_by_member_id(self, community_id, member_id):
        community_member = self.db((self.db.community_members.community_id == community_id) & (self.db.community_members.member_id == member_id)).select().first()

        return community_member
    
    # Function to update a community member, depending on the given fields, by member_id
    def update_community_member(self, member_id, data):
        community_member = self.db(self.db.community_members.member_id == member_id).select().first()
        if not community_member:
            return "Community member does not exist."

        if 'role_id' in data:
            community_member.update_record(role_id=data['role_id'])
        if 'currency' in data:
            community_member.update_record(currency=data['currency'])
        if 'reputation' in data:
            community_member.update_record(reputation=data['reputation'])

        self.db.commit()

        return "Community member updated successfully"
    