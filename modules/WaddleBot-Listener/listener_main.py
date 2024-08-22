from src.listener.listener import WaddleBotListener
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Matterbridge API URL to manage messages
matterbridgeURL = os.getenv('MATTERBRIDGE_URL')

# User manager API URL to add users to the database
userManagerURL = os.getenv('USER_MANAGER_URL')

# Marketplace API URL to manage the marketplace
marketplaceURL = os.getenv('MARKETPLACE_URL')

# Community Modules API URL to manage community modules to get the community modules
communityModulesURL = os.getenv('COMMUNITY_MODULES_URL')

# Initial context API URL to set the initial context of new users to the database.
contextURL = os.getenv('CONTEXT_URL')

# Redis parameters
redisHost = os.getenv('REDIS_HOST')
redisPort = os.getenv('REDIS_PORT')

# The main function of the program
def main() -> None:
    matterbridgeGetURL = matterbridgeURL + 'messages'
    matterbridgePostURL = matterbridgeURL + 'message'

    # Initialize the Matterbridge Link
    listener = WaddleBotListener(matterbridgeGetURL, matterbridgePostURL, contextURL, redisHost, redisPort, marketplaceURL, communityModulesURL)

    # Start listening for messages
    listener.listen()
    

if __name__ == '__main__':
    main()