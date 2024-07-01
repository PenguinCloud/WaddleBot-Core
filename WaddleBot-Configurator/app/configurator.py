import toml
import requests
import os
from dotenv import load_dotenv

# The main function that will be called when the script is run
def main():
    # Check if the .env file exists
    try:
        # load_dotenv() 

        # If the .env file exists, get the values of the environment variables
        # and store them in variables
        gateways_url = os.getenv('GATEWAYS_GET_URL')
        community_routes_url = os.getenv('COM_ROUTES_GET_URL')
        discord_name = os.getenv('USER_DISCORD_NAME')
        discord_server_id = os.getenv('USER_DISCORD_ID')
        discord_token = os.getenv('DISCORD_TOKEN')
        twitch_name = os.getenv('TWITCH_NAME')
        twitch_nick = os.getenv('TWITCH_NICK')
        twitch_token = os.getenv('TWITCH_TOKEN')
        api_name = os.getenv('API_NAME')
        api_address = os.getenv('API_ADDRESS')

        gateways = get_gateways(gateways_url)
        community_routes = get_community_routes(community_routes_url)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'mat_template.toml')

        # Load the template toml file "mat_template.toml" in the "templates" folder
        with open(file_path, 'r') as file:
            template = file.read()

            # Replace the placeholders in the template file with the environment variables
            template = template.replace('{{discord_gateway_name}}', discord_name)
            template = template.replace('{{discord_server_id}}', discord_server_id)
            template = template.replace('{{discord_token}}', discord_token)
            template = template.replace('{{twitch_gateway_name}}', twitch_name)
            template = template.replace('{{twitch_nick}}', twitch_nick)
            template = template.replace('{{twitch_token}}', twitch_token)
            template = template.replace('{{api_gateway_name}}', api_name)
            template = template.replace('{{api_address}}', api_address)
            # template = template.replace('{{gateway_name}}', gateway_name)

            template += '\n'

            # In the template file, add new sections for each gateway
            # for gateway in gateways:
            #     if 'channel_id' in gateway and 'account' in gateway:
            #         template += f'\n[[gateway.inout]]\naccount = "{gateway["account"]}"\nchannel = "{gateway["channel_id"]}"\n'

            # Create the global community toml object string
            global_community_toml = create_gateways(gateways, api_name)

            # Create the community toml object string
            # community_toml = create_community_toml(community_routes, gateways, api_name)

            # Add the global community to the template file
            template += global_community_toml

            # Add the community to the template file
            # template += community_toml

            # Get the path of the script directory and the output file path
            out_file_path = os.path.join(script_dir, 'matterbridge.toml')

            # Write the new toml file "matterbridge.toml"
            with open(out_file_path, 'w') as file:
                file.write(template)

        msg = "Successfully created MAT configuration file"
        return(msg)

    except Exception as e:
        return(str(e))

# Function that creates a toml object string for each community in a list of communities and gateways, by checking 
# which community has a list of gateways and then using the gateways in the other list to create the toml object string
def create_community_toml(community_routes, gateways, api_name):
    toml_string = ""

    for community in community_routes:
        if 'gateways' in community and len(community['gateways']) > 0:
            toml_string += f'\n[[gateway]]\nname="{community["community_name"]}"\nenable=true\n'

            for com_gateway in community['gateways']:
                for gateway in gateways:
                    if 'channel_id' in gateway and 'account' in gateway and gateway['channel_id'] == com_gateway:
                        toml_string += f'\n[[gateway.inout]]\naccount="{gateway["account"]}"\nchannel="{gateway["channel_id"]}"\n'

            # Add the api gateway inout to the global community toml object string
            toml_string += f'\n[[gateway.inout]]\naccount = "api.{api_name}"\nchannel = "api"\n'

    return toml_string

# Function to create a gateway opject for each gateway in the list of gateways
def create_gateways(gateways, api_name):
    toml_string = ""

    # Create all the gateway objects
    for gateway in gateways:
        # Create the first part of the toml string to contain the gateway name
        toml_string += f'\n[[gateway]]\nname = "{gateway["channel_id"]}"\nenable=true\n'

        # Create the second part of the toml string to contain the gateway inout objects
        toml_string += f'\n[[gateway.inout]]\naccount="{gateway["account"]}"\nchannel="{gateway["channel_id"]}"\n'

        # Add the api gateway inout toml object string
        toml_string += f'\n[[gateway.inout]]\naccount = "api.{api_name}"\nchannel = "api"\n'

    return toml_string

# Function to get the gateways from the API
def get_gateways(url):
    # Make a GET request to the MAT API to get the gateways
    response = requests.get(url)

    gateways = []

    # Check if the response is successful
    if response.status_code == 200:
        # Check that the response is in JSON format and that the key "data" exists
        if response.headers['Content-Type'] == 'application/json' and 'data' in response.json():
            response_json = response.json()
            gateways = response_json['data']
    else:
        print("Failed to get gateways from MAT API")
        return None

    # Check if the gateways list is not empty
    if len(gateways) == 0:
        print("No gateways found")
        return None
    
    return gateways

# Function to get the community routes from the API
def get_community_routes(url):
    # Make a GET request to the MAT API to get the community routes
    response = requests.get(url)

    community_routes = []

    # Check if the response is successful
    if response.status_code == 200:
        # Check that the response is in JSON format and that the key "data" exists
        if response.headers['Content-Type'] == 'application/json' and 'data' in response.json():
            response_json = response.json()
            community_routes = response_json['data']
    else:
        print("Failed to get community routes from MAT API")
        return None

    # Check if the community routes list is not empty
    if len(community_routes) == 0:
        print("No community routes found")
        return None
    
    return community_routes

if __name__ == "__main__":
    msg = main()
    print(msg)

