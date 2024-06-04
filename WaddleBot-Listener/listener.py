from src.matterbridge.matterbridge_link import WaddleBotListener

# Matterbridge API URL to manage messages
matterbridgeURL = 'http://localhost:4200/api/'

# User manager API URL to add users to the database
userManagerURL = 'http://localhost:8000/waddlebot_db_manager/identities/create.json/'

# Marketplace API URL to manage the marketplace
marketplaceURL = 'http://localhost:8000/marketplace_manager/marketplace/get_by_url.json'

# Redis parameters
redisHost = 'localhost'
redisPort = 6379

# The main function of the program
def main():
    matterbridgeGetURL = matterbridgeURL + 'messages'
    matterbridgePostURL = matterbridgeURL + 'message'

    # Initialize the Matterbridge Link
    listener = WaddleBotListener(matterbridgeGetURL, matterbridgePostURL, userManagerURL, redisHost, redisPort, marketplaceURL)

    # Start listening for messages
    listener.listen()
    

if __name__ == '__main__':
    main()