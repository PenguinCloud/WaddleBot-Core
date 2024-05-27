import os
from pydal import DAL, Field

from flask import Flask, request
from flask_restx import Namespace, Resource, fields

from src.community.managers.community_module_manager import CommunityModuleManager

# The connectionString is the path to the database.
connectionString = os.environ.get('db_conn_string')

# Initialize the database
db = DAL(connectionString, pool_size=0)

communityModuleManager = CommunityModuleManager(db)

# Add this portion of the api as a namespace
api = Namespace('Community Modules', description='Operations to interact with the community modules')

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

# Define the model for communities
community_module_model = api.model('CommunityModule', {
    "module_id": (fields.Integer(
        required=True,
        description='ID of the module. This must be provided')),
    "community_id": (fields.Integer(
        required=True,
        description='ID of the community. This must be provided')),
    "privilages": (fields.List(fields.String(
        required=False,
        description='List of privilages. This is not required.'))),
    "enabled": (fields.Boolean(
        required=False,
        description='Whether the module is enabled. This is not required.'))
})


# Endpoint to handle community module GET and POST requests
@api.route('/', methods=['GET', 'POST'])
class CommunityModule(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        """
        Get all community modules
        """
        communities = communityModuleManager.get_community_modules()

        return communities
    
    @api.doc(responses=apiResponses)
    @api.expect(community_module_model)
    def post(self):
        """
        Create a new community module
        """
        community_module = request.json

        response = communityModuleManager.create_community_module(community_module)

        return response
    
# Endpoint to handle community module GET requests by community id
@api.route('/<community_id>', methods=['GET'])
class CommunityModule(Resource):
    @api.doc(responses=apiResponses)
    def get(self, community_id):
        """
        Get a community module by name
        """
        community = communityModuleManager.get_community_modules_by_community_id(community_id)

        return community
    
# Endpoint to handle community module GET and DELETE requests by module id and community id
@api.route('/<module_id>/<community_id>', methods=['GET', 'DELETE'])
class CommunityModule(Resource):
    @api.doc(responses=apiResponses)
    def get(self, module_id, community_id):
        """
        Get a community module by module id and community id
        """
        community = communityModuleManager.get_community_module_by_module_id_and_community_id(module_id, community_id)

        return community
    
    @api.doc(responses=apiResponses)
    def delete(self, module_id, community_id):
        """
        Delete a community module by module id and community id
        """
        response = communityModuleManager.remove_community_module(module_id, community_id)

        return response