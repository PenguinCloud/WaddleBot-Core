import requests
from pydal import DAL, Field

class TwitchManager:
    def __init__(self, db):
        self.db = db

        self.create_twitch_table()

    # Function to create the twitch table
    def create_twitch_table(self):
        print("Creating twitch table")
        self.db.define_table('twitch', 
                            Field('channel', 'string'),
                            Field('community_id', 'integer'),
                            Field('servers', 'list:string'),
                            Field('aliases', 'list:string'),)
        
        self.db.commit()

    # Function to add a new twitch channel community entry, if the community already exists, it will return an error
    def create_twitch(self, data): 
        # Before a new twitch channel is created, we need to check if the channel already exists
        twitch = self.db(self.db.twitch.channel == data['channel']).select().first()
        if twitch:
            return "Twitch channel already exists."
        else:
            self.db.twitch.insert(channel=data['channel'])

            twitch = self.db(self.db.twitch.channel == data['channel']).select().first()

            if 'community_id' in data:
                twitch.update_record(community_id=data['community_id'])
            if 'servers' in data:
                twitch.update_record(servers=data['servers'])
            if 'aliases' in data:
                twitch.update_record(aliases=data['aliases'])

            self.db.commit()

            return "Twitch channel created successfully"
        
    # Function to retrieve a specific twitch channel by channel name
    def get_twitch_by_channel(self, channel):
        twitch = self.db(self.db.twitch.channel == channel).select().first()

        if not twitch:
            return { 'error': 'Twitch channel does not exist.'}
        return twitch.as_dict()
    
    # Function to add a server to a twitch channel
    def add_server_to_twitch(self, channel, server):
        # Check if the twitch channel exists
        twitch = self.db(self.db.twitch.channel == channel).select().first()
        if not twitch:
            return "Twitch channel does not exist."

        # Add the server to the twitch channel
        self.db(self.db.twitch.channel == channel).update_record(servers=server)

        self.db.commit()

        return "Server added to twitch channel successfully"
    
    # Function to get a list of all twitch servers
    def get_twitch_channels(self):
        twitch = self.db(self.db.twitch).select()

        return twitch.as_list()
    
    # Function to update a twitch server, depending on the given fields in a data dictionary
    def update_twitch(self, channel, data):
        # Check if the twitch server exists
        twitch = self.db(self.db.twitch.channel == channel).select().first()
        if not twitch:
            return "Twitch channel does not exist."
        
        # Update the twitch server
        if 'channel' in data:
            twitch.update_record(channel=data['channel'])
        if 'community_id' in data:
            twitch.update_record(community_id=data['community_id'])
        if 'servers' in data:
            twitch.update_record(servers=data['servers'])
        if 'aliases' in data:
            twitch.update_record(aliases=data['aliases'])

        self.db.commit()

        return "Twitch channel updated successfully"
    
    # Function to remove a twitch channel
    def remove_twitch(self, channel):
        # Check if the twitch channel exists
        twitch = self.db(self.db.twitch.channel == channel).select().first()
        if not twitch:
            return "Twitch channel does not exist."

        # Remove the twitch channel
        self.db(self.db.twitch.channel == channel).delete()

        self.db.commit()

        return "Twitch channel removed successfully"
    
    # Function to get a list of all twitch servers by community_id
    def get_twitchs_by_community_id(self, community_id):
        twitchs = self.db(self.db.twitch.community_id == community_id).select()

        return twitchs.as_list()
    
    