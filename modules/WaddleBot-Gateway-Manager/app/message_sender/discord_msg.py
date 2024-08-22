import requests
import logging

class Discord_Message_Sender:
    def __init__(self, token: str, user_id: str, message: str) -> None:
        self.token = token
        self.user_id = user_id
        self.message = message
        self.channel_id = self.create_dm_channel()

    def send_message(self) -> None:
        try:
            url = 'https://discord.com/api/v8/channels/{}/messages'.format(self.channel_id)
            data = {"content": self.message}
            header = {"authorization": self.token}
            r = requests.post(url, data=data, headers=header)
            logging.info(r.status_code)
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def create_dm_channel(self) -> str:
        try:
            data = {"recipient_id": self.user_id}
            headers = {"authorization": self.token}
            r = requests.post(f'https://discord.com/api/v9/users/@me/channels', json=data, headers=headers)
            logging.info(r.status_code)
            channel_id = r.json()['id']
            return channel_id
        except Exception as e:
            logging.error(f"Error creating DM channel: {e}")
    


# def sendMessage(token, channel_id, message):
#     url = 'https://discord.com/api/v8/channels/{}/messages'.format(channel_id)
#     data = {"content": message}
#     header = {"authorization": token}
 
#     r = requests.post(url, data=data, headers=header)
#     print(r.status_code)
 
 
# def createDmChannel(token, user_id):
#     data = {"recipient_id": user_id}
#     headers = {"authorization": token}
 
#     r = requests.post(f'https://discord.com/api/v9/users/@me/channels', json=data, headers=headers)
#     print(r.status_code)
 
#     channel_id = r.json()['id']
 
#     return channel_id
 
 
# #Change these variables
# token = ''
# user_id = ''
# message = ''
 
# channel_id = createDmChannel(token, user_id)
# sendMessage(token, channel_id, message)