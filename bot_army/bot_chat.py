import string
import pymysql
import datetime, time
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom
# from time import gmtime, strftime, asctime
from time import *

s = openSocket()
joinRoom(s)
readbuffer = ""

#connect to the database
connection = pymysql.connect(host="96.126.111.207", port=3306, user="root",
    passwd="TwitchPlaysRobotics", db="TwitchPlays")
cursor = connection.cursor()

message_id = 0

while True:
    
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        
        if line == "PING :tmi.twitch.tv\r":
            sendMessage(s, "PONG :tmi.twitch.tv".encode("utf-8"))
            continue
        # print("line: ", line )
        user = getUser(line)
        message = getMessage(line)

        print user + " typed :" + message
        sendMessage(s, "Thank you for your message!")

        currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print currentTime

        
        #INSERT INTO chats VALUES (ID, time, user, txt);
        sql = "INSERT INTO chats(timeA, username, txt) VALUES('%s', '%s', '%s');"%(currentTime, user, message)
        try:
            cursor.execute(sql)
            connection.commit()
        except:
            print("unable to insert data")
            connection.rollback()
			    
connection.close()			
