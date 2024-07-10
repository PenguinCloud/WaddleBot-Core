import requests
import time
import re
from pydal import DAL, Field
from urllib.parse import quote, urlencode, quote_plus

from src.redis.redis_cache import RedisCache

class WaddleBotListener:
    def __init__(self, matterbridgeGetURL, matterbridgePostURL, contextURL, redisHost, redisPort, marketplaceURL, communityModulesURL):
        # Initialize the variables
        self.matterbridgeGetURL = matterbridgeGetURL
        self.matterbridgePostURL = matterbridgePostURL
        self.marketplaceURL = marketplaceURL
        self.communityModulesURL = communityModulesURL

        self.initialContextURL = contextURL + "initialize_user.json/"
        self.getContextURL = contextURL + "get_by_identity_name.json/"

        # Initialize the Redis Manager
        self.redisManager = RedisCache(redisHost, redisPort)

    # Function to listen for messages
    def listen(self):
        # TODO: When the Redis cache is implemented, remove the below execution of the add_test_commands function
        # Add the test commands to the Redis cache
        print("Adding test commands to Redis....")
        self.redisManager.add_test_commands()

        print("Listening for messages....")

        while True:
            # Check if the matterbridge API is reachable
            resp = None

            try: 
                resp = requests.get(self.matterbridgeGetURL)
            except requests.exceptions.RequestException as e:
                print(e)
                print("An error has occurred while trying to communicate with the API. Retrying in 1 second....")
                time.sleep(1)
                continue

            if resp is not None and resp.ok:
                messageData = resp.json()

                # Check if the message data is not empty
                if len(messageData) > 0:
                    print("FOUND MESSAGE!!")
                    print(messageData)

                    username = None

                    # Create a user if the user does not exist
                    if 'username' in messageData[0]:
                        username = messageData[0]['username']
                        self.add_identity(username)

                    if 'text' in messageData[0] and 'gateway' in messageData[0]:
                        gateway = messageData[0]['gateway']
                        message = messageData[0]['text']
                        channel = messageData[0]['channel']
                        account = messageData[0]['account']

                        if "!" in message and message[0] == "!" or "#" in message and message[0] == "#":
                            # Seperate the command from the message as the first item in the list
                            msgCommands = message.split(" ")

                            mainCommand = msgCommands[0]

                            commands = self.get_commands(mainCommand)

                            # commands = self.get_commands(msgCommand)

                            # print("The list of commands are:")
                            # print(commands)

                            # Execute the command
                            # commandResult = self.execute_command(command)

                            print("Command found in text. Looking up command....")

                            # Check if the command is in the botCommands dictionary
                            cmdResult = ""

                            # Get the userid from the message
                            pingUsername = "<@" + messageData[0]['userid'] + ">"

                            # Add the username to the response message
                            cmdResult += f"{pingUsername}, "

                            # If the command is !help, display the help message
                            if mainCommand == "!help":
                                cmdResult += self.display_help()
                            # Else, check if the command is in the Redis cache
                            else:
                                # Set the command as a Redis key
                                # redisCommand = self.set_redis_command(mainCommand)

                                # Get the command data from the Redis cache
                                commandName = self.redisManager.get_command(mainCommand)
                                if commandName is not None:
                                    print("Command found in Redis cache.")
                                    print(commandName)
                                    
                                    # Get marketplace module from the marketplace
                                    module = self.get_marketplace_module_by_name(commandName)

                                    if module is None:
                                        print("Error occured while trying to get the metadata from the marketplace.")
                                        cmdResult += "The command could not be found. Ensure that the command is typed correctly."
                                        self.send_bot_message(gateway, cmdResult, account)
                                        continue

                                    print("The module is:")
                                    print(module)
                                    metadata = module['metadata']
                                    moduleTypeName = module['module_type_name']
                                    moduleID = module['id']

                                    # Get the command properties from the metadata
                                    commandData = self.get_command_properties(msgCommands, metadata)

                                    print("The command data is:")
                                    print(commandData)

                                    # print("I GOT SOMETHING FROM THE MARKETPLACE!!!!")
                                    # print(metadata)

                                    # Execute the command
                                    cmdResult += self.execute_command(username, message, commandData, moduleID, moduleTypeName, channel)
                                else:
                                    print("Command not found in Redis cache.")
                                    cmdResult += "Command not found. Please use !help to see the list of available commands."

                            self.send_bot_message(gateway, cmdResult, account) 
                            
                        else:
                            print("No command tag found in message.")
                    else:
                        print("Error occured while processing the message. Either the 'gateway' or the 'text' attributes are missing.")
            else:
                print("An error has occurred while trying to communicate with the API.")

            time.sleep(1)

    # Function to set the list of commands as a singular redis key string by concatenating the commands with the underscore character
    def set_redis_command(self, commands):
        print("Setting the Redis command....")

        command = "_".join(commands)

        return command

    # Function to get the command from the message
    def get_commands(self, message):
        print("Getting the command from the message....")

        commands = []

        # Remove all strings from the message that fall between the [ ] brackets or the < > brackets
        message = re.sub(r'\[.*?\]', '', message)
        message = re.sub(r'\<.*?\>', '', message)

        # Get the first word from the message
        commands = message.split(" ")

        # Remove all strings from the list that fall between the [ ] brackets or the < > brackets
        commands = [x for x in commands if "[" not in x and "]" not in x and "<" not in x and ">" not in x]

        filteredCommands = []
        if len(commands) > 0:
            for command in commands:
                if command != "":
                    filteredCommands.append(command)

        print(f"The command list is:")
        print(filteredCommands)

        return filteredCommands
    
    # Function to get the command parameters from the message, that fall between the < > brackets
    def get_message_params(self, message):
        print("Getting the command parameters from the message....")

        # Get the command parameters from the message
        params = re.findall(r'\<(.*?)\>', message)

        return params
    
    # Function to get the payload values from the message, that fall between the [ ] brackets
    def get_payload_values(self, message):
        print("Getting the payload values from the message....")
        print(f"Message: {message}")

        # s=str(re.escape('['))
        # e=str(re.escape(']'))

        # Get the payload values from the message
        # values = re.findall(s+'(.*)'+e, message)

        # Find all occerences of the strings that fall between their own [ ] brackets
        values = re.findall(r'\[(.*?)\]', message)

        # If the values are is empty, return a list with only a singular empty string
        if len(values) == 0:
            values = []

            return values

        return values
    
    # Function to get the function parameters from a command retrieved from redis
    def get_function_params(self, commandData):
        print("Getting the function parameters from the command....")

        params = []
        # Get the function parameters from the command
        if commandData is not None and 'parameters' in commandData and len(commandData['parameters']) > 0:
            params = commandData['parameters']
        else:
            params = None

        return params

    # Function to get the payload keys from a command retrieved from redis
    def get_payload_keys(self, commandData):
        print("Getting the payload keys from the command....")

        keys = []
        # Get the payload keys from the command
        if commandData is not None and 'payload_keys' in commandData:
            keys = commandData['payload_keys']
        else:
            keys = None

        return keys
    
    # Function to get the action from the command data
    def get_action(self, commandData):
        print("Getting the action from the command data....")

        action = ""
        # Get the action from the command data
        if commandData is not None and 'action' in commandData:
            action = commandData['action']

        return action
    
    # Function to create a function URL with parameters by adding the parameters to the URL
    def create_function_url(self, action, params):
        print("Creating the function URL....")

        url = f"{action}"

        # Add the parameters to the URL
        for param in params:
            # Check if the parameter starts with a # character. If it does, replace the first character with %23.
            if param[0] == "#":
                param = "%23" + param[1:]

            url += f"/{param}"

        return url
    
    # Function to create a function payload with values by adding given values and keys to a dictionary
    def create_function_payload(self, keys, values, username):
        print("Creating the function payload....")

        # Create the payload dictionary
        payload = {}

        # Add the keys and values to the payload
        for i in range(len(keys)):
            payload[keys[i]] = values[i]

        # Add the username to the payload if it is not None
        print(f"Username to be added to the payload: {username}")
        if username is not None:
            payload['identity_name'] = username

        return payload
    
    # Function to check if a given community module exists in a given community, using the module id and the community id
    def check_community_module_exists(self, community_id, module_id):
        print("Checking if the community module exists....")

        # Create the function URL
        url = f"{self.communityModulesURL}{community_id}/{module_id}"

        resp = None

        try:
            resp = requests.get(url=url)
        except requests.exceptions.RequestException as e:
            print(e)
            return False

        if resp is not None and resp.ok:
            respJson = resp.json()

            if 'msg' in respJson and respJson['msg'] is not None:
                return False
            elif "community_module" in respJson:
                return True
        else:
            return False

    # Function to check if the given module type of a command is a core module
    def check_core_module(self, moduleType):
        print("Checking if the module is a core module....")

        if moduleType == "Core":
            return True
        else:
            return False
        
    # Function to check if a given module exists in a given community, using the module id and the community id
    def check_module_exists(self, community_id, module_id):
        print("Checking if the module exists....")

        # Create the function URL
        url = f"{self.communityModulesURL}{community_id}/{module_id}"
        print(f"THE URL TO GET THE MODULE IS: {url}")

        resp = None

        try:
            resp = requests.get(url=url)
        except requests.exceptions.RequestException as e:
            print(e)
            return False

        if resp is not None and  resp.ok:
            respJson = resp.json()

            if 'msg' in respJson and respJson['msg'] is not None:
                return False
            else:
                return True
        else:
            return False

    # Function to get the context of the current user
    def get_context(self, username):
        print("Getting the context....")

        # Create the function URL
        url = f"{self.getContextURL}{username}"

        resp = None

        try:
            resp = requests.get(url=url)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

        if resp is not None and resp.ok:
            respJson = resp.json()

            if 'msg' in respJson and respJson['msg'] is not None:
                return None
            elif "data" in respJson and "community_name" in respJson["data"]:
                return respJson["data"]["community_name"]
        else:
            return None


    # Function to execute a command from the Redis cache, given the message command and the command data
    def execute_command(self, username, message, commandData, moduleId, moduleTypeName, channel):
        print("Executing the command....")

        # Get the payload keys from the command data
        keys = self.get_payload_keys(commandData)
        
        # Get the function parameters from the command data
        funcParams = self.get_function_params(commandData)

        if keys is None:
            msg = "The command does not exist. Ensure that you typed it correctly."
            print(msg)
            return msg

        # Get the action value from the metadata
        action = commandData['action']

        community_name = self.get_context(username)

        # Get the command parameters from the message
        params = self.get_message_params(message)

        # Check if 'community_name' is in the function parameters. If it is, add the community name to the parameters at the beginning of the list
        if funcParams is not None and "community_name" in funcParams:
            params.insert(0, community_name)


        # Check if 'channel' is in the function parameters. If it is, add the channel to the parameters at the beginning of the list
        if funcParams is not None and "channel_id" in funcParams:
            params.insert(0, channel)
        
        # Check if the module_type_name is in the command data. After that, check if the module is a core module. If it is a core module
        # then execute the command. If it is not a core module, check if the module exists in the community. If it does, execute the command.
        # If it does not, return a message saying that the module does not exist in the community.
        if moduleTypeName is not None:
            if self.check_core_module(moduleTypeName):
                print("The module is a core module.")
            else:
                print("The module is not a core module.")
                
                # Check if the module exists in the current community context of the user
                if self.check_module_exists(community_name, moduleId):
                    print("The module exists in the community.")
                else:
                    print("The module does not exist in the community.")
                    return "The module does not exist in the community. Please install it first."

        # Get the payload values from the message
        values = self.get_payload_values(message)

        # Get the command description from the command meta data
        description = ""
        if 'description' in commandData:
            description = commandData['description']

        print(f"The keys before removing the identity_name key: {keys}")

        # Set the payload username value if the identity_name key is in the keys
        payloadUsername = None

        if "identity_name" in keys:
            payloadUsername = username
            # Remove the identity_name key from the keys
            keys.remove("identity_name")

        # # If the key identity_name is in the keys, add the username to the values as a dictionary with the isidentity flag set to True
        # for key in keys:
        #     if key == "identity_name":
        #         values.append(dict(value=username, isidentity=True))

        print(f"Keys: {keys}")
        print(f"Values: {values}")

        # Check if the number of keys and values match
        if len(keys) != len(values):
            msg = ""

            # If the command description was found, add it to the message
            if description != "":
                msg = f"Command description: {description}"
            else:
                msg = "The number of keys and values do not match."

            print(msg)
            return msg
        
        # Check if the number 

        # Create the function URL
        url = self.create_function_url(action, params)

        # Create the function payload
        payload = self.create_function_payload(keys, values, payloadUsername)

        print(f"URL: {url}")
        print(f"Payload: {payload}")

        resp = None

        # Execute the function, depending on the method
        if commandData['method'] == "GET":
            print("Executing GET Method")
            try:
                resp = requests.get(url=url, json=payload)
            except requests.exceptions.RequestException as e:
                print(e)
                return "An error has occurred while trying to execute the command."
        elif commandData['method'] == "POST":
            print("Executing POST Method")
            try:
                resp = requests.post(url=url, json=payload)
            except requests.exceptions.RequestException as e:
                print(e)
                return "An error has occurred while trying to execute the command."
        elif commandData['method'] == "PUT":
            print("Executing PUT Method")
            try:
                resp = requests.put(url=url, json=payload)
            except requests.exceptions.RequestException as e:
                print(e)
                return "An error has occurred while trying to execute the command."
        elif commandData['method'] == "DELETE":
            print("Executing DELETE Method")
            try:
                resp = requests.delete(url=url, json=payload)
            except requests.exceptions.RequestException as e:
                print(e)
                return "An error has occurred while trying to execute the command."

        if resp is not None and resp.ok:
            respJson = resp.json()

            msg = ""
            # Convert the response data to a string
            if 'msg' in respJson and respJson['msg'] is not None:
                msg = respJson['msg']
            elif "data" in respJson:
                msg = self.data_to_string(respJson["data"])
            
            print(msg)
            return msg
        else:
            msg = f"An error has occurred while trying to execute the command. Command description: {description}. Error: {resp.text}"
            print(msg)
            return msg

    # Function to send a bot message
    def send_bot_message(self, gateway, command, account):
        print("Sending Bot Message....")

        payload = {
            "text": f"{command}",
            "username": "Waddle Bot",
            "gateway": gateway,
            "account": account,
        }

        resp = requests.post(url=self.matterbridgePostURL, json=payload)

        if resp.ok:
            print("BOT Message Successfully Sent!")

    # Function to add an identity (User) to the database
    def add_identity(self, username):
        print("Adding Identity....")

        payload = {
            "identity_name": username
        }

        resp = requests.post(url=self.initialContextURL, json=payload)

        if resp.ok:
            # print('response:', resp.json())
            msg = ""
            if 'msg' in resp.json():
                msg = resp.json()['msg']
            print(msg) 
        

    # Function to turn a data dictionary response from a request into a string
    def data_to_string(self, data):
        print("Converting Data to String....")
        print("The given data:")
        print(data)

        # Convert the data dictionary to a string
        dataStr = ""
        if len(data) > 0:
            for count in range(len(data)):
                for key in data[count]:
                    dataStr += f"{key}: {data[count][key]}\n"

        return dataStr

    # Function to display the help message, containing all the associated commands from Redis
    def display_help(self):
        print("Displaying Help Message....")

        keys = self.redisManager.get_all_keys()
        # commands = self.redisManager.get_all_commands()

        # Print the commands
        # print("The commands are:")
        # print(commands)

        helpMessage = "Available Commands:\n"

        # Loop through the commands and display the command and its description.
        for key in keys:
            # Remove the _ character from the command key
            command = key.replace("_", " ")
            helpMessage += f"{command}\n"


        return helpMessage
    
    # Function to retrieve a marketplace module entry by its URL
    def get_marketplace_module_by_name(self, moduleName):
        print("Getting Marketplace Module by URL....")

        # Old call
        # callURL = self.marketplaceURL + "?url=" + quote_plus(url, safe='', encoding='utf-8')
        callURL = self.marketplaceURL + "/" + moduleName

        print(f"Call URL: {callURL}")

        resp = requests.get(url=callURL)

        if resp.ok:
            response = resp.json()
            marketplaceModule = response

            return marketplaceModule
        else:
            return None

    # Function to retrieve the metadata json object from a given marketplace module URL
    def get_marketplace_metadata(self, marketplaceModuleURL):
        print("Getting Marketplace Metadata....")

        callURL = self.marketplaceURL + "?url=" + quote_plus(marketplaceModuleURL, safe='', encoding='utf-8')

        print(f"Call URL: {callURL}")

        resp = requests.get(url=callURL)

        if resp.ok:
            response = resp.json()

            if 'metadata' in response:
                metadata = response['metadata']
                # print("The metadata is:")
                # print(metadata)

                return metadata

            else:
                return None
        else:
            return None
        
    # A function that accepts a string list, loops through each string and checks if they are present within one another in a given metadata object, and returns the command properties
    def get_command_properties(self, commandlist, metadata):
        print("Getting Command Properties....")

        print(f"Command List: {commandlist}")
        print(f"Metadata: {metadata}")

        # TODO: Find a way to dynamically generate a metadata key path, dependant on the length of the commandlist
        if metadata is not None and len(commandlist) > 0:
            if len(commandlist) == 1 and commandlist[0] in metadata and 'description' in metadata[commandlist[0]]:
                return metadata[commandlist[0]]
            elif len(commandlist) == 2 and commandlist[0] in metadata and commandlist[1] in metadata[commandlist[0]] and 'description' in metadata[commandlist[0]][commandlist[1]]:
                return metadata[commandlist[0]][commandlist[1]]
            elif len(commandlist) == 3 and commandlist[0] in metadata and commandlist[1] in metadata[commandlist[0]] and commandlist[2] in metadata[commandlist[0]][commandlist[1]] and 'description' in metadata[commandlist[0]][commandlist[1]][commandlist[2]]:
                return metadata[commandlist[0]][commandlist[1]][commandlist[2]]
            else:
                return None
                
            
        

    

