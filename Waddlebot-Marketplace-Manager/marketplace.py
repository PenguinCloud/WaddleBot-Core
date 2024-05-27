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

from src.marketplace.namespaces.marketplace_namespace import api as marketApi

from pydal import DAL, Field



logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)
app.config['RESTX_MASK_SWAGGER'] = False

api = Api(app, version='1.0.0', title='Waddle Bot Marketplace Manager API',
          description='Waddle Bot Marketplace Manager API',
          default='Waddle Bot Marketplace Manager API',
          default_label='Waddle Bot Marketplace Manager API')

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

# Add the marketplace namespace the API
api.add_namespace(marketApi, path='/marketplace')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6300)