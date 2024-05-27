import os
from pydal import DAL, Field

from flask import Flask, request
from flask_restx import Namespace, Resource, fields

from src.identity.managers.identity_manager import IdentityManager

# The connectionString is the path to the database.
connectionString = os.environ.get('db_conn_string')

# Initialize the database
db = DAL(connectionString, pool_size=0)

identityManager = IdentityManager(db)

# Add this portion of the api as a namespace
api = Namespace('Identity', description='Operations to interact with the identity table')

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

# Define the model for the identity
identity_model = api.model('Identity', {
    "name": (fields.String(
        required=False,
        description='Name of the identity. This must be provided')),
    "country": (fields.String(
        required=False,
        description='Country of the identity. This is not required.')),
    "ip_address": (fields.String(
        required=False,
        description='IP address of the identity. This is not required.')),
    "browser_fingerprints": (fields.List(fields.String(
        required=False,
        description='List of browser fingerprints. This is not required.')))
})


# Endpoints to handle Identity GET and POST requests
@api.route('/', methods=['GET', 'POST'])
class IdentityList(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        """
        Get all identities
        """
        response = identityManager.get_all_identities()
        
        return response 

    @api.doc(responses=apiResponses)
    @api.expect(identity_model)
    def post(self):
        """
        Create a new identity
        """
        data = request.json

        response = identityManager.create_identity(data)
        
        return response
    
# Endpoints to handle Identity GET, PUT, and DELETE requests
@api.route('/<string:name>', methods=['GET', 'PUT', 'DELETE'])
class Identity(Resource):
    @api.doc(responses=apiResponses)
    def get(self, name):
        """
        Get a specific identity by name
        """
        response = identityManager.get_identity_by_name(name)
        
        return response

    @api.doc(responses=apiResponses)
    @api.expect(identity_model)
    def put(self, name):
        """
        Update an identity by name
        """
        data = request.json

        response = identityManager.update_identity(name, data)
        
        return response

    @api.doc(responses=apiResponses)
    def delete(self, name):
        """
        Delete an identity by name
        """
        response = identityManager.delete_identity(name)
        
        return response
