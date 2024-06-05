import os
from pydal import DAL, Field

from flask import Flask, request
from flask_restx import Namespace, Resource, fields

from src.community.managers.community_members_manager import CommunityMembersManager

# The connectionString is the path to the database.
connectionString = os.environ.get('db_conn_string')

# Initialize the database
db = DAL(connectionString, pool_size=0)

communityMembersManager = CommunityMembersManager(db)

# Add this portion of the api as a namespace
api = Namespace('Community Members', description='Operations to interact with the community members')

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
community_member_model = api.model('CommunityMember', {
    "community_id": (fields.Integer(
        required=True,
        description='ID of the community. This must be provided')),
    "member_id": (fields.Integer(
        required=True,
        description='ID of the member. This must be provided')),
    "role_id": (fields.Integer(
        required=False,
        description='ID of the role. This is not required.')),
    "currency": (fields.Integer(
        required=False,
        description='Currency of the member. This is not required.')),
    "reputation": (fields.Integer(
        required=False,
        description='Reputation of the member. This is not required.'))
})


# Endpoint to handle community member GET and POST requests
@api.route('/', methods=['GET', 'POST'])
class CommunityMember(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        """
        Get all community members
        """
        communities = communityMembersManager.get_community_members()

        return communities

    @api.doc(responses=apiResponses)
    @api.expect(community_member_model)
    def post(self):
        """
        Create a new community member
        """
        community_member_data = request.json

        response = communityMembersManager.create_community_member(community_member_data)

        return response
    
# Endpoint to handle community member GET requests by community id
@api.route('/<community_id>', methods=['GET'])
class CommunityMember(Resource):
    @api.doc(responses=apiResponses)
    def get(self, community_id):
        """
        Get all community members by community id
        """
        communities = communityMembersManager.get_community_members_by_community_id(community_id)

        return communities
    
# Endpoint to handle community member GET and DELETE requests by community id and member id
@api.route('/<community_id>/<member_id>', methods=['GET', 'DELETE'])
class CommunityMember(Resource):
    @api.doc(responses=apiResponses)
    def get(self, member_id, community_id):
        """
        Get a community member by member id and community id
        """
        community = communityMembersManager.get_community_member_by_community_id_and_member_id(community_id, member_id)

        return community

    @api.doc(responses=apiResponses)
    def delete(self, member_id, community_id):
        """
        Delete a community member by member id and community id
        """
        response = communityMembersManager.remove_community_member(community_id, member_id)

        return response
