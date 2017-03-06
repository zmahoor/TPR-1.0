import time;
import re;
import socket; #imports module allowing connection to IRC
import threading; #imports module allowing timing functions
# import msvcrt #imports module necessary for key reading

#sets variables for connection to twitch chat
bot_owner = 'Slayton';
nick = 'tpr_bot';
channel = '#mungozero';
server = 'irc.twitch.tv';
port = 6667;
password = 'oauth:kzutoi7q39ib3p19waq5f9nq8kerd8';
RATE = (20./30.);
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :");

irc = socket.socket();
irc.connect((server, port));

#sends variables for connection to twitch chat
irc.send("PASS {}\r\n".format(password).encode("utf-8"));
irc.send("NICK {}\r\n".format(nick).encode("utf-8"));
irc.send("JOIN {}\r\n".format(channel).encode("utf-8"));

def Chat_From_User(msg):
	return ( msg[0] != ':' );

def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    print("Chat attempted")
    message = msg.rstrip();
    sock.send("PRIVMSG %s :" % channel + message + "\r\n" );
    # , msg
def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user));

def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs));

def main():
    userLog = {};
    chatLog = [];
    
    print("Welcome welcome, chat bot ready to go")
    
    while True:
        response = irc.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            irc.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0) # return the entire match
            message = CHAT_MSG.sub("", response);
            
            if ( Chat_From_User(message) ):
                # Logs Calls for Scoreboard
                print(message)
                chatLog.append(message);

                # Checks for Commands
                if(message[0] == ("_")):
                    # Score Command
                    if (message.rstrip()[1:] == ("score")):
                            chat(irc, printUserLog(userLog));
                    else:
                        reply = message[1:].rstrip() + " is not a command";
                        print(reply)
                        chat(irc, reply);
                
                # Logs Normal Chat Messages
                else:
                    print(username + ': ' + message);
                    if(userLog.has_key(username)):
                        userLog[username] += 1;
                    else:
                        print("New User Recognized: " + username);
                        userLog[username] = 1;
            time.sleep( 1.0 / RATE );

def printUserLog(log):
    string = "Score Board:";
    for key in log:
        string += key + ':' + str(log[key]) + " ";
    return string;
    
    

main();

