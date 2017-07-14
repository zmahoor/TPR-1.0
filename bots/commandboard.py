from table import TABLE
from pygameWrapper import PYGAMEWRAPPER
import time
import random
from database import DATABASE
import pygame
from timer import TIMER
import numpy as np

DB = DATABASE()
FONT_SIZE = 20
WIDTH = 440
HEIGHT = 360
WINDOW = PYGAMEWRAPPER(width = WIDTH, height = HEIGHT, fontSize = FONT_SIZE)
SCREEN = WINDOW.screen
UPDATE_PERIOD = 10
    
table = TABLE(WINDOW, width = WIDTH, height = HEIGHT)
updateTimer = TIMER(UPDATE_PERIOD)
    
def get_NewCmd():
    #gets recent commands and picks one at random
    recent_cmd = DB.Fetch_Recent_Typed_Command(interval = 10)

    if recent_cmd == None: return None
    if len(recent_cmd)>0:
        index = np.random.randint(0, len(recent_cmd))
        return recent_cmd[index]
    else:
        return None

def Parse_Scores(li):
    #converts dict into list of tuples
    #allows universal passing to table object
    scorelist = []

    if li == None: return []

    for i in li:
        n = i.get('cmd')
        s = i.get('score')
        scorelist.append((n,s))
    return scorelist

newList = Parse_Scores(DB.Fetch_Topn_Unique_Commands(10))
newCmd = get_NewCmd()
print 'user', newCmd

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WINDOW.Quit()
                        
    WINDOW.Wipe()
    
    table.Update(newList, newCmd)
    WINDOW.Draw_Text('COMMAND', x = WIDTH*0.15, y = 15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('RANK', x = 4, y = 15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('SCORE', x = 0.7*WIDTH, y = 15+.5*HEIGHT/12.0, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('TOP COMMANDS LEARNED BY THE ROBOTS', x = 0.10*WIDTH, y = 1, fontSize=FONT_SIZE)
    WINDOW.Draw_Text('Need help? Type ?commandScores', x = .12*WIDTH, y = HEIGHT - 25, fontSize=FONT_SIZE)
    
    if updateTimer.Time_Elapsed():

        newList = Parse_Scores(DB.Fetch_Topn_Unique_Commands(10))
        newCmd  = get_NewCmd()
        
        updateTimer.Reset()
        print 'user', newCmd

    WINDOW.Refresh()
