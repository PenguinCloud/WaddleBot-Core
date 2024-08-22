# Config portion
import socket
import logging
# import pyttsx3
# import soundfx


# HOST = "irc.chat.twitch.tv"  # the twitch irc server
# PORT = 6667  # always use port 6667
# NICK = "fuzzybottgaming"  # twitch username, lowercase
# PASS = "oauth:[]"  # your twitch OAuth token
# CHAN = "#[my channel]"  # the channel you want to join

class Twitch_Message_Sender:
    def __init__(self, HOST: str, PORT: int, NICK: str, PASS: str, CHAN: str) -> None:
        self.HOST = HOST
        self.PORT = PORT
        self.NICK = NICK
        self.PASS = PASS
        self.CHAN = CHAN

    def send_message(self, message: str) -> None:
        s = socket.socket()
        logging.info("Connecting to twitch")
        logging.info(f"HOST: {self.HOST}")
        logging.info(f"PORT: {self.PORT}")

        try:
            s.connect((self.HOST, self.PORT))
            logging.info("Connected to twitch")

            s.send(f"PASS {self.PASS}\r\n".encode("utf-8"))
            logging.info("Sent pass")

            s.send(f"NICK {self.NICK}\r\n".encode("utf-8"))
            logging.info("Sent nick")

            s.send(f"JOIN {self.CHAN}\r\n".encode("utf-8"))
            logging.info("Sent join")

            s.send(f"PRIVMSG {self.CHAN} :{message}\r\n".encode("utf-8"))
            logging.info("Sent message")

            s.send(f"PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            logging.info("Sent pong")

            s.close()
            logging.info(f"Message sent to Twitch. Message: {message}")
        except Exception as e:
            logging.error(f"Error sending message: {e}")

        # If an error occurs, return a 500 error
        # if not s:
        #     logging.info("Error sending message")
