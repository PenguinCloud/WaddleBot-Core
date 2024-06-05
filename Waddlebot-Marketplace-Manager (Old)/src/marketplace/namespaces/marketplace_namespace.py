from flask_restx import Namespace, Resource, fields
from pydal import DAL, Field
from urllib.parse import unquote

from src.marketplace.managers.marketplace_db_manager import MarketplaceDBManager

# Initialize the table managers
marketplaceManager = MarketplaceDBManager()

# Add this portion of the api as a namespace
api = Namespace('Marketplace', description='Operations to interact with the marketplace')

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

# Define the model for the marketplace
marketplace_model = api.model('Marketplace', {
    "name": (fields.String(
        required=True,
        description='Name of the marketplace. This must be provided')),
    "description": (fields.String(
        required=False,
        description='Description of the marketplace. This is not required.')),
    "gateway_url": (fields.String(
        required=False,
        description='URL of the gateway. This is not required.')),
    "module_type_id": (fields.Integer(
        required=False,
        description='ID of the module type. This is not required.')),
    "metadata": (fields.Raw(
        required=False,
        description='A json object to determine any additional needed parameters. This is not required.'))   
})

# Parser to accept the URL parameter
url_parser = api.parser()
url_parser.add_argument('url', type=str, help='URL of the marketplace module', location='args')

# Endpoint to GET and POST marketplaces from the marketplace database
@api.route('/', methods=['GET', 'POST'])
class Marketplace(Resource):
    @api.doc(responses=apiResponses)
    def get(self):
        """
        Get all marketplace modules
        """
        marketplaces = marketplaceManager.get_marketplace_modules()

        return marketplaces
    
    @api.doc(responses=apiResponses)
    @api.expect(marketplace_model)
    def post(self):
        """
        Create a new marketplace module
        """
        data = api.payload

        response = marketplaceManager.create_marketplace(data)

        return response
    
# Endpoints to GET, PUT and DELETE a marketplace module command endpoint by URL string
@api.route('/url', methods=['GET', 'PUT', 'DELETE'])
class MarketplaceURLParam(Resource):
    @api.doc(responses=apiResponses)
    @api.expect(url_parser)
    def get(self):
        """
        Get a marketplace module by URL 
        """
        
        args = url_parser.parse_args()
        url = args['url']

        url = unquote(url)
        print("THE UNQOUTED URL IS: ", url)

        marketplace = marketplaceManager.get_marketplace_by_url(url)

        return marketplace
    
    @api.doc(responses=apiResponses)
    @api.expect(marketplace_model)
    def put(self, url):
        """
        Update a marketplace module by URL
        """
        data = api.payload

        url = unquote(url)

        response = marketplaceManager.update_marketplace(url, data)

        return response
    
    @api.doc(responses=apiResponses)
    def delete(self, url):
        """
        Delete a marketplace module by URL
        """
        url = unquote(url)

        response = marketplaceManager.remove_marketplace(url)

        return response
    






    


