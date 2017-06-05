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

def get_NewUser():
    newUser = ('  ', 0, 99999)
    test = db.Fetch_Recent_Active_Users(interval = 10)
    print 'test', test
    if test != ():
        size = len(test)
        if size == 1:
            r = 0
        else:
            r = random.randint(0,size-1)
        newUser = (test[r].get('userName'),test[r].get('score'),test[r].get('rank'))
    return newUser

def Parse_Users(li):
    userlist = []

    if li == None: return []

    for i in li:
        n = i.get('userName')
        s = i.get('score')
        userlist.append((n,s))
    return userlist

newList = Parse_Users(db.Fetch_Top_Users(10))  
newUser = get_NewUser()
print 'user', newUser

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.Quit()
                        
    window.Wipe()
    
    table.Update(newList, newUser)
    window.Draw_Text('USERNAME', x = (w/2.0) - 100, y = .5*h/12.0)
    window.Draw_Text('RANK', x = 7, y = .5*h/12.0)
    window.Draw_Text('SCORE', x = .65*w, y = .5*h/12.0)
    window.Draw_Text('#Re', x = .815*w, y = .5*h/12.0)
    window.Draw_Text('#Cmd', x = .915*w, y = .5*h/12.0)

    window.Draw_Text('For more information, type "?scores"'.upper(), x = .12*w, y = 12.3/13.0 * h)
    
    time.sleep(.2)
    c = c + 1
    if c > 50:
        newList = Parse_Users(db.Fetch_Top_Users(10))
        newUser = get_NewUser()
        print 'user', newUser
        c = 0    
    window.Refresh()

