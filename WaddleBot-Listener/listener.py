from src.matterbridge.matterbridge_link import matterbridgelink

# Matterbridge API URL to manage messages
matterbridgeURL = 'http://localhost:4200/api/'

# User manager API URL to add users to the database
userManagerURL = 'http://localhost:5000/identity_new'

# Redis parameters
redisHost = 'localhost'
redisPort = 6379

# The main function of the program
def main():
    matterbridgeGetURL = matterbridgeURL + 'messages'
    matterbridgePostURL = matterbridgeURL + 'message'

    # Initialize the Matterbridge Link
    matterbridge = matterbridgelink(matterbridgeGetURL, matterbridgePostURL, userManagerURL, redisHost, redisPort)

    # Start listening for messages
    matterbridge.listen()
    

if __name__ == '__main__':
    main()