from src.listener.listener import WaddleBotListener

# Matterbridge API URL to manage messages
matterbridgeURL = 'http://localhost:4200/api/'

# User manager API URL to add users to the database
userManagerURL = 'http://localhost:8000/WaddleDBM/identities/create.json/'

# Marketplace API URL to manage the marketplace
marketplaceURL = 'http://localhost:8000/marketplace_manager/marketplace/get.json'

# Community Modules API URL to manage community modules to get the community modules
communityModulesURL = 'http://localhost:8000/WaddleDBM/community_modules/get_by_community_name_and_module_id.json/'

# Initial context API URL to set the initial context of new users to the database.
contextURL = 'http://localhost:8000/WaddleDBM/context/'

# Redis parameters
redisHost = 'localhost'
redisPort = 6379

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