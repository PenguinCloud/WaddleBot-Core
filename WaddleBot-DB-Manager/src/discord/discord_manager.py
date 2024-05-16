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
    def create_discord(self, channel): 
        # Before a new discord channel is created, we need to check if the channel already exists
        discord = self.get_discord_by_channel(channel)
        if discord:
            return "Discord channel already exists."
        else:
            self.db.discord.insert(channel=channel)

            self.db.commit()

            return "Discord channel created successfully"
        
    # Function to retrieve a specific discord channel by channel name
    def get_discord_by_channel(self, channel):
        discord = self.db(self.db.discord.channel == channel).select().first()

        return discord
    
    # Function to add a server to a discord channel
    def add_server_to_discord(self, channel, server):
        # Check if the discord channel exists
        discord = self.get_discord_by_channel(channel)
        if not discord:
            return "Discord channel does not exist."

        # Add the server to the discord channel
        self.db(self.db.discord.channel == channel).update_record(servers=server)

        self.db.commit()

        return "Server added to discord channel successfully"
