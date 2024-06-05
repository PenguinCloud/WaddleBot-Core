import os
from pydal import DAL, Field

from flask import Flask, request
from flask_restx import Namespace, Resource, fields

from src.discord.managers.discord_manager import DiscordManager

# The connectionString is the path to the database.
connectionString = os.environ.get('db_conn_string')

# Initialize the database
db = DAL(connectionString, pool_size=0)

discordManager = DiscordManager(db)

# Add this portion of the api as a namespace

api = Namespace('Discord', description='Operations to interact with the discord bot')

# Response code for the API enpoints
apiResponses = {
    200: "The resource has been retrieved successfully",
    400: "General client error - further details are provided in the message",
    401: "No authentication credentials found",
    403: "Invalid authentication credentials",
    404: "The resource was not found",
    409: "The resource requested already exists",
    500: "General internal server error",
    504: "Timeout during communication with the backend service"
}

# Define the model for the discord
discord_model = api.model('Discord', {
    "channel": (fields.String(
        required=False,
        description='Name of the discord channel. This must be provided')),
    "community_id": (fields.Integer(
        required=False,
        description='ID of the community. This is not required.')),
    "servers": (fields.List(fields.String(
        required=False,
        description='List of servers. This is not required.'))),
    "aliases": (fields.List(fields.String(
        required=False,
        description='List of aliases. This is not required.')))
})


# Endpoints to handle Discord GET and POST requests
@api.route('/', methods=['GET', 'POST'])
class DiscordList(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        """
        Get all discord
        """
        response = discordManager.get_discords()
        
        return response 

    @api.doc(responses=apiResponses)
    @api.expect(discord_model)
    def post(self):
        """
        Create a new discord
        """
        data = request.json

        response = discordManager.create_discord(data)

        return response
    
# Endpoints to handle Discord GET, PUT, and DELETE requests, by channel name
@api.route('/<string:channel>', methods=['GET', 'PUT', 'DELETE'])
class Discord(Resource):
    @api.doc(responses=apiResponses)
    def get(self, channel):
        """
        Get a specific discord by channel name
        """
        response = discordManager.get_discord_by_channel(channel)
        
        return response

    @api.doc(responses=apiResponses)
    @api.expect(discord_model)
    def put(self, channel):
        """
        Update a discord by channel name
        """
        data = request.json

        response = discordManager.update_discord(channel, data)

        return response

    @api.doc(responses=apiResponses)
    def delete(self, channel):
        """
        Delete a discord by channel name
        """
        response = discordManager.remove_discord(channel)

        return response