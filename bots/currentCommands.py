from pygameWrapper import PYGAMEWRAPPER
import time
import random
import pygame
from database import DATABASE

db = DATABASE()

window = PYGAMEWRAPPER(width = 960, height = 250, fontSize = 20)

y = [100, 150, 200]

reset = 1

# [ (c1, v1, [users]), (c2, v2, [users]), ... (cn, vn, [users]) ]

an = []

def Get_Commands():

        a = []
        
        newCmds = db.Fetch_For_Command_Window(interval = reset * 10)

        print reset * 10

        for i in newCmds:

                usn = i.get('userName')
                
                cmn = i.get('cmdTxt')
                
                exists = False
                
                for j in range(0,an):
                        if a[j][0] == cmn:
                                exists = True
                                index = j
                if exists:
                        a[index][1] = a[index][1] + 1
                        a[index][2].append(usn)
                else:
                        a.append( (cmn.upper(), 1, [usn]) )
                        
        a.sort(key = lambda a : a[1])
        
        a = a[::-1]
                                
        return a
        
ctr = 0

li = Get_Commands()

xc = 1000

while 1:

        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                        
                        window.Quit()
                        
        window.Wipe()

        window.Draw_Text('These are the top commands for the next robot to be given.', x = 10, y = 10)
        window.Draw_Text('Please vote by typing in "!commandName"', x = 10, y = 35)
        
        size = len(li)
        if size > 3:
                size = 3

        for i in range (0, size):
                window.Draw_Text(li[i][2].upper(), x = xc, y = y[i], color = 'DARKGRAY')
                window.Draw_Rect(180, y[i], 3*li[i][1] + 15, 20, color = 'BLACK')
                window.Draw_Text(str(li[i][1]), x = 183, y = y[i]-1, color = 'WHITE')
                window.Draw_Text(li[i][0], x = 25, y = y[i]) 
        
        xc = xc - 0.8
        
        time.sleep(.01)

        ctr = ctr + 1

        if ctr == 1000:

                reset = reset + 1
                
                li = Get_Commands()
                
                xc = 1000
                
                ctr = 0

        if reset == 18:
                
                reset = 0

                newActive = an[0][0]
                
                db.Set_Current_Command(newActive)
                          
	window.Refresh()


        


        
