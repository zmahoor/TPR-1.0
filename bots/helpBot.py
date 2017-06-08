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
gen = """This is Twitch Plays Robotics, a..\
        "?project" for more info on the project\
       "?robot" for more info on the robots\
       "?command" for more info on the commands\
       "?reinforce" for more info on reinforcements\
       "?sim" for more info on the simulation\
       "?myscore" to see your own score\
       "?scores" for information on the scoring system."""

#Project help message
proj = 'Twitch Plays Robotics is a ...'

#Robot help message
bot = 'These robots are created every 30 seconds, and...'

#Commands help message
cmd = """Commands are typed in the chat, and the one asked for the most over\
        every 3 miutes will become the command the robot will try.\
        Ever try asking a dog to learn a new trick? Think of it like that!"""

#Reinforcements help message
reinforce = """Reinforcements help the robot learn. Saying "yes" to the robot\
        is rewarding it, e.g. giving a dog a treat.  Saying "no" ... """

#Simulation help message
sim = """The simulation is created in a physics engine called Open Dynamics\
        Engine (ODE.) The robots inside of it are made through a python wrapper\
        called PyRoSim (Python Robotics Simulator.)"""

scores = """To collect points, give reinforcement to robots or vote for commands.\
         To see your points type in ?myscore"""

first_time = 'Congratulations! You just earned your first point.'

#Organize messages by type
help_type = {'general'   : gen, 'project'   : proj,
             'robot'     : bot, 'command'   : cmd,
             'reinforce' : reinforce, 'simulator' : sim,
             'scores'    : scores}

# sleep to avoid getting blocked from twitch. There is a limit on the number of messages 
# a bot can send to channel. 
SLEEP_RATE = 20/30

while True:

    # to send a pong message to twitch server otherwise the connection is closed.
    # msg_from_twitch = t.recieve_messages(amount = 1024)

    # print "msg from twitch:", msg_from_twitch

    # get the oldest unprocessed request for help with flag=0.
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
            sent = t.send_message("@"+ username + ", score:"+
                str(result['score'])+" invited by: "+ str(result['parentName']))

        elif (msg == 'first_time_contribution'):
            t.send_message('@' + username + ' ' + first_time)

        elif msg_to_send in help_type:
            print('sent filtered')
            t.send_message('@' + username + ' ' + help_type.get(msg_to_send))

        else:
            print('sent general')
            t.send_message('@' + username + ' ' + help_type.get('general'))

        time.sleep(SLEEP_RATE)


    
			
