"""
This script picks an unprocessed help message from the database and sends a response to the user in the chat session
"""

import string
import pymysql
from database import DATABASE
from twitch import Twitch
import time
from settings import *
import datetime

t = Twitch()
db = DATABASE()

username = IDENT  # Your twitch username. ALL LOWER CASE
key = PASS        # Key acquired from twitch.tv account page
channel = CHANNEL
port = PORT
host = HOST

# sleep to avoid getting blocked from twitch. There is a limit on the number of messages
# a bot can send to channel.
SLEEP_RATE = 20/30

t.connect(username, key, channel, host, port)

# to send a pong message to twitch server every 5 minutes otherwise the connection
# is closed. This is a good option when a bot is not actively listening to a channel.
t.pong()

# General help message
gen = """Twitch Plays Robotics is a community-driven project to teach robots language.\
 To learn more about any aspect of the project, type ?robots, ?silverRobots ?reinforcement,\
  ?votes, ?scores, ?myscore, or ?commandScores. More details at https://tpr-uvm.github.io."""

# Robot help message
bot = """Every 30 seconds one robot, out a population of 50, is simulated.\
 It "hears" the current command and senses its environment.\
  There are 10 species of bots: have you seen them all?"""

# Reinforcement help message
rewards = """Robots collect [y]es's, [n]o's, [l]ikes and [d]islikes.\
 Robots that are disobedient (y<n) and unpopular (l<d) are periodically killed,\
  and are replaced with randomly-modified copies of more obedient (y>n)\
   and popular (l>d) survivors. Thus, the robots evolve, based on your guidance,\
    to become more obedient and popular."""

scores = """You get one point every time you reinforce a robot with y, n, l, or d,\
 and each time you vote for a command. To see your score, type ?myscore"""

commandScores = """We wish to discover which commands are most learnable by the robots.\
 A command is considered learnable if, over time, robots become increasingly obedient\
  to that command. In other words, bots collect an increasing number\
   of yes's from the crowd, under that command, over time."""

votes = """Every three minutes, the command most voted on by the crowd is issued to the robot.\
 There is no set list; you can type in anything you like.\
  You can vote for a command by typing !command. Don't forget the exclamation mark!"""

silver = """Every silver robot is a new unseen robot that is added to the population of robots every hour."""

first_time = 'Congratulations! You just earned your first point.'

# Organize messages by type
help_type = {'general': gen, 'silverrobots': silver,
             'robots': bot, 'commandscores': commandScores,
             'reinforcement': rewards, 'reinforcements': rewards,
             'scores': scores, 'votes': votes}


db.flush_old_unprocessed_helps()

while True:
    # to send a pong message to twitch server otherwise the connection is closed.
    # receive_message(..) in twitch class is a blocking function and not suitable 
    # for help bot.
    # msg_from_twitch = t.recieve_messages(amount = 1024)

    # get the oldest unprocessed request for help with flag=0.
    records = db.fetch_oldest_help()

    if records is None: continue
    
    msg = records['txt']
    username = records['userName']
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), records
    msg_to_send = msg[1:].rstrip()

    if msg == '?myscore':
        result = db.fetch_user_score(username)
        sent = t.send_message("@"+ username + ", your score:"+ str(result['score']))
        print('Num of bytes sent out:', sent)

    elif msg == 'first_time_contribution':
        sent = t.send_message('@' + username + ' ' + first_time)
        print('Num of bytes sent out: ', sent)

    elif msg_to_send in help_type:
        sent = t.send_message('@' + username + ' ' + help_type.get(msg_to_send))
        print('Num of bytes sent out: ', sent)

    else:
        sent = t.send_message('@' + username + ' ' + help_type.get('general'))
        print('Num of bytes sent out:', sent)

    time.sleep(SLEEP_RATE)

