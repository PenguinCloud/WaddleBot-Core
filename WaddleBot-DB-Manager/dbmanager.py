from flask import Flask, request
from flask_restx import Resource, Api, fields, abort
import logging
import apiutils
from flask_cors import CORS
import requests
from requests.auth import HTTPBasicAuth
import os
import base64
import json

from pydal import DAL, Field

from src.identity.identity_manager import IdentityManager
from src.community.community_manager import CommunityManager
from src.community.community_members_manager import CommunityMembersManager
from src.community.community_module_manager import CommunityModuleManager
from src.roles.roles_manager import RolesManager
from src.discord.discord_manager import DiscordManager
from src.twitch.twitch_manager import TwitchManager
from src.marketplace.marketplace_manager import MarketplaceManager

# The connectionString is the path to the database.
connectionString = 'sqlite://src/db/test.db'

# Initialize the database
db = DAL(connectionString, pool_size=2)

# Initialize the table managers
identityManager = IdentityManager(db)
discordManager = DiscordManager(db)
twitchManager = TwitchManager(db)
marketplaceManager = MarketplaceManager(db)
communityManager = CommunityManager(db)
communityMembersManager = CommunityMembersManager(db)
communityModuleManager = CommunityModuleManager(db)
rolesManager = RolesManager(db)

logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)
app.config['RESTX_MASK_SWAGGER'] = False

api = Api(app, version='1.0.0', title='Waddle Bot Database Manager API',
          description='Waddle Bot Database Manager API',
          default='Waddle Bot Database Manager API',
          default_label='Waddle Bot Database Manager API')

# Function to create the database with its tables
def createDatabase():
    print("Creating the database, if not exists....")

    # Create the user table, if it doesnt exist
    identityManager.create_identity_table()

    # Create the community table, if it doesnt exist
    communityManager.create_community_table()

    # Create the community members table, if it doesnt exist
    communityMembersManager.create_community_members_table()

    # Create the community module table, if it doesnt exist
    communityModuleManager.create_community_module_table()

    # Create the roles table, if it doesnt exist
    rolesManager.create_roles_table()

    # Create the discord table, if it doesnt exist
    discordManager.create_discord_table()

    # Create the twitch table, if it doesnt exist
    twitchManager.create_twitch_table()

    # Create the marketplace table, if it doesnt exist
    marketplaceManager.create_marketplace_table()

    print("Database created successfully!")

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

parser = api.parser()

# Models for inserting/updating data
identity_model = api.model('Identity', {
    "name": (fields.String(
        required=False,
        description='Name of the user. This must be provided')),
    "country": (fields.String(
        required=False,
        description='Name of the country that the user is from. This is not required.')),
    "ip_address": (fields.String(
        required=False,
        description='IP Address of the user. This is not required.')),
    "browser_fingerprints": (fields.List(fields.String(
        required=False,
        description='List of browser fingerprints. This is not required.')))
})

community_model = api.model('Community', {
    "community_name": (fields.String(
        required=False,
        description='Name of the community. This must be provided')),
    "community_description": (fields.String(
        required=False,
        description='Description of the community. This is not required.'))
})

community_member_model = api.model('CommunityMember', {
    "community_id": (fields.String(
        required=False,
        description='ID of the community. This must be provided')),
    "member_id": (fields.String(
        required=False,
        description='ID of the member. This must be provided')),
    "role_id": (fields.String(
        required=False,
        description='ID of the role. This is not required.')),
    "currency": (fields.String(
        required=False,
        description='Currency of the member. This is not required.')),
    "reputation": (fields.String(
        required=False,
        description='Reputation of the member. This is not required.'))
})

community_module_model = api.model('CommunityModule', {
    "module_id": (fields.String(
        required=False,
        description='ID of the module. This must be provided')),
    "community_id": (fields.String(
        required=False,
        description='ID of the community. This must be provided')),
    "privilages": (fields.List(fields.String(
        required=False,
        description='List of privilages. This is not required.'))),
    "enabled": (fields.Boolean(
        required=False,
        description='Whether the module is enabled. This is not required.'))
})

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

discord_model = api.model('Discord', {
    "channel": (fields.String(
        required=False,
        description='Name of the discord channel. This must be provided')),
    "community_id": (fields.String(
        required=False,
        description='ID of the community. This is not required.')),
    "servers": (fields.List(fields.String(
        required=False,
        description='List of servers. This is not required.'))),
    "aliases": (fields.List(fields.String(
        required=False,
        description='List of aliases. This is not required.')))
})

twitch_model = api.model('Twitch', {
    "channel": (fields.String(
        required=False,
        description='Name of the twitch channel. This must be provided')),
    "community_id": (fields.String(
        required=False,
        description='ID of the community. This is not required.')),
    "servers": (fields.List(fields.String(
        required=False,
        description='List of servers. This is not required.'))),
    "aliases": (fields.List(fields.String(
        required=False,
        description='List of aliases. This is not required.')))
})

marketplace_model = api.model('Marketplace', {
    "name": (fields.String(
        required=False,
        description='Name of the marketplace. This must be provided')),
    "description": (fields.String(
        required=False,
        description='Description of the marketplace. This is not required.')),
    "gateway_url": (fields.String(
        required=False,
        description='URL of the gateway. This is not required.')),
    "module_type_id": (fields.String(
        required=False,
        description='ID of the module type. This is not required.')),
    "metadata": (fields.List(fields.String(
        required=False,
        description='List of metadata. This is not required.')))
})

# ==================================
# Identity Endpoints
# ==================================

@api.route('/identity_new', methods=['POST'])
@api.doc(parser=parser)
class identity_post(Resource):
    @api.expect(identity_model, validate=False)
    @api.doc(responses=apiResponses)
    def post(self):
        try:
            print('Identity Creation request received')

            # Get the data from the request
            data = request.json

            # Create the identity
            msg = identityManager.create_identity(data['name'], data['country'], data['ip_address'], data['browser_fingerprints'])

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))


@api.route('/identity/<name>', methods=['GET'])
@api.doc(parser=parser)
class identity_get_by_name(Resource):
    @api.doc(responses=apiResponses)
    def get(self, name):
        try:
            print('Identity Retrieval request received')

            # Get the identity
            identity = identityManager.get_identity_by_name(name)

            # Generate a response to be sent back.
            response = [identity.as_dict()]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))

@api.route('/identity_list', methods=['GET'])
@api.doc(parser=parser)
class identities_get(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        try:
            print('Identities Retrieval request received')

            # Get all identities
            identities = identityManager.get_all_identities()

            # Generate a response to be sent back.
            response = [identity.as_dict() for identity in identities]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))

@api.route('/identity_delete/<identity_id>', methods=['DELETE'])
@api.doc(parser=parser)
class identity_delete(Resource):
    @api.doc(responses=apiResponses)
    def delete(self, identity_id):
        try:
            print('Identity Deletion request received')

            # Delete the identity
            msg = identityManager.delete_identity(identity_id)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))

@api.route('/identity_update/<identity_id>', methods=['PUT'])
@api.doc(parser=parser)
class identity_update(Resource):
    @api.expect(identity_model, validate=False)
    @api.doc(responses=apiResponses)
    def put(self, identity_id):
        try:
            print('Identity Update request received')

            # Get the data from the request
            data = request.json

            # Update the identity
            msg = identityManager.update_identity(identity_id, data)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))

# ==================================
# Community Endpoints
# ==================================

@api.route('/community_new', methods=['POST'])
@api.doc(parser=parser)
class community_post(Resource):
    @api.expect(community_model, validate=False)
    @api.doc(responses=apiResponses)
    def post(self):
        try:
            print('Community Creation request received')

            # Get the data from the request
            data = request.json

            # Create the community
            msg = communityManager.create_community(data['community_name'], data['community_description'])

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_list', methods=['GET'])
@api.doc(parser=parser)
class communities_list(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        try:
            print('Communities Retrieval request received')

            # Get all communities
            communities = communityManager.get_communities()

            # Generate a response to be sent back.
            response = [community.as_dict() for community in communities]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community/<community_name>', methods=['GET'])
@api.doc(parser=parser)
class community_get_by_name(Resource):
    @api.doc(responses=apiResponses)
    def get(self, community_name):
        try:
            print('Community Retrieval request received')

            # Get the community
            community = communityManager.get_community_by_name(community_name)

            # Generate a response to be sent back.
            response = [community.as_dict()]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_delete/<community_name>', methods=['DELETE'])
@api.doc(parser=parser)
class community_delete(Resource):
    @api.doc(responses=apiResponses)
    def delete(self, community_name):
        try:
            print('Community Deletion request received')

            # Delete the community
            msg = communityManager.delete_community(community_name)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_update/<community_name>', methods=['PUT'])
@api.doc(parser=parser)
class community_update(Resource):
    @api.expect(community_model, validate=False)
    @api.doc(responses=apiResponses)
    def put(self, community_name):
        try:
            print('Community Update request received')

            # Get the data from the request
            data = request.json

            # Update the community
            msg = communityManager.update_community(community_name, data)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
# ==================================
# Community Members Endpoints
# ==================================

@api.route('/community_member_new', methods=['POST'])
@api.doc(parser=parser)
class community_member_post(Resource):
    @api.expect(community_member_model, validate=False)
    @api.doc(responses=apiResponses)
    def post(self):
        try:
            print('Community Member Creation request received')

            # Get the data from the request
            data = request.json

            # Create the community member
            msg = communityMembersManager.create_community_member(data['community_id'], data['member_id'], data['role_id'], data['currency'], data['reputation'])

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_member_list', methods=['GET'])
@api.doc(parser=parser)
class community_members_list(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        try:
            print('Community Members Retrieval request received')

            # Get all community members
            community_members = communityMembersManager.get_community_members()

            # Generate a response to be sent back.
            response = [community_member.as_dict() for community_member in community_members]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_member/<community_id>/<member_id>', methods=['GET'])
@api.doc(parser=parser)
class community_member_get_by_id(Resource):
    @api.doc(responses=apiResponses)
    def get(self, community_id, member_id):
        try:
            print('Community Member Retrieval request received')

            # Get the community member
            community_member = communityMembersManager.get_community_member_by_community_id_and_member_id(community_id, member_id)

            # Generate a response to be sent back.
            response = [community_member.as_dict()]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_member_delete/<community_id>/<member_id>', methods=['DELETE'])
@api.doc(parser=parser)
class community_member_delete(Resource):
    @api.doc(responses=apiResponses)
    def delete(self, community_id, member_id):
        try:
            print('Community Member Deletion request received')

            # Delete the community member
            msg = communityMembersManager.remove_community_member(community_id, member_id)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_member_update/<member_id>', methods=['PUT'])
@api.doc(parser=parser)
class community_member_update(Resource):
    @api.expect(community_member_model, validate=False)
    @api.doc(responses=apiResponses)
    def put(self, member_id):
        try:
            print('Community Member Update request received')

            # Get the data from the request
            data = request.json

            # Update the community member
            msg = communityMembersManager.update_community_member(member_id, data)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
# ==================================
# Community Modules Endpoints
# ==================================

@api.route('/community_module_new', methods=['POST'])
@api.doc(parser=parser)
class community_module_post(Resource):
    @api.expect(community_module_model, validate=False)
    @api.doc(responses=apiResponses)
    def post(self):
        try:
            print('Community Module Creation request received')

            # Get the data from the request
            data = request.json

            # Create the community module
            msg = communityModuleManager.create_community_module(data['module_id'], data['community_id'], data['privilages'], data['enabled'])

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_module_list', methods=['GET'])
@api.doc(parser=parser)
class community_modules_list(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        try:
            print('Community Modules Retrieval request received')

            # Get all community modules
            community_modules = communityModuleManager.get_community_modules()

            # Generate a response to be sent back.
            response = [community_module.as_dict() for community_module in community_modules]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_module/<module_id>/<community_id>', methods=['GET'])
@api.doc(parser=parser)
class community_module_get_by_id(Resource):
    @api.doc(responses=apiResponses)
    def get(self, module_id, community_id):
        try:
            print('Community Module Retrieval request received')

            # Get the community module
            community_module = communityModuleManager.get_community_module_by_module_id_and_community_id(module_id, community_id)

            # Generate a response to be sent back.
            response = [community_module.as_dict()]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_module_delete/<module_id>/<community_id>', methods=['DELETE'])
@api.doc(parser=parser)
class community_module_delete(Resource):
    @api.doc(responses=apiResponses)
    def delete(self, module_id, community_id):
        try:
            print('Community Module Deletion request received')

            # Delete the community module
            msg = communityModuleManager.remove_community_module(module_id, community_id)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/community_module_update/<module_id>/<community_id>', methods=['PUT'])
@api.doc(parser=parser)
class community_module_update(Resource):
    @api.expect(community_module_model, validate=False)
    @api.doc(responses=apiResponses)
    def put(self, module_id, community_id):
        try:
            print('Community Module Update request received')

            # Get the data from the request
            data = request.json

            # Update the community module
            msg = communityModuleManager.update_community_module(module_id, data)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
# ==================================
# Roles Endpoints
# ==================================

@api.route('/role_new', methods=['POST'])
@api.doc(parser=parser)
class role_post(Resource):
    @api.expect(role_model, validate=False)
    @api.doc(responses=apiResponses)
    def post(self):
        try:
            print('Role Creation request received')

            # Get the data from the request
            data = request.json

            # Create the role
            msg = rolesManager.create_role(data['name'], data['description'], data['privilages'], data['requirements'])

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/role_list', methods=['GET'])
@api.doc(parser=parser)
class roles_list(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        try:
            print('Roles Retrieval request received')

            # Get all roles
            roles = rolesManager.get_roles()

            # Generate a response to be sent back.
            response = [role.as_dict() for role in roles]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/role/<role_name>', methods=['GET'])
@api.doc(parser=parser)
class role_get_by_name(Resource):
    @api.doc(responses=apiResponses)
    def get(self, role_name):
        try:
            print('Role Retrieval request received')

            # Get the role
            role = rolesManager.get_role_by_name(role_name)

            # Generate a response to be sent back.
            response = [role.as_dict()]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/role_delete/<role_name>', methods=['DELETE'])
@api.doc(parser=parser)
class role_delete(Resource):
    @api.doc(responses=apiResponses)
    def delete(self, role_name):
        try:
            print('Role Deletion request received')

            # Delete the role
            msg = rolesManager.remove_role(role_name)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/role_update/<role_name>', methods=['PUT'])
@api.doc(parser=parser)
class role_update(Resource):
    @api.expect(role_model, validate=False)
    @api.doc(responses=apiResponses)
    def put(self, role_name):
        try:
            print('Role Update request received')

            # Get the data from the request
            data = request.json

            # Update the role
            msg = rolesManager.update_role(role_name, data)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))

# ==================================
# Discord Endpoints
# ==================================

@api.route('/discord_new', methods=['POST'])
@api.doc(parser=parser)
class discord_post(Resource):
    @api.expect(discord_model, validate=False)
    @api.doc(responses=apiResponses)
    def post(self):
        try:
            print('Discord Creation request received')

            # Get the data from the request
            data = request.json

            # Create the discord
            msg = discordManager.create_discord(data['channel'], data['community_id'], data['servers'], data['aliases'])

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/discord_list', methods=['GET'])
@api.doc(parser=parser)
class discords_list(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        try:
            print('Discords Retrieval request received')

            # Get all discords
            discords = discordManager.get_discords()

            # Generate a response to be sent back.
            response = [discord.as_dict() for discord in discords]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/discord/<channel>', methods=['GET'])
@api.doc(parser=parser)
class discord_get_by_channel(Resource):
    @api.doc(responses=apiResponses)
    def get(self, channel):
        try:
            print('Discord Retrieval request received')

            # Get the discord
            discord = discordManager.get_discord_by_channel(channel)

            # Generate a response to be sent back.
            response = [discord.as_dict()]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/discord_delete/<channel>', methods=['DELETE'])
@api.doc(parser=parser)
class discord_delete(Resource):
    @api.doc(responses=apiResponses)
    def delete(self, channel):
        try:
            print('Discord Deletion request received')

            # Delete the discord
            msg = discordManager.remove_discord(channel)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/discord_update/<channel>', methods=['PUT'])
@api.doc(parser=parser)
class discord_update(Resource):
    @api.expect(discord_model, validate=False)
    @api.doc(responses=apiResponses)
    def put(self, channel):
        try:
            print('Discord Update request received')

            # Get the data from the request
            data = request.json

            # Update the discord
            msg = discordManager.update_discord(channel, data)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
# ==================================
# Twitch Endpoints
# ==================================

@api.route('/twitch_new', methods=['POST'])
@api.doc(parser=parser)
class twitch_post(Resource):
    @api.expect(twitch_model, validate=False)
    @api.doc(responses=apiResponses)
    def post(self):
        try:
            print('Twitch Creation request received')

            # Get the data from the request
            data = request.json

            # Create the twitch
            msg = twitchManager.create_twitch(data['channel'], data['community_id'], data['servers'], data['aliases'])

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/twitch_list', methods=['GET'])
@api.doc(parser=parser)
class twitch_list(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        try:
            print('Twitchs Retrieval request received')

            # Get all twitchs
            twitchs = twitchManager.get_twitchs()

            # Generate a response to be sent back.
            response = [twitch.as_dict() for twitch in twitchs]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))

@api.route('/twitch/<channel>', methods=['GET'])
@api.doc(parser=parser)
class twitch_get_by_channel(Resource):
    @api.doc(responses=apiResponses)
    def get(self, channel):
        try:
            print('Twitch Retrieval request received')

            # Get the twitch
            twitch = twitchManager.get_twitch_by_channel(channel)

            # Generate a response to be sent back.
            response = [twitch.as_dict()]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/twitch_delete/<channel>', methods=['DELETE'])
@api.doc(parser=parser)
class twitch_delete(Resource):
    @api.doc(responses=apiResponses)
    def delete(self, channel):
        try:
            print('Twitch Deletion request received')

            # Delete the twitch
            msg = twitchManager.remove_twitch(channel)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/twitch_update/<channel>', methods=['PUT'])
@api.doc(parser=parser)
class twitch_update(Resource):
    @api.expect(twitch_model, validate=False)
    @api.doc(responses=apiResponses)
    def put(self, channel):
        try:
            print('Twitch Update request received')

            # Get the data from the request
            data = request.json

            # Update the twitch
            msg = twitchManager.update_twitch(channel, data)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
# ==================================
# Marketplace Endpoints
# ==================================

@api.route('/marketplace_new', methods=['POST'])
@api.doc(parser=parser)
class marketplace_new(Resource):
    @api.expect(marketplace_model, validate=False)
    @api.doc(responses=apiResponses)
    def post(self):
        try:
            print('Marketplace Creation request received')

            # Get the data from the request
            data = request.json

            # Create the marketplace
            msg = marketplaceManager.create_marketplace(data['name'], data['description'], data['gateway_url'], data['module_type_id'], data['metadata'])

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/marketplace_list', methods=['GET'])
@api.doc(parser=parser)
class marketplaces(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        try:
            print('Marketplaces Retrieval request received')

            # Get all marketplaces
            marketplaces = marketplaceManager.get_marketplace_modules()

            # Generate a response to be sent back.
            response = [marketplace.as_dict() for marketplace in marketplaces]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/marketplace/<name>', methods=['GET'])
@api.doc(parser=parser)
class marketplace(Resource):
    @api.doc(responses=apiResponses)
    def get(self, name):
        try:
            print('Marketplace Retrieval request received')

            # Get the marketplace
            marketplace = marketplaceManager.get_marketplace_by_name(name)

            # Generate a response to be sent back.
            response = [marketplace.as_dict()]

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/marketplace_delete/<name>', methods=['DELETE'])
@api.doc(parser=parser)
class marketplace_delete(Resource):
    @api.doc(responses=apiResponses)
    def delete(self, name):
        try:
            print('Marketplace Deletion request received')

            # Delete the marketplace
            msg = marketplaceManager.remove_marketplace(name)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            
@api.route('/marketplace_update/<name>', methods=['PUT'])
@api.doc(parser=parser)
class marketplace_update(Resource):
    @api.expect(marketplace_model, validate=False)
    @api.doc(responses=apiResponses)
    def put(self, name):
        try:
            print('Marketplace Update request received')

            # Get the data from the request
            data = request.json

            # Update the marketplace
            msg = marketplaceManager.update_marketplace(name, data)

            # Generate a response to be sent back.
            response = msg

            return response
        except Exception as e:
            abort(500,
                'Could Not Retrieve Data ' + str(e),
                status='error', uuid=str(apiutils.request_id()))
            

if __name__ == '__main__':
    createDatabase()
    app.run(host='0.0.0.0', port=5000)

