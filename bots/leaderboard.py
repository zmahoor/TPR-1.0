from table import TABLE
from pygameWrapper import PYGAMEWRAPPER
import time
import random
from database import DATABASE
import pygame
from timer import TIMER
import numpy as np

DB = DATABASE()
WIDTH     = 440
HEIGHT    = 360
FONT_SIZE = 20
WINDOW = PYGAMEWRAPPER(width = WIDTH, height = HEIGHT, fontSize = FONT_SIZE)
UPDATE_PERIOD = 10

#get screen
SCREEN = WINDOW.screen
    
#create new table object
table = TABLE(WINDOW, width = WIDTH, height = HEIGHT)
updateTimer = TIMER(UPDATE_PERIOD)

#This function takes users who are recently active and
#picks a random one to be displayed at the bottom of the table
def get_NewUser():

    recent_users = DB.Fetch_Recent_Active_Users(interval = 10)
    if recent_users == None: return None

    if len(recent_users)>0:
        index = np.random.randint(0, len(recent_users))
        return recent_users[index]
    else:
        return None

#This function takes apart the database information and puts it 
#into a format that the table class can use
def Parse_Users(li):

    userlist = []

    if li == None: return []

    for i in li:            
        n = i.get('userName')
        s = i.get('score')
        userlist.append((n,s))

    return userlist

newList = Parse_Users(DB.Fetch_Top_Users(10))  
newUser = get_NewUser()
print 'user', newUser

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WINDOW.Quit()
                        
    WINDOW.Wipe()
    
    table.Update(newList, newUser)
    
    WINDOW.Draw_Text('USERNAME', x = WIDTH*0.15, y = 15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('RANK', x = 4, y = 15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)    
    WINDOW.Draw_Text('SCORE', x = .7*WIDTH, y = 15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('TOP USERS TEACHING THE ROBOTS', x = 0.15*WIDTH, y = 1, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('Need help? Type ?scores', x = .12*WIDTH, y = HEIGHT - 25, fontSize=FONT_SIZE)

    if updateTimer.Time_Elapsed():

        newList = Parse_Users(DB.Fetch_Top_Users(10))
        newUser = get_NewUser()
        updateTimer.Reset()

        print 'user', newUser

    WINDOW.Refresh()
