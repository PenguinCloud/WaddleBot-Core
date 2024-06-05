from flask import Flask, request
from flask_restx import Resource, Api, fields, abort, Namespace
import logging
import apiutils
from flask_cors import CORS
import requests
from requests.auth import HTTPBasicAuth
import os
import base64
import json

from pydal import DAL, Field

from src.identity.namespaces.identity_namespace import api as identity_api

from src.community.namespaces.community_namespace import api as community_api

from src.community.namespaces.community_members_namespace import api as community_members_api

from src.community.namespaces.community_module_namespace import api as community_modules_api

from src.discord.namespaces.discord_namespace import api as discord_api

from src.roles.namespaces.roles_namespace import api as roles_api

from src.twitch.namespaces.twitch_namespace import api as twitch_api

# The connectionString is the path to the database.
connectionString = os.environ.get('db_conn_string')

# Initialize the database
db = DAL(connectionString, pool_size=0)

# Initialize the table managers
# identityManager = IdentityManager(db)
# discordManager = DiscordManager(db)
# twitchManager = TwitchManager(db)
# communityManager = CommunityManager(db)
# communityMembersManager = CommunityMembersManager(db)
# communityModuleManager = CommunityModuleManager(db)
# rolesManager = RolesManager(db)

logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)
app.config['RESTX_MASK_SWAGGER'] = False

api = Api(app, version='1.0.0', title='Waddle Bot Database Manager API',
          description='Waddle Bot Database Manager API',
          default='Waddle Bot Database Manager API',
          default_label='Waddle Bot Database Manager API')

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


# Function to turn a dictionary into a message to be sent back
def dict_to_message(data):
    message = ""
    for key in data:
        message += key + ": " + str(data[key]) + "\n"
    return message

# Function to turn a list of dictionaries into a message to be sent back
def list_to_message(data):
    message = ""
    for item in data:
        message += dict_to_message(item)
    return message

# Function to create Response Payload
def create_response_payload(data, message=None):
    response = {}
    response['data'] = data
    response['msg'] = message
    return response

# ==================================
# Identity Endpoints
# ==================================

# Add the identity namespace
api.add_namespace(identity_api, path='/identity')

# @api.route('/identity_new', methods=['POST'])
# @api.doc(parser=parser)
# class identity_post(Resource):
#     @api.expect(identity_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def post(self):
#         try:
#             print('Identity Creation request received')

#             # Get the data from the request
#             data = request.json

#             # Create the identity
#             msg = identityManager.create_identity(data['name'], data['country'], data['ip_address'], data['browser_fingerprints'])

#             # Generate a response to be sent back.
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')


# @api.route('/identity/<name>', methods=['GET'])
# @api.doc(parser=parser)
# class identity_get_by_name(Resource):
#     @api.doc(responses=apiResponses)
#     def get(self, name):
#         try:
#             print('Identity Retrieval request received')

#             # Get the identity
#             identity = identityManager.get_identity_by_name(name)

#             # Generate a response to be sent back.
#             response = create_response_payload(identity)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')

# @api.route('/identity_list', methods=['GET'])
# @api.doc(parser=parser)
# class identities_get(Resource):
#     @api.doc(responses=apiResponses)
#     def get(self):
#         try:
#             print('Identities Retrieval request received')

#             # Get all identities
#             identities = identityManager.get_all_identities()

#             # Generate a response to be sent back.
#             # response = [identity.as_dict() for identity in identities]
#             response = create_response_payload(identities)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')

# @api.route('/identity_delete/<identity_id>', methods=['DELETE'])
# @api.doc(parser=parser)
# class identity_delete(Resource):
#     @api.doc(responses=apiResponses)
#     def delete(self, identity_id):
#         try:
#             print('Identity Deletion request received')

#             # Delete the identity
#             msg = identityManager.delete_identity(identity_id)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')

# @api.route('/identity_update/<identity_id>', methods=['PUT'])
# @api.doc(parser=parser)
# class identity_update(Resource):
#     @api.expect(identity_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def put(self, identity_id):
#         try:
#             print('Identity Update request received')

#             # Get the data from the request
#             data = request.json

#             # Update the identity
#             msg = identityManager.update_identity(identity_id, data)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')

# ==================================
# Community Endpoints
# ==================================

# Add the community namespace
api.add_namespace(community_api, path='/community')

# @api.route('/community_new', methods=['POST'])
# @api.doc(parser=parser)
# class community_post(Resource):
#     @api.expect(community_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def post(self):
#         try:
#             print('Community Creation request received')

#             # Get the data from the request
#             data = request.json

#             # Create the community
#             msg = communityManager.create_community(data)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/community_list', methods=['GET'])
# @api.doc(parser=parser)
# class communities_list(Resource):
#     @api.doc(responses=apiResponses)
#     def get(self):
#         try:
#             print('Communities Retrieval request received')

#             # Get all communities
#             communities = communityManager.get_communities()

#             for community in communities:
#                 print(community.as_dict())
#             # print(communities)

#             # Create a message string from the list of communities to be sent back.
#             response_data = [community.as_dict() for community in communities]

#             # response = {'msg': message}
#             # Generate a response to be sent back.
#             response = create_response_payload(response_data, None)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/community/<community_name>', methods=['GET'])
# @api.doc(parser=parser)
# class community_get_by_name(Resource):
#     @api.doc(responses=apiResponses)
#     def get(self, community_name):
#         try:
#             # Get the community
#             community = communityManager.get_community_by_name(community_name)

#             # Generate a response to be sent back.
#             # response = community
#             response = create_response_payload([community])

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/community_delete/<community_name>', methods=['DELETE'])
# @api.doc(parser=parser)
# class community_delete(Resource):
#     @api.doc(responses=apiResponses)
#     def delete(self, community_name):
#         try:
#             print('Community Deletion request received')

#             # Delete the community
#             msg = communityManager.delete_community(community_name)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/community_update/<community_name>', methods=['PUT'])
# @api.doc(parser=parser)
# class community_update(Resource):
#     @api.expect(community_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def put(self, community_name):
#         try:
#             print('Community Update request received')

#             # Get the data from the request
#             data = request.json

#             # Update the community
#             msg = communityManager.update_community(community_name, data)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# # Function to update the descriptions of a community
# @api.route('/community_update_desc/<community_name>', methods=['PUT'])
# @api.doc(parser=parser)
# class community_update_desc(Resource):
#     @api.expect(community_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def put(self, community_name):
#         try:
#             print('Community Description Update request received')

#             # Get the data from the request
#             data = request.json

#             # Update the community description
#             msg = communityManager.update_community_description(community_name, data['community_description'])

#             # Generate a response to be sent back.
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# ==================================
# Community Members Endpoints
# ==================================

# Add the community members namespace
api.add_namespace(community_members_api, path='/community_members')

# ==================================
# Community Modules Endpoints
# ==================================

# Add the community modules namespace
api.add_namespace(community_modules_api, path='/community_modules')
            
# ==================================
# Roles Endpoints
# ==================================

# Add the roles namespace
api.add_namespace(roles_api, path='/roles')


# ==================================
# Discord Endpoints
# ==================================

# Add the discord namespace
api.add_namespace(discord_api, path='/discord')

# @api.route('/discord_new', methods=['POST'])
# @api.doc(parser=parser)
# class discord_post(Resource):
#     @api.expect(discord_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def post(self):
#         try:
#             print('Discord Creation request received')

#             # Get the data from the request
#             data = request.json

#             # Create the discord
#             msg = discordManager.create_discord(data['channel'], data['community_id'], data['servers'], data['aliases'])

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/discord_list', methods=['GET'])
# @api.doc(parser=parser)
# class discords_list(Resource):
#     @api.doc(responses=apiResponses)
#     def get(self):
#         try:
#             print('Discords Retrieval request received')

#             # Get all discords
#             discords = discordManager.get_discords()

#             # Generate a response to be sent back.
#             # response = [discord.as_dict() for discord in discords]
#             response = create_response_payload([discord.as_dict() for discord in discords])

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/discord/<channel>', methods=['GET'])
# @api.doc(parser=parser)
# class discord_get_by_channel(Resource):
#     @api.doc(responses=apiResponses)
#     def get(self, channel):
#         try:
#             print('Discord Retrieval request received')

#             # Get the discord
#             discord = discordManager.get_discord_by_channel(channel)

#             # Generate a response to be sent back.
#             # response = discord
#             response = create_response_payload(discord)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/discord_delete/<channel>', methods=['DELETE'])
# @api.doc(parser=parser)
# class discord_delete(Resource):
#     @api.doc(responses=apiResponses)
#     def delete(self, channel):
#         try:
#             print('Discord Deletion request received')

#             # Delete the discord
#             msg = discordManager.remove_discord(channel)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/discord_update/<channel>', methods=['PUT'])
# @api.doc(parser=parser)
# class discord_update(Resource):
#     @api.expect(discord_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def put(self, channel):
#         try:
#             print('Discord Update request received')

#             # Get the data from the request
#             data = request.json

#             # Update the discord
#             msg = discordManager.update_discord(channel, data)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# ==================================
# Twitch Endpoints
# ==================================

# Add the twitch namespace
api.add_namespace(twitch_api, path='/twitch')

# @api.route('/twitch_new', methods=['POST'])
# @api.doc(parser=parser)
# class twitch_post(Resource):
#     @api.expect(twitch_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def post(self):
#         try:
#             print('Twitch Creation request received')

#             # Get the data from the request
#             data = request.json

#             # Create the twitch
#             msg = twitchManager.create_twitch(data['channel'], data['community_id'], data['servers'], data['aliases'])

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/twitch_list', methods=['GET'])
# @api.doc(parser=parser)
# class twitch_list(Resource):
#     @api.doc(responses=apiResponses)
#     def get(self):
#         try:
#             print('Twitchs Retrieval request received')

#             # Get all twitchs
#             twitchs = twitchManager.get_twitchs()

#             # Generate a response to be sent back.
#             # response = [twitch.as_dict() for twitch in twitchs]
#             response = create_response_payload([twitch.as_dict() for twitch in twitchs])

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')

# @api.route('/twitch/<channel>', methods=['GET'])
# @api.doc(parser=parser)
# class twitch_get_by_channel(Resource):
#     @api.doc(responses=apiResponses)
#     def get(self, channel):
#         try:
#             print('Twitch Retrieval request received')

#             # Get the twitch
#             twitch = twitchManager.get_twitch_by_channel(channel)

#             # Generate a response to be sent back.
#             # response = twitch
#             response = create_response_payload(twitch)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/twitch_delete/<channel>', methods=['DELETE'])
# @api.doc(parser=parser)
# class twitch_delete(Resource):
#     @api.doc(responses=apiResponses)
#     def delete(self, channel):
#         try:
#             print('Twitch Deletion request received')

#             # Delete the twitch
#             msg = twitchManager.remove_twitch(channel)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            
# @api.route('/twitch_update/<channel>', methods=['PUT'])
# @api.doc(parser=parser)
# class twitch_update(Resource):
#     @api.expect(twitch_model, validate=False)
#     @api.doc(responses=apiResponses)
#     def put(self, channel):
#         try:
#             print('Twitch Update request received')

#             # Get the data from the request
#             data = request.json

#             # Update the twitch
#             msg = twitchManager.update_twitch(channel, data)

#             # Generate a response to be sent back.
#             # response = msg
#             response = create_response_payload(None, msg)

#             return response
#         except Exception as e:
#             abort(500,
#                 'Could Not Retrieve Data ' + str(e),
#                 status='error')
            

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

