"""
twitch class
"""
# Code used and modified with permission from author from http://pastebin.com/MDC0RZDp.
# Original author: Frederik Witte http://www.wituz.com/
# Code acquired on 9/02/2015

import socket
import sys
import re
import string
import threading
import datetime

class Twitch:

    def __init(self, sock=None):
        self.user = ""
        self.oauth = ""
        self.channel = ""
        self.port = ""
        self.host = ""
        self.channel = ""

        self.sock = None

    def connect(self, user, key, channel, host, port):
        """
        connect to a twitch channel
        :param user: string
        :param key: string
        :param channel: string
        :param host: string
        :param port: int
        :return:
        """
        self.user = user
        self.oauth = key

        print("Connecting to twitch.tv")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # to have a non-blocking soucket add this line. not tested yet.
        # self.sock.settimeout(0.6)
        self.host = host
        self.port = port
        self.channel = channel

        try:
            self.sock.connect((self.host, self.port))
        except:
            print("Failed to connect to twitch")
            sys.exit()

        print("Connected to twitch")
        print("Sending our details to twitch...")

        self.sock.send("PASS " + key + "\r\n")
        self.sock.send("NICK " + user + "\r\n")
        self.sock.send("JOIN #" + channel + "\r\n")
        
        self.join_room()

    def join_room(self):
        """
        joins a channel
        :return: none
        """
        readbuffer = ""
        loading = True

        while loading:
            readbuffer = readbuffer + self.sock.recv(1024)
            temp = string.split(readbuffer, "\n")
            readbuffer = temp.pop()
            
            for line in temp:
                print(line)

                if self.login_status(line):
                    print("Login authentication failed")
                    sys.exit()

                loading = self.loading_complete(line) 

        print('Joined %s channel..' %(self.channel))
        self.send_message("Joined chat...")

    def loading_complete(self, line):
        """
        return true if the loading is done
        :param line: string
        :return: bool
        """
        if("End of /NAMES list" in line):
            return False
        else:
            return True
    
    def login_status(self, line):
        if ("Login authentication failed" in line):
            return True
        else:
            return False

    def send_message(self, message):
        """
        sends a message to the connected twitch channel
        :param message: string
        :return: none
        """
        messageTemp = "PRIVMSG #" + self.channel + " :" + message.rstrip()
        # print messageTemp
        try:
            sent = self.sock.send(messageTemp + "\r\n")
            print("Sent: %s" %(messageTemp))
        except:
            print("Lost connection to Twitch, attempting to reconnect...")
            self.connect(self.user, self.oauth, self.channel, self.host, self.port)
            sent = None
        return sent

    def pong(self):
        """
        create a thread to send a pong message to the twitch server every 5 minutes.
        """
        try:
            self.sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "PONG SENT!")

        except KeyboardInterrupt:
            sys.exit()

        except:
            print('Unable to send pong message..')
            self.connect(self.user, self.oauth, self.channel, self.host, self.port)

        t = threading.Timer(300, self.pong)
        t.daemon = True
        t.start()

    def is_ping_message(self, data):
        """
        if the incoming message is ping, then send a pong back to the twitch server.
        :param data:
        :return: bool
        """
        if "PING :tmi.twitch.tv\r" in data:
            print('recieved ping...', ' sending pong...')
            self.sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            return True
        else: 
            return False

    def recieve_messages(self, amount=512):
        """
        receives a message of a given size from a twitch channel
        :param amount: int
        :return: list[string]
        """
        # data = None
        data = self.sock.recv(amount)

        if self.is_ping_message(data):
            return None
        # try:
        #     data = self.sock.recv(amount)
        # except: 
        #     return False

        # if not data:
        #     print("Lost connection to Twitch, attempting to reconnect...")
        #     self.connect(self.user, self.oauth, self.channel, self.host, self.port)
        #     return None
        #self.ping(data)

        if self.check_has_message(data):
            return [self.parse_message(line) for line in filter(None, data.split('\r\n'))] 

    def check_has_message(self, data):
        return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv) PRIVMSG #[a-zA-Z0-9_]+ :.+$',
                        data)

    def parse_message(self, data):
        return {
            'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0],
            'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', data)[0],
            'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0].decode('utf8')
        }

