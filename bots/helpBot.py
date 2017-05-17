###USE TPR_BOT3 FOR SENDING MESSAGES

import string
import pymysql
from database import DATABASE
from twitch import Twitch
import time
from settings import *

t = Twitch()
db = DATABASE()

username = IDENT #Your twitch username. ALL LOWER CASE
key = PASS #Key acquired from twitch.tv account page
channel = CHANNEL
port = PORT
host = HOST

t.connect(username, key, channel, host, port)

#General help message
gen = 'This is Twitch Plays Robotics, a...\n\
       "?project" for more info on the project\n\
       "?robot" for more info on the robots\n\
       "?command" for more info on the commands\n\
       "?reinf" for more info on reinforcements\n\
       "?sim" for more info on the simulation\n\
       "?myscore" for information on your score.'

#Project help message
proj = 'Twitch Plays Robotics is a ...'

#Robot help message
bot = 'These robots are created every x minutes, and...'

#Commands help message
cmd = 'Commands are typed in the chat, and the one asked for the most\
        over every x seconds will become the command the robot will try. \
        Ever try asking a dog to learn a new trick? Think of it like that!'

#Reinforcements help message
reinf = 'Reinforcements help the robot learn. Saying "yes" to the robot\
        is rewarding it, e.g. giving a dog a treat.  Saying "no" ... '

#Simulation help message
sim = 'The simulation is created in a physics engine called Open Dynamics \
        Engine (ODE.) The robots inside of it are made through a python wrapper\
        called PyRoSim (Python Robotics Simulator.)'

#Organize messages by type
help_type = {'general' : gen, 'project' : proj,
             'robot' : bot, 'command' : cmd,
             'reinf' : reinf, 'sim' : sim}

while True:
    time.sleep(2)
    #QUERY DATABASE FOR RECORDS IN 'HELP' W/ FLAG 0
    #GRAB OLDEST
    records = db.Fetch_Oldest_Help()
    if records == None:
        continue
    else:
        msg = records['txt']
        username = records['userName']
        print msg, username
        msg_to_send = msg[1:].rstrip()

        if (msg == '?myscore'):
            result = db.Fetch_User_Score(username)
            t.send_message("@"+ username + ", score:"+
                str(result['score'])+" invited by: "+ str(result['parentName']))

        elif msg_to_send in help_type:
            print('sent filtered')
            t.send_message('@' + username + ' ' + help_type.get(msg_to_send))
        else:
            print('sent general')
            t.send_message('@' + username + ' ' + help_type.get('general'))
    

    
			
