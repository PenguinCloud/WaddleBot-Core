from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.eventsub.webhook import EventSubWebhook
from twitchAPI.object.eventsub import ChannelFollowEvent, ChannelSubscribeEvent, ChannelSubscriptionGiftEvent
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand, ClearChatEvent, NoticeEvent, RoomStateChangeEvent
import asyncio
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# async def twitch_example():
#     client_id = os.getenv('TWITCH_CLIENT_ID')
#     client_secret = os.getenv('TWITCH_CLIENT_SECRET')
#     # initialize the twitch instance, this will by default also create a app authentication for you
#     twitch = await Twitch(app_id=client_id, app_secret=client_secret)
#     # call the API for the data of your twitch user
#     # this returns a async generator that can be used to iterate over all results
#     # but we are just interested in the first result
#     # using the first helper makes this easy.
#     user = await first(twitch.get_users(logins='mjshepherd95'))
#     # print the ID of your user or do whatever else you want with it
#     print(user.id)

# # run this example
# asyncio.run(twitch_example())

activities = [
    {"name": "bits", "amount": 20},
    {"name": "follow", "amount": 10},
    {"name": "sub", "amount": 50},
    {"name": "raid", "amount": 30},
    {"name": "ban", "amount": -10},
    {"name": "subgift", "amount": 60},
]

# Setup the twitch api listener as a class
class TwitchAPIListener:
    def __init__(self, app_id, app_secret, user_scope, target_channels, context_url, eventsub_url, target_user):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user_scope = user_scope
        self.context_url = context_url
        self.eventsub_url = eventsub_url
        self.target_user = target_user

        self.target_channels = target_channels


# APP_ID = os.getenv('TWITCH_APP_ID')
# APP_SECRET = os.getenv('TWITCH_APP_SECRET')
# USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_READ_FOLLOWERS]
# TARGET_CHANNELS = []

# # Endpoint URL's for Waddlebot's DB
# GATEWAYS_GET_URL = os.getenv('GATEWAYS_GET_URL')
# CONTEXT_URL = os.getenv('CONTEXT_URL')

    

    # This functiom will get/initialize the context for a given user through the context API
    def get_context(self, username):
        print(f'Getting context for {username}')

        # The request payload.
        payload = {
            "identity_name": username
        }

        # Make the request to the context API
        response = requests.post(self.context_url, json=payload)

        if response.ok:
            data = None
            if response.json() and 'data' in response.json():
                data = response.json()['data']
            return data
        else:
            return None
        
    # This function will process an activity and send a request to the reputation module depending on the activity
    def process_activity(self, activity, username):
        print(f'Processing activity for {username}')

        # Get the context for the user
        context = self.get_context(username)

        if context:
            # The request payload.
            payload = {
                "userid": context['identity_id'],
                "activity": activity['name'],
                "amount": activity['amount'],
                "text": f"{activity['name']} activity for {username}",
                "namespace": context['namespace_name'],
                "namespaceid": context['namespace_id'],
                "platform": "Twitch"
            }

            print(f'Activity processed for {username}')
            print(f'Payload: {payload}')

            # TODO: When the reputation API is ready, uncomment the code below
            # # Make the request to the reputation API
            # response = requests.post(self.context_url, json=payload)

            # if response.ok:
            #     print(f'Activity processed for {username}')
            # else:
            #     print(f'Failed to process activity for {username}')
        else:
            print(f'Failed to get context for {username}')
    


    # this will be called when the event READY is triggered, which will be on bot start
    async def on_ready(self, ready_event: EventData):
        print('Bot is ready for work, joining channels')
        print("The target channels are: ", self.target_channels)
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await ready_event.chat.join_room(self.target_channels)
        # you can do other bot initialization things in here


    # this will be called whenever a message in a channel was send by either the bot OR another user
    async def on_message(self, msg: ChatMessage):
        print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')
        # print(f"The amount of bits is: {msg.bits}")

        # If the message's bits is greater than 0, process the bits activity
        if msg.bits > 0:
            self.process_activity(activities[0], msg.user.name)


    # this will be called whenever someone subscribes to a channel
    async def on_sub(self, sub: ChatSub):
        print(f'New subscription in {sub.room.name}:\n'
            f'  Type: {sub.sub_plan}\n'
            f'  Message: {sub.sub_message}')
        print(f"The sub data is: {sub}")
        
        # Process the sub activity
        # self.process_activity(activities[2], sub.user.name)

    # This will be called when a raid is triggered
    async def on_raid(self, raid: EventData):
        # print(f'Raid Data')
        # print(f'{raid}')

        if 'tags' in raid:
            # print(f'Tags')
            # print(f'{raid["tags"]}')

            # Get the display name of the user who initiated the raid
            display_name = raid['tags']['display-name']

            print(f'Display Name of the raider: {display_name}')

            # Process the raid activity
            self.process_activity(activities[3], display_name)

    # This will be called when a ban is triggered
    async def on_ban(self, ban: ClearChatEvent):
        print(f"The user {ban.user_name} has timed out or banned")

        # Process the ban activity
        self.process_activity(activities[4], ban.user_name)

    # this will be called whenever someone follows a channel
    async def on_follow(self, data: ChannelFollowEvent):
        # our event happend, lets do things with the data we got!
        print(f'{data.event.user_name} now follows {data.event.broadcaster_user_name}!')

        userName = data.event.user_name

        # Process the follow activity
        self.process_activity(activities[1], userName)

    # this will be called whenever someone subscribes to a channel
    async def on_sub(self, data: ChannelSubscribeEvent):
        # our event happend, lets do things with the data we got!
        print(f'{data.event.user_name} just subscribed to {data.event.broadcaster_user_name}!')

        userName = data.event.user_name

        # Process the sub activity
        self.process_activity(activities[2], userName)

    # this will be called whenever someone gifts a subscription to a channel
    async def on_subgift(self, data: ChannelSubscriptionGiftEvent):
        # our event happend, lets do things with the data we got!
        print(f'{data.event.user_name} just gifted a subscription to {data.event.broadcaster_user_name}!')

        userName = data.event.user_name

        # Process the subgift activity
        self.process_activity(activities[5], userName)

    # this will be called whenever the !reply command is issued
    async def test_command(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply('you did not tell me what to reply with')
        else:
            await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')

    # this will be called when a notice event is triggered
    async def on_notice(self, notice: NoticeEvent):
        print(f'Notice event: {notice}')

    # thsi will be called when a room state change event is triggered
    async def on_room_state_change(self, room_state: RoomStateChangeEvent):
        print(f'Room state change: {room_state}')

    # this is where we set up the bot
    async def run(self):
        print(f'Target channels: {self.target_channels}')

        # set up twitch api instance and add user authentication with some scopes
        try:
            twitch = await Twitch(self.app_id, self.app_secret)
            # user = await first(twitch.get_users(logins=self.target_user))
            
            auth = UserAuthenticator(twitch, self.user_scope)

            token, refresh_token = await auth.authenticate()

            await twitch.set_user_authentication(token, self.user_scope, refresh_token)
        except Exception as e:
            print(f"An error ocurred setting up the Twitch API: {e}")

        # create chat instance
        try:
            chat = await Chat(twitch)

            # register the handlers for the events you want

            # listen to when the bot is done starting up and ready to join channels
            chat.register_event(ChatEvent.READY, self.on_ready)
            # listen to chat messages
            chat.register_event(ChatEvent.MESSAGE, self.on_message)
            # listen to channel subscriptions
            chat.register_event(ChatEvent.SUB, self.on_sub)
            # Listen to raids
            chat.register_event(ChatEvent.RAID, self.on_raid)
            # Listen to bans
            chat.register_event(ChatEvent.CHAT_CLEARED, self.on_ban)
            # Listen for notices
            chat.register_event(ChatEvent.NOTICE, self.on_notice)
            # Listen for room state changes
            chat.register_event(ChatEvent.ROOM_STATE_CHANGE, self.on_room_state_change)

            # you can directly register commands and their handlers, this will register the !reply command
            chat.register_command('reply', self.test_command)


            # we are done with our setup, lets start this bot up!
            chat.start()
        except Exception as e:
            print(f"An error ocurred setting up the chat bot: {e}")

        # # register the eventsub webhook
        # # basic setup, will run on port 8080 and a reverse proxy takes care of the https and certificate
        try:
            eventsub = EventSubWebhook(self.eventsub_url, 8080, twitch)

            # unsubscribe from all old events that might still be there
            # this will ensure we have a clean slate
            await eventsub.unsubscribe_all()
            # start the eventsub client
            eventsub.start()

            # Get the usernames from the list of gateways
            user_list = self.get_usernames(self.target_channels)

            # Subscribe to events for the list of users
            await self.subscribe_to_events(eventsub, twitch, user_list)
        except Exception as e:
            print(f"An error ocurred setting up the webhook events: {e}")

        # lets run till we press enter in the console
        try:
            input('press ENTER to stop\n')
        finally:
            # now we can close the chat bot and the twitch api client
            # stopping both eventsub as well as gracefully closing the connection to the API
            await eventsub.stop()

            chat.stop()
            await twitch.close()

    # A function to return a list of usernames from a list of users retrieved from the Waddlebot's DB
    def get_usernames(self, users):
        user_list = []
        if len(users) > 0:
            for user in users:
                # Check if the first character of the string is a "#" symbol
                if user[0] == "#":
                    # Remove the "#" symbol from the string
                    user = user[1:]
                user_list.append(user)
        
        return user_list

    # A function to return a list of user objects from a list of user names
    async def get_user_objects(self, twitch, user_list):
        users = []
        if len(user_list) > 0:
            for user in user_list:
                user = await first(twitch.get_users(logins=user))
                users.append(user)
        
        return users

    # Function to subscribe to events for a list of users
    async def subscribe_to_events(self, eventsub, twitch, user_list):

        print("Getting user data")
        # users = []
        # users.append(await first(twitch.get_users(logins=user)))
        # From the list of users, get all the twitch user objects and store them in a list
        # users = await get_user_objects(twitch, USER_LIST)
        users = await self.get_user_objects(twitch, user_list)

        # print(f'subscribing to follow events for user {user.id}')
        # From the list of users, subscribe to the follow event for each user
        for user in users:
            print(f'subscribing to follow events for user {user.id}')
            await eventsub.listen_channel_follow_v2(user.id, user.id, self.on_follow)
        
        # From the list of users, subscribe to the sub event for each user
        for user in users:
            print(f'subscribing to sub events for user {user.id}')
            await eventsub.listen_channel_subscribe(user.id, self.on_sub)

        # From the list of users, subscribe to the subgift event for each user
        for user in users:
            print(f'subscribing to subgift events for user {user.id}')
            await eventsub.listen_channel_subscription_gift(user.id, self.on_subgift)

        print("Listening to events")

    

TARGET_SCOPES = [AuthScope.MODERATOR_READ_FOLLOWERS, AuthScope.USER_READ_FOLLOWS, AuthScope.USER_EDIT_FOLLOWS, AuthScope.MODERATOR_MANAGE_AUTOMOD]

# The main function to run the bot
def main():
    # Get the gateways from the Waddlebot's DB
    gateways = get_gateways(os.getenv('GATEWAYS_GET_URL'))

    # Create an instance of the TwitchAPIListener
    listener = TwitchAPIListener(
        os.getenv('TWITCH_APP_ID'),
        os.getenv('TWITCH_APP_SECRET'),
        TARGET_SCOPES,
        gateways,
        os.getenv('CONTEXT_URL'),
        os.getenv('EVENTSUB_URL'),
        os.getenv('TARGET_USERNAME')
    )

    # Run the bot
    asyncio.run(listener.run())

# This function will retrieve all the gateways stored in the Waddlebot's DB
def get_gateways(url):
    print('Getting gateways')

    channels = []

    # Make the request to the gateways API
    response = requests.get(url)

    if response.ok:
        data = None

        if response.json() and 'data' in response.json():
            data = response.json()['data']

            if len(data) > 0:
                for gateway in data:
                    if 'gateway_type' in gateway and gateway['gateway_type'] == 'Twitch' and 'channel_id' in gateway and 'is_active' in gateway and gateway['is_active'] == True:
                        channel_id = gateway['channel_id']

                        if channel_id not in channels:
                            channels.append(gateway['channel_id'])
            
    return channels


if __name__ == '__main__':
    main()
