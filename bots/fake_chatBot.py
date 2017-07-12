from settings import *
from time import *
from database import DATABASE
import numpy as np

db = DATABASE()

# !r !g !b
def validPrefix():
    global validColors
    return [ "!"+color[0] for color in validColors]

# !rn 
def rewardSignals():
    global validColors

    validRS = [p+"y" for p in validPrefix()]+[p+"n" for p in validPrefix()]+\
    [p+"l" for p in validPrefix()]+[p+"d" for p in validPrefix()]

    return validRS

REWARDS = rewardSignals()
CMDS    = ['!walk very fast then jump', '!walk back then forward', '!crawl', '!jump',\
 '!walk', '!run away', '!break free', '!stay still', '!move', '!help',\
 '!walk forward', 'walk fast forward' , '!dance dance', '!dance', '!move forward', '!walkkk']

HELPS   = ['?' , '?rewards', '?commands', '?myscore', '?scores', '?robots', '?votes', '?project']
EXTRA   = ['helloO %$##', 'WHat is this?', 'DROP TABLE', 'SQL DELETE Rows']

DATA    = REWARDS + CMDS + HELPS + EXTRA

USERS = ['zmahoor', 'jfelag', 'doctorjoshuvm', 'tpr_bot1', 'ccappelle',\
    'abernatskiy', 'dwood', 'cfusting', 'jsmith', 'samk', 'marcin', 'roman.popov',\
    'krystalleger', 'sijmen']

#The main loop
while True:
    
    dindex = np.random.randint(len(DATA))
    uindex = np.random.randint(len(USERS))
    
    message = {'message': DATA[dindex], 'username': USERS[uindex]}   
    sleep(1.0)

    try:
        #Get info from message.
        msg = str(message['message'].lower().replace("'", ''))
        username = str(message['username'].lower())

        print(username + ": " + msg)
        currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())

        if(username not in filteredUsers):
            db.Add_To_Chat_Table(username, currentTime, msg)

    except Exception as e:
        print str(e)
        print("something went wrong. Unable inserting this message.")
        #end if not in filtered users
