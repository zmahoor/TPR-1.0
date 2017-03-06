import string
import pymysql
import datetime, time

#connect to the database
conn = pymysql.connect(host="96.126.111.207",port=3306,user="root",passwd="TwitchPlaysRobotics",db="TwitchPlays")
cur = conn.cursor()

message_type = 0

#IF NEW RECORD
if (False):
    #FILTER WHAT MESSAGE TYPE
    #0 -- raw chat
    #1 -- command
    #2 -- reinforcement
    #3 -- help

    #message = pull new message from 'chats' table
    
    
    if (message[0] == '?'):
        message_type = 3
        #send message to helpbot to chat to user
        elif (message[0] == '!'):
               
            #Either command (1)
            #then move to commands table
            message_type = 1
            #Or reinforcement (2)
            #then move to reinforcements table
            message_type = 2
        else:
            #if does not start with ? or !, it is raw chat
            message_type = 0
            #keep in chats table???

    #user = pull user field from new row
    if (user not in users):
        #add user, assign new ID
        #keep record of when their first message was sent???
        
        
