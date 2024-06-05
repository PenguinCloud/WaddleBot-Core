import os
from pydal import DAL, Field

from flask import Flask, request
from flask_restx import Namespace, Resource, fields

from src.community.managers.community_manager import CommunityManager

# The connectionString is the path to the database.
connectionString = os.environ.get('db_conn_string')

# Initialize the database
db = DAL(connectionString, pool_size=0)

communityManager = CommunityManager(db)

# Add this portion of the api as a namespace
api = Namespace('Community', description='Operations to interact with the communities')

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

community_model = api.model('Community', {
    "community_name": (fields.String(
        required=False,
        description='Name of the community. This must be provided')),
    "community_description": (fields.String(
        required=False,
        description='Description of the community. This is not required.'))
})

# Endpoint to handle community GET and POST requests, without parameters
@api.route('/', methods=['GET', 'POST'])
class Community(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        """
        Get all communities
        """
        communities = communityManager.get_communities()

        return {"data":communities}
    
    @api.doc(responses=apiResponses)
    @api.expect(community_model)
    def post(self):
        """
        Create a new community
        """
        community = request.json

        response = communityManager.create_community(community)

        return {"msg":response}
    
# Endpoint to handle community GET, PUT, and DELETE requests, with a community name parameter
@api.route('/<community_name>', methods=['GET', 'PUT', 'DELETE'])
class Community(Resource):
    @api.doc(responses=apiResponses)
    def get(self, community_name):
        """
        Get a community by name
        """
        community = communityManager.get_community_by_name(community_name)

        return {"data":[community]}
    
    @api.doc(responses=apiResponses)
    @api.expect(community_model)
    def put(self, community_name):
        """
        Update a community by name
        """
        community = request.json

        response = communityManager.update_community(community_name, community)

        return {"msg":response}
    @api.doc(responses=apiResponses)
    def delete(self, community_name):
        """
        Delete a community by name
        """
        response = communityManager.delete_community(community_name)

        return {"msg":response} 