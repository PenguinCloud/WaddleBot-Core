import requests
from pydal import DAL, Field

class DiscordManager:
    def __init__(self, db):
        self.db = db

        self.create_discord_table()
        
    # Function to create the user table
    def create_discord_table(self):
        print("Creating discord table")
        self.db.define_table('discord', 
                            Field('channel', 'string'),
                            Field('community_id', 'integer'),
                            Field('servers', 'list:string'),
                            Field('aliases', 'list:string'),)
        self.db.commit()

    # Function to add a new discord channel community entry, if the community already exists, it will return an error
    def create_discord(self, data):
        # Before a new discord channel is created, we need to check if the discord channel already exists
        discord = self.db(self.db.discord.channel == data['channel']).select().first()
        if discord:
            return "Discord channel already exists."
        else:
            self.db.discord.insert(channel=data['channel'])

            discord = self.db(self.db.discord.channel == data['channel']).select().first()

            if 'community_id' in data:
                print("Adding community_id...")
                discord.update_record(community_id=0)
            if 'servers' in data:
                print("Adding servers...")
                discord.update_record(servers=data['servers'])
            if 'aliases' in data:
                print("Adding aliases...")
                discord.update_record(aliases=data['aliases'])  

            self.db.commit()

            return "Discord channel created successfully"
        
    # Function to retrieve a specific discord channel by channel name
    def get_discord_by_channel(self, channel):
        discord = self.db(self.db.discord.channel == channel).select().first()

        if not discord:
            return { 'error': 'Discord channel does not exist.'}
        return discord.as_dict()
    
    # Function get discord by ID
    def get_discord_by_id(self, id):
        discord = self.db(self.db.discord.id == id).select().first()

        return discord
    
    # Function to remove a discord server by channel name
    def remove_discord(self, channel):
        # Check if the discord server exists
        discord = self.db(self.db.discord.channel == channel).select().first()
        if not discord:
            return "Discord channel does not exist."

        # Remove the discord server
        self.db(self.db.discord.channel == channel).delete()

        self.db.commit()

        return "Discord channel removed successfully"
    
    
    # Function to get a list of all discord servers
    def get_discords(self):
        discords = self.db(self.db.discord).select()

        return discords.as_list()
    
    # Function to update a discord server, depending on the given fields in a data dictionary
    def update_discord(self, channel, data):
        # Check if the discord server exists
        discord = self.db(self.db.discord.channel == channel).select().first()
        if not discord:
            return "Discord channel does not exist."
        
        # Update the discord server
        if 'channel' in data:
            discord.update_record(channel=data['channel'])
        if 'community_id' in data:
            discord.update_record(community_id=data['community_id'])
        if 'servers' in data:
            discord.update_record(servers=data['servers'])
        if 'aliases' in data:
            discord.update_record(aliases=data['aliases'])

        self.db.commit()

        return "Discord channel updated successfully"

