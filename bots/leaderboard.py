"""
This script displays a window of top 5 users by score.
"""
from table import TABLE
from pygameWrapper import PYGAMEWRAPPER
from database import DATABASE
import pygame
from timer import TIMER
import numpy as np

DB = DATABASE()
WIDTH = 440
HEIGHT = 360
FONT_SIZE = 20
TITLE = "TPR- Top Users"
WINDOW = PYGAMEWRAPPER(width=WIDTH, height=HEIGHT, title=TITLE, fontSize=FONT_SIZE)
UPDATE_PERIOD = 10
WSPACE = 5
# get screen
SCREEN = WINDOW.screen
    
# create new table object
table = TABLE(WINDOW, width=WIDTH, height=HEIGHT)
updateTimer = TIMER(UPDATE_PERIOD)

# This function takes users who are recently active and
# picks a random one to be displayed at the bottom of the table
def get_NewUser():
    recent_users = DB.fetch_recent_active_users(interval=10)
    if recent_users is None: return None

    if len(recent_users)>0:
        index = np.random.randint(0, len(recent_users))
        return recent_users[index]
    else:
        return None

# This function takes apart the database information and puts it
# into a format that the table class can use
def Parse_Users(li):
    userlist = []
    if li is None: return []
    for i in li:            
        n = i.get('userName')
        s = i.get('score')
        userlist.append((n,s))
    return userlist


# newList = Parse_Users(DB.Fetch_Top_Users(10))  
newList = Parse_Users(DB.fetch_top_daily_users(10))
newUser = get_NewUser()
print 'user', newUser

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WINDOW.Quit()
    WINDOW.Wipe()
    table.update(newList, newUser)
    
    WINDOW.Draw_Text('Username', x=WIDTH*0.15, y=15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('Rank', x=4, y=15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('Score', x=.7*WIDTH, y=15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)
    # WINDOW.Draw_Text('Top Users Teaching the Robots', x = 0.15*WIDTH, y = 1, bold=True, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('Today\'s Top Users', x=0.25*WIDTH, y=1, bold=True, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('Need help? Type', x=.12*WIDTH, y=HEIGHT-25, fontSize=FONT_SIZE)
    WINDOW.Draw_Text("?scores", x=WINDOW.text_x+WINDOW.text_width+WSPACE, y=HEIGHT-25, color='BROWN', fontSize=FONT_SIZE)

    if updateTimer.Time_Elapsed():
        # newList = Parse_Users(DB.Fetch_Top_Users(10))
        newList = Parse_Users(DB.fetch_top_daily_users(10))
        newUser = get_NewUser()
        updateTimer.Reset()
        print 'user', newUser

    WINDOW.Refresh()
