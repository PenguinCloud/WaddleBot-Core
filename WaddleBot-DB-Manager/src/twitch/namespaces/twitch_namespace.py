import os
from pydal import DAL, Field

from flask import Flask, request
from flask_restx import Namespace, Resource, fields

from src.twitch.managers.twitch_manager import TwitchManager

# The connectionString is the path to the database.
connectionString = os.environ.get('db_conn_string')

# Initialize the database
db = DAL(connectionString, pool_size=0)

twitchManager = TwitchManager(db)

# Add this portion of the api as a namespace
api = Namespace('Twitch', description='Operations to interact with the twitch table')

# Response code for the API endpoints
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

# Define the model for the twitch
twitch_model = api.model('Twitch', {
    "channel": (fields.String(
        required=False,
        description='Name of the twitch channel. This must be provided')),
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


# Endpoints to handle Twitch GET and POST requests
@api.route('/', methods=['GET', 'POST'])
class Twitch(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        """
        Get all twitch channels
        """
        twitch = twitchManager.get_twitch_channels()

        return twitch

    @api.doc(responses=apiResponses, body=twitch_model)
    def post(self):
        """
        Create a new twitch channel
        """
        data = request.json

        response = twitchManager.create_twitch(data)

        return response
    
# Endpoints to handle Twitch GET, PUT and DELETE requests by the channel parameter
@api.route('/<string:channel>', methods=['GET', 'PUT', 'DELETE'])
class TwitchChannel(Resource):
    @api.doc(responses=apiResponses)
    def get(self, channel):
        """
        Get a specific twitch channel
        """
        twitch = twitchManager.get_twitch_by_channel(channel)

        return twitch

    @api.doc(responses=apiResponses, body=twitch_model)
    def put(self, channel):
        """
        Update a specific twitch channel
        """
        data = request.json

        response = twitchManager.update_twitch(channel, data)

        return response

    @api.doc(responses=apiResponses)
    def delete(self, channel):
        """
        Delete a specific twitch channel
        """
        response = twitchManager.remove_twitch(channel)

        return response
