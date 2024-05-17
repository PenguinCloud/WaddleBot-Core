from src.matterbridge.matterbridge_link import matterbridgelink

# The connectionString is the path to the database.
connectionString = 'sqlite://src/db/test.db'

# Matterbridge API URL to send messages
requestURL = 'http://localhost:4200/api/'

# The main function of the program
def main():
    requestGetURL = requestURL + 'messages'
    requestPostURL = requestURL + 'message'

    # Initialize the Matterbridge Link
    matterbridge = matterbridgelink(requestGetURL, requestPostURL, connectionString)

    # Start listening for messages
    matterbridge.listen()
    

if __name__ == '__main__':
    main()