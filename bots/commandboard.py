from table import TABLE
from pygameWrapper import PYGAMEWRAPPER
import time
import random
from database import DATABASE
import pygame

db = DATABASE()
window = PYGAMEWRAPPER(width = 480, height = 500)
c = 0

w = window.size[0]
h = window.size[1]

screen = window.screen
    
table = TABLE(window, width = w, height = h)
    
def get_NewCmd():
    #gets recent commands and picks one at random
    newCmd = ('   ', 0, 99999)
    test = db.Fetch_Recent_Typed_Command(interval = 10)
    print 'test', test
    if test != ():
        size = len(test)
        if size == 1:
            r = 0
        else:
            r = random.randint(0,size-1)
        newCmd = (test[r].get('cmd'),test[r].get('score'),test[r].get('rank'))
    return newCmd

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

newList = Parse_Scores(db.Fetch_Topn_Unique_Commands(10))
newCmd = get_NewCmd()
print 'user', newCmd

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.Quit()
                        
    window.Wipe()
    
    table.Update(newList, newCmd)
    window.Draw_Text('COMMAND', x = (w/2.0) - 100, y = .5*h/12.0)
    window.Draw_Text('RANK', x = 7, y = .5*h/12.0)
    window.Draw_Text('SCORE', x = .65*w, y = .5*h/12.0)
    window.Draw_Text('#YES', x = .815*w, y = .5*h/12.0)
    window.Draw_Text('#NO', x = .915*w, y = .5*h/12.0)

    window.Draw_Text('Need help? type "?commands"'.upper(), x = .12*w, y = 12.3/13.0 * h)
    
    time.sleep(.2)
    c = c + 1
    if c > 51:
        newList = Parse_Scores(db.Fetch_Topn_Unique_Commands(10))
        newCmd = get_NewCmd()
        print 'user', newCmd
        c = 0    
    window.Refresh()

