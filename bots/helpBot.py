###USE TPR_BOT3 FOR SENDING MESSAGES
# This bot picks an unprocessed help message from database and sends a response.

import string
import pymysql
from database import DATABASE
from twitch import Twitch
import time
from settings import *

t  = Twitch()
db = DATABASE()

username = IDENT #Your twitch username. ALL LOWER CASE
key      = PASS #Key acquired from twitch.tv account page
channel  = CHANNEL
port     = PORT
host     = HOST

t.connect(username, key, channel, host, port)

# to send a pong message to twitch server every 5 minutes otherwise the connection
# is closed. This is a good option when a bot is not actively listening to a channel.
t.pong()

#General help message
gen = """This is Twitch Plays Robotics, a..\
        "?project" for more info on the project\
       "?robots" for more info on the robots\
       "?commands" for more info on the commands\
       "?votes" for more info on reinforcements\
       "?rewards" for more info on the simulation\
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
rewards = """Reinforcements help the robot learn. Saying "yes" to the robot\
        is rewarding it, e.g. giving a dog a treat.  Saying "no" ... """

#Simulation help message
sim = """The simulation is created in a physics engine called Open Dynamics\
        Engine (ODE.) The robots inside of it are made through a python wrapper\
        called PyRoSim (Python Robotics Simulator.)"""

scores = """To collect points, give reinforcement to robots or vote for commands.\
         To see your points type in ?myscore"""

votes = """You can vote for a command by typing !command. Don't forget the exclamation mark!"""

first_time = 'Congratulations! You just earned your first point.'

#Organize messages by type
help_type = {'general'   : gen, 'project'   : proj,
             'robots'     : bot, 'commands'   : cmd,
             'rewards' : rewards, 'simulator' : sim,
             'scores'    : scores, 'votes': votes}

# sleep to avoid getting blocked from twitch. There is a limit on the number of messages 
# a bot can send to channel. 
SLEEP_RATE = 20/30

while True:

    # to send a pong message to twitch server otherwise the connection is closed.
    # receive_message(..) in twitch class is a blocking function and not suitable 
    # for help bot.
    # msg_from_twitch = t.recieve_messages(amount = 1024)

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
            sent = t.send_message("@"+ username + ", your score:"+ str(result['score']))
            print('sent score info', sent)

        elif (msg == 'first_time_contribution'):
            sent = t.send_message('@' + username + ' ' + first_time)
            print('first time contribution: ', sent)

        elif msg_to_send in help_type:
            sent = t.send_message('@' + username + ' ' + help_type.get(msg_to_send))
            print('sent filtered', sent)

        else:
            sent = t.send_message('@' + username + ' ' + help_type.get('general'))
            print('sent general', sent)

        time.sleep(SLEEP_RATE)


    
			
