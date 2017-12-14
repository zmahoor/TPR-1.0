"""
this script listens to a twitch channel and records any incoming message to the chat table.
"""
from settings import *
from time import *
from database import DATABASE
from twitch import Twitch

t = Twitch()
db = DATABASE()

username = IDENT  # Your twitch username. ALL LOWER CASE
key = PASS        # Key acquired from twitch.tv account page
channel = CHANNEL
port = PORT
host = HOST
t.connect(username, key, channel, host, port)
 
# The main loop
while True:
    newMessages = t.recieve_messages(amount=1024)
    # print("mess: ", newMessages)
    if newMessages:
        for message in newMessages:
            # Try block, some characters are not understood by python and can cause exceptions
            try:
                # Get info from message.
                msg = str(message['message'].lower().replace("'", ''))
                username = str(message['username'].lower())
                # t.send_message("Thank you for your message!")
                currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
                print(currentTime, username + ": " + msg)

                if username not in filteredUsers:
                    print('Adding to the chat table...')
                    db.add_to_chat_table(username, currentTime, msg)

            except Exception as e:
                print str(e)
                print("something went wrong. Unable inserting this message.")
                # end if not in filtered users
        # end for each message in new messages
    # end if new messages

