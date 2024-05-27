import requests
import time
import re
from pydal import DAL, Field
from urllib.parse import quote, urlencode, quote_plus

from src.redis.redis_cache import RedisCache

class WaddleBotListener:
    def __init__(self, matterbridgeGetURL, matterbridgePostURL, userManagerURL, redisHost, redisPort, marketplaceURL):
        # Initialize the variables
        self.matterbridgeGetURL = matterbridgeGetURL
        self.matterbridgePostURL = matterbridgePostURL
        self.userManagerURL = userManagerURL
        self.marketplaceURL = marketplaceURL

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
            resp = requests.get(self.matterbridgeGetURL)
            if resp.ok:
                messageData = resp.json()

                # Check if the message data is not empty
                if len(messageData) > 0:
                    print("FOUND MESSAGE!!")
                    print(messageData)

                    # Create a user if the user does not exist
                    # if 'username' in messageData[0]:
                    #     self.add_identity(messageData[0]['username'])

                    if 'text' in messageData[0] and 'gateway' in messageData[0]:
                        gateway = messageData[0]['gateway']
                        message = messageData[0]['text']

                        if "!" in message and message[0] == "!":
                            commands = self.get_commands(message)

                            # print("The list of commands are:")
                            # print(commands)

                            # Execute the command
                            # commandResult = self.execute_command(command)

                            print("Command found in text. Looking up command....")

                            # Check if the command is in the botCommands dictionary
                            cmdResult = ""

                            # Get the userid from the message
                            username = "<@" + messageData[0]['userid'] + ">"

                            # Add the username to the response message
                            cmdResult += f"{username}, "

                            # If the command is !help, display the help message
                            if commands[0] == "!help":
                                cmdResult += self.display_help()
                            # Else, check if the command is in the Redis cache
                            else:
                                # Remove the '!' from the command
                                redisCommand = commands[0]

                                # Get the command data from the Redis cache
                                commandURL = self.redisManager.get_command(redisCommand)
                                if commandURL is not None:
                                    print("Command found in Redis cache.")
                                    print(commandURL)
                                    
                                    # Get command metadata from the marketplace
                                    metadata = self.get_marketplace_metadata(commandURL)

                                    if metadata is None:
                                        print("Error occured while trying to get the metadata from the marketplace.")
                                        cmdResult += "The command could not be found. Ensure that the command is typed correctly."
                                        self.send_bot_message(gateway, cmdResult)
                                        continue

                                    # Get the command properties from the metadata
                                    commandData = self.get_command_properties(commands, metadata)

                                    print("The command data is:")
                                    print(commandData)

                                    # print("I GOT SOMETHING FROM THE MARKETPLACE!!!!")
                                    # print(metadata)

                                    # Execute the command
                                    cmdResult += self.execute_command(message, commandData, commandURL)
                                else:
                                    print("Command not found in Redis cache.")
                                    cmdResult += "Command not found. Please use !help to see the list of available commands."

                            self.send_bot_message(gateway, cmdResult) 
                            
                        else:
                            print("No command tag found in message.")
                    else:
                        print("Error occured while processing the message. Either the 'gateway' or the 'text' attributes are missing.")
            else:
                print("An error has occurred while trying to communicate with the API.")

            time.sleep(1)

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
    def get_command_params(self, message):
        print("Getting the command parameters from the message....")

        # Get the command parameters from the message
        params = re.findall(r'<(.*?)>', message)

        return params
    
    # Function to get the payload values from the message, that fall between the [ ] brackets
    def get_payload_values(self, message):
        print("Getting the payload values from the message....")
        print(f"Message: {message}")

        s=str(re.escape('['))
        e=str(re.escape(']'))

        # Get the payload values from the message
        values = re.findall(s+'(.*)'+e, message)

        # If the values are is empty, return a list with only a singular empty string
        if len(values) == 0:
            values = []

        return values
    
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
    
    # Function to create a function URL with parameters by adding the parameters to the URL
    def create_function_url(self, url, params):
        print("Creating the function URL....")

        # Add the parameters to the URL
        for param in params:
            url += f"/{param}"

        return url
    
    # Function to create a function payload with values by adding given values and keys to a dictionary
    def create_function_payload(self, keys, values):
        print("Creating the function payload....")

        # Create the payload dictionary
        payload = {}

        # Add the keys and values to the payload
        for i in range(len(keys)):
            payload[keys[i]] = values[i]

        return payload

    # Function to execute a command from the Redis cache, given the message command and the command data
    def execute_command(self, message, commandData, commandURL):
        print("Executing the command....")

        # Get the payload keys from the command data
        keys = self.get_payload_keys(commandData)

        if keys is None:
            msg = "The command does not exist. Ensure that you typed it correctly."
            print(msg)
            return msg

        # Get the command parameters from the message
        params = self.get_command_params(message)

        # Get the payload values from the message
        values = self.get_payload_values(message)

        print(f"Keys: {keys}")
        print(f"Values: {values}")

        # Check if the number of keys and values match
        if len(keys) != len(values):

            msg = "The number of keys and values do not match."

            print(msg)
            return msg

        # Create the function URL
        url = self.create_function_url(commandURL, params)

        # Create the function payload
        payload = self.create_function_payload(keys, values)

        print(f"URL: {url}")
        print(f"Payload: {payload}")

        # Execute the function, depending on the method
        if commandData['method'] == "GET":
            print("Executing GET Method")
            resp = requests.get(url=url, json=payload)
        elif commandData['method'] == "POST":
            print("Executing POST Method")
            resp = requests.post(url=url, json=payload)
        elif commandData['method'] == "PUT":
            print("Executing PUT Method")
            resp = requests.put(url=url, json=payload)
        elif commandData['method'] == "DELETE":
            print("Executing DELETE Method")
            resp = requests.delete(url=url, json=payload)

        if resp.ok:
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
            msg = "An error has occurred while trying to execute the command."
            print(msg)
            return msg

    # Function to send a bot message
    def send_bot_message(self, gateway, command):
        print("Sending Bot Message....")

        payload = {
            "text": f"{command}",
            "username": "Waddle Bot",
            "gateway": gateway
        }

        resp = requests.post(url=self.matterbridgePostURL, json=payload)

        if resp.ok:
            print("BOT Message Successfully Sent!")

    # Function to add an identity (User) to the database
    def add_identity(self, username):
        print("Adding Identity....")

        payload = {
            "name": username,
            "country": "Unknown",
            "ip_address": "Unknown",
            "browser_fingerprints": []
        }

        resp = requests.post(url=self.userManagerURL, json=payload)

        if resp.ok:
            print('response:', resp.json())
            print("Identity Successfully Added!") 
        

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

        # keys = self.redisManager.get_all_keys()
        commands = self.redisManager.get_all_commands()

        # Print the commands
        # print("The commands are:")
        # print(commands)

        helpMessage = "Available Commands:\n"

        # Loop through the commands and display the command and its description.
        for command in commands:
            helpMessage += f"{command}\n"


        return helpMessage
    
    # Function to retrieve the metadata json object from a given marketplace module URL
    def get_marketplace_metadata(self, marketplaceModuleURL):
        print("Getting Marketplace Metadata....")

        callURL = self.marketplaceURL + 'url?url=' + quote_plus(marketplaceModuleURL, safe='', encoding='utf-8')

        print(f"Call URL: {callURL}")

        resp = requests.get(url=callURL)

        if resp.ok:
            response = resp.json()

            if 'metadata' in response:
                metadata = response['metadata']
                print("The metadata is:")
                print(metadata)

                return metadata

            else:
                return None
        else:
            return None
        
    # A function that accepts a string list, loops through each string and checks if they are present within one another in a given metadata object, and returns the command properties
    def get_command_properties(self, commandlist, metadata):
        print("Getting Command Properties....")

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
                
            
        

    

