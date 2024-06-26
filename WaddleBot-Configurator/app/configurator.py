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
        mat_url = os.getenv('GATEWAYS_GET_URL')
        discord_name = os.getenv('USER_DISCORD_NAME')
        discord_server_id = os.getenv('USER_DISCORD_ID')
        discord_token = os.getenv('DISCORD_TOKEN')
        twitch_name = os.getenv('TWITCH_NAME')
        twitch_nick = os.getenv('TWITCH_NICK')
        twitch_token = os.getenv('TWITCH_TOKEN')
        api_name = os.getenv('API_NAME')
        api_address = os.getenv('API_ADDRESS')
        gateway_name = os.getenv('GATEWAY_NAME')

        gateways = get_gateways(mat_url)

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
            template = template.replace('{{gateway_name}}', gateway_name)

            template += '\n'

            # In the template file, add new sections for each gateway
            for gateway in gateways:
                if 'channel_id' in gateway and 'account' in gateway:
                    template += f'\n[[gateway.inout]]\naccount = "{gateway["account"]}"\nchannel = "{gateway["channel_id"]}"\n'

            out_file_path = os.path.join(script_dir, 'matterbridge.toml')

            # Write the new toml file "matterbridge.toml"
            with open(out_file_path, 'w') as file:
                file.write(template)

        msg = "Successfully created MAT configuration file"
        return(msg)

    except Exception as e:
        return(str(e))

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

if __name__ == "__main__":
    msg = main()
    print(msg)

