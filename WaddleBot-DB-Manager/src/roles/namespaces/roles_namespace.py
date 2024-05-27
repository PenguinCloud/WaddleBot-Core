import os
from pydal import DAL, Field

from flask import Flask, request
from flask_restx import Namespace, Resource, fields

from src.roles.managers.roles_manager import RolesManager

# The connectionString is the path to the database.
connectionString = os.environ.get('db_conn_string')

# Initialize the database
db = DAL(connectionString, pool_size=0)

rolesManager = RolesManager(db)

# Add this portion of the api as a namespace
api = Namespace('Roles', description='Operations to interact with the roles table')

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

# Define the model for the role
role_model = api.model('Role', {
    "name": (fields.String(
        required=False,
        description='Name of the role. This must be provided')),
    "description": (fields.String(
        required=False,
        description='Description of the role. This is not required.')),
    "privilages": (fields.List(fields.String(
        required=False,
        description='List of privilages. This is not required.'))),
    "requirements": (fields.List(fields.String(
        required=False,
        description='List of requirements. This is not required.')))
})


# Endpoints to handle Role GET and POST requests
@api.route('/', methods=['GET', 'POST'])
class Roles(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        """
        Get all roles
        """
        roles = rolesManager.get_roles()

        return roles

    @api.doc(responses=apiResponses, body=role_model)
    def post(self):
        """
        Create a new role
        """
        data = request.json
        
        response = rolesManager.create_role(data)

        return response
    
# Endpoints to handle Role GET, PUT and DELETE requests by the name parameter
@api.route('/<string:name>', methods=['GET', 'PUT', 'DELETE'])
class Role(Resource):
    @api.doc(responses=apiResponses)
    def get(self, name):
        """
        Get a role by name
        """
        role = rolesManager.get_role_by_name(name)

        return role

    @api.doc(responses=apiResponses, body=role_model)
    def put(self, name):
        """
        Update a role by name
        """
        data = request.json

        response = rolesManager.update_role(name, data)

        return response

    @api.doc(responses=apiResponses)
    def delete(self, name):
        """
        Delete a role by name
        """
        response = rolesManager.remove_role(name)

        return response