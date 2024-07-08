# Config portion
import socket
# import pyttsx3
# import soundfx


# HOST = "irc.chat.twitch.tv"  # the twitch irc server
# PORT = 6667  # always use port 6667
# NICK = "fuzzybottgaming"  # twitch username, lowercase
# PASS = "oauth:[]"  # your twitch OAuth token
# CHAN = "#[my channel]"  # the channel you want to join

class Twitch_Message_Sender:
    def __init__(self, HOST, PORT, NICK, PASS, CHAN):
        self.HOST = HOST
        self.PORT = PORT
        self.NICK = NICK
        self.PASS = PASS
        self.CHAN = CHAN

    def send_message(self, message):
        s = socket.socket()
        print("Connecting to twitch")
        print(f"HOST: {self.HOST}")
        print(f"PORT: {self.PORT}")
        s.connect((self.HOST, self.PORT))
        print("Connected to twitch")
        s.send(f"PASS {self.PASS}\r\n".encode("utf-8"))
        print("Sent pass")
        s.send(f"NICK {self.NICK}\r\n".encode("utf-8"))
        print("Sent nick")
        s.send(f"JOIN {self.CHAN}\r\n".encode("utf-8"))
        print("Sent join")
        s.send(f"PRIVMSG {self.CHAN} :{message}\r\n".encode("utf-8"))
        print("Sent message")
        s.send(f"PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("Sent pong")
        s.close()
        print(f"Message sent to Twitch. Message: {message}")

        # If an error occurs, return a 500 error
        # if not s:
        #     print("Error sending message")
