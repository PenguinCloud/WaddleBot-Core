from flask import Flask
from flask_restx import Resource, Api, fields, reqparse, abort
import logging
import json
import os
from datetime import datetime
import base64
import sys
import requests
import logging

from namespaces.gateway_creator_namespace import gateway_creator_namespace
# from message_sender.twitch_msg import Twitch_Message_Sender

# Set the logging level
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

api = Api(app, version='1.0', title='WADDLEBOT GATEWAY CREATION API', description='API for the creation of gateways for waddlebot', validate=True)

api.add_namespace(gateway_creator_namespace)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

