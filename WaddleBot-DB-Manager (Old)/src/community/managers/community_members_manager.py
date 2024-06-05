import requests
from pydal import DAL, Field

class CommunityMembersManager:
    def __init__(self, db):
        self.db = db

        self.create_community_members_table()
        
    # Function to create the user table
    def create_community_members_table(self):
        print("Creating the community members table....")
        self.db.define_table('community_members', 
                            Field('community_id', 'integer'),
                            Field('member_id', 'integer'),
                            Field('role_id', 'integer'),
                            Field('currency', 'integer', default=0),
                            Field('reputation', 'integer', default=0),)
        self.db.commit()

    # Function to create a new community member from a data object. If the community member already exists, it will return an error
    def create_community_member(self, data):
        # Before a new community member is created, we need to check if the community member already exists
        community_member = self.get_community_member_by_community_id_and_member_id(data['community_id'], data['member_id'])
        if 'error' not in community_member:
            return "Community member already exists."
        else:
            self.db.community_members.insert(community_id=data['community_id'], member_id=data['member_id'])

            community_member = self.db((self.db.community_members.community_id == data['community_id']) & (self.db.community_members.member_id == data['member_id'])).select().first()

            if 'role_id' in data:
                community_member.update(role_id=1)
            if 'currency' in data:
                community_member.update(currency=data['currency'])
            if 'reputation' in data:
                community_member.update(reputation=data['reputation'])

            self.db.commit()

            return "Community member created successfully"
        
    # Function to remove a community member
    def remove_community_member(self, community_id, member_id):
        # Check if the community member exists
        community_member = self.get_community_member_by_community_id_and_member_id(community_id, member_id)
        if 'error' in community_member:
            return "Community member does not exist."

        # Remove the community member
        self.db((self.db.community_members.community_id == community_id) & (self.db.community_members.member_id == member_id)).delete()

        self.db.commit()

        return "Community member removed successfully"
    
    # Function to get a community member by community_id and member_id and return the value as a dictionary. Return a message if the community member does not exist
    def get_community_member_by_community_id_and_member_id(self, community_id, member_id):
        community_member = self.db((self.db.community_members.community_id == community_id) & (self.db.community_members.member_id == member_id)).select().first()

        if not community_member:
            return {"error": "Community member does not exist."}
        return community_member.as_dict()
    
    # Function to get a list of all community members by community_id. Return an empty list if no community members are found
    def get_community_members_by_community_id(self, community_id):
        community_members = self.db(self.db.community_members.community_id == community_id).select()

        return community_members.as_list()
    
    # Function to get a list of all community members. Return an empty list if no community members are found
    def get_community_members(self):
        community_members = self.db(self.db.community_members).select()

        return community_members.as_list()
    
    # Function to get a community member by member_id. Return a message if the community member does not exist
    def get_community_member_by_member_id(self, community_id, member_id):
        community_member = self.db((self.db.community_members.community_id == community_id) & (self.db.community_members.member_id == member_id)).select().first()

        if not community_member:
            return {"error": "Community member does not exist."}
        return community_member.as_dict()
    
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
    