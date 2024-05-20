import requests
from pydal import DAL, Field

class DiscordManager:
    def __init__(self, db):
        self.db = db
        
    # Function to create the user table
    def create_discord_table(self):
        self.db.define_table('discord', 
                            Field('channel', 'string'),
                            Field('community_id', 'integer'),
                            Field('servers', 'list:string'),
                            Field('aliases', 'list:string'),)
        self.db.commit()

    # Function to add a new discord channel community entry, if the community already exists, it will return an error
    def create_discord(self, channel, community_id, servers=[], aliases=[]): 
        # Before a new discord channel is created, we need to check if the channel already exists
        discord = self.get_discord_by_channel(channel)
        if discord:
            return "Discord channel already exists."
        else:
            self.db.discord.insert(channel=channel, community_id=community_id, servers=servers, aliases=aliases)

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
    
    # Function to remove a discord channel
    def remove_discord(self, channel):
        # Check if the discord channel exists
        discord = self.get_discord_by_channel(channel)
        if not discord:
            return "Discord channel does not exist."

        # Remove the discord channel
        self.db(self.db.discord.channel == channel).delete()

        self.db.commit()

        return "Discord channel removed successfully"
    
    # Function to get a list of all discord servers
    def get_discords(self):
        discords = self.db(self.db.discord).select()

        return discords
    
    # Function to update a discord server, depending on the given fields in a data dictionary
    def update_discord(self, channel, data):
        # Check if the discord server exists
        discord = self.get_discord_by_channel(channel)
        if not discord:
            return "Discord channel does not exist."
        
        # Update the discord server
        if 'channel' in data:
            discord.channel = data['channel']
        if 'community_id' in data:
            discord.community_id = data['community_id']
        if 'servers' in data:
            discord.servers = data['servers']
        if 'aliases' in data:
            discord.aliases = data['aliases']

        self.db.commit()

        return "Discord channel updated successfully"

