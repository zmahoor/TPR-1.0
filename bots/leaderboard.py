from table import TABLE
from pygameWrapper import PYGAMEWRAPPER
import time
import random
from database import DATABASE
import pygame
from timer import TIMER

DB = DATABASE()
WIDTH     = 480
HEIGHT    = 500
FONT_SIZE = 17
WINDOW = PYGAMEWRAPPER(width = WIDTH, height = HEIGHT, fontSize = FONT_SIZE)
UPDATE_PERIOD = 10
updateTimer = TIMER(UPDATE_PERIOD)

#get screen
SCREEN = WINDOW.screen
    
#create new table object
table = TABLE(WINDOW, width = WIDTH, height = HEIGHT)

#This function takes users who are recently active and
#picks a random one to be displayed at the bottom of the table
def get_NewUser():

    newUser = ('  ', 0, 99999)
    test = DB.Fetch_Recent_Active_Users(interval = 10)
        
    print 'test', test

    if test != ():
        size = len(test)
        if size == 1:
            r = 0
        else:
            r = random.randint(0,size-1)
        newUser = (test[r].get('userName'),test[r].get('score'),test[r].get('rank'))

    return newUser

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
    
    WINDOW.Draw_Text('USERNAME', x = WIDTH*0.15, y = .5*HEIGHT/12.0)
    WINDOW.Draw_Text('RANK', x = 4, y = .5*HEIGHT/12.0)    
    WINDOW.Draw_Text('SCORE', x = .7*WIDTH, y = .5*HEIGHT/12.0)

    WINDOW.Draw_Text('For more information, type "?scores"'.upper(), x = .12*WIDTH, y = 12.3/13.0 * HEIGHT)

    if updateTimer.Time_Elapsed():

        newList = Parse_Users(DB.Fetch_Top_Users(10))
        newUser = get_NewUser()
        updateTimer.Reset()

        print 'user', newUser

        WINDOW.Refresh()


