import twitch
from settings import *
import database
from time import *

t = twitch.Twitch()
mydatabase = database.DATABASE()


#Enter your twitch username and oauth-key below, and the app connects to twitch with the details.
#Your oauth-key can be generated at 
username = IDENT #Your twitch username. ALL LOWER CASE
key = PASS #Key acquired from twitch.tv account page
channel = CHANNEL
port = PORT
host = HOST

t.connect(username, key, channel, host, port)
 
#The main loop
while True:

    newMessages = t.recieve_messages(amount = 1024)
    # print("mess: ", newMessages)

    if newMessages:

        for message in newMessages:

            #Try block, some characters are not understood by python and can cause exceptions
            try:
                #Get info from message.
                msg = str(message['message'].lower().replace("'", ''))
                username = str(message['username'].lower())
                # t.send_message("Thank you for your message!")

                print(username + ": " + msg)
                currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())

                if(username not in filteredUsers):
                    mydatabase.Add_To_Chat_Table(username, currentTime, msg)

            except:
                print("msg error")
                #end if not in filtered users
        #end for each message in new messages
    #end if new messages

