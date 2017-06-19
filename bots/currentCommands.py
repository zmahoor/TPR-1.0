from pygameWrapper import PYGAMEWRAPPER
import time
import random
import pygame
from database import DATABASE
from settings import *
import math
import copy

startTime = time.time()
call = True
#create database object
db = DATABASE()

#create window
window = PYGAMEWRAPPER(width = 960, height = 250, fontSize = 20)

#y-coordinates of top 3 commands
y = [100, 150, 200]

reset = 0

#List format
# [ (c_1, v_1, [users]), (c_2, v_2, [users]), ... (c_n, v_n, [users]) ]


#Checks li for an instance of c
#If exists, return the index where it's located
def Return_Index(l, c):

        if l == [] or l == None:
                
                return None	#return None if list is empty
        
        index = None		#return None if c is not found

        for j in range(0,len(l)):

                if l[j][0] == c:

                        exists = True

                        i = j

                        return i
        


curr = 0
def Add_Time_Since_Start(call, cr):

        timeSinceStart = time.time() - startTime
	
        s = int(timeSinceStart)

	if s != cr:
		cr = s
		call = True

        m, s = divmod(s, 60)

        timer = ''

        timer = timer + str(30 - s) + 's '

	window.Draw_Text("Time to next:   " + timer, x = 800, y = 200) 

	return s, call, cr

# 1---get commands in current cycle
# 2---get total number of votes for each command
# 3---keep track of which user voted for which command
def Get_Commands():

        a = []
        
        newCmds = db.Fetch_For_Command_Window(interval = (reset-1) * 10)
	print reset - 1
	#print 'COMMANDS'     

        for i in newCmds:

                usn = i['userName'].upper()
                
                cmn = i['cmdTxt'].upper()

                index = Return_Index(a, cmn)
                
                if index != None:	 #if command is already in the list
                        
                        temp = a[index][2]

                        if usn not in temp:

                                temp.append(usn)	#add user to user list

                        print "temp: ", temp

                        c = a[index][0]

                        v = a[index][1]

                        tup = (c, v + 1, copy.deepcopy(temp))	#increment votes by 1

                        del a[index]

                        a.append(tup)

                else:			#if empty, create new element

                        a.append( (cmn.upper(), 1, [usn]) )
                        
        a.sort(key = lambda a : a[1])	#sort the list by vote order
        
        a = a[::-1]

        return a
        
ctr = 0

#li = Get_Commands()
li = []
xc = 1000


while 1:

        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                        
                        window.Quit()
                        
        window.Wipe()

        window.Draw_Text('These are the top commands for the next robot to be given.'.upper(), x = 10, y = 10)
        window.Draw_Text('Please vote by typing in "!commandName"'.upper(), x = 10, y = 35)
        
	c, call, curr = Add_Time_Since_Start(call, curr)
	
        size = len(li)
        if size > 3:
                size = 3
        cols = ['RED', 'BLUE', 'DARKGREEN']
        for i in range (0, size):
                window.Draw_Text(li[i][2][0].upper(), x = xc, y = y[i], color = 'DARKGRAY')
                window.Draw_Rect(180, y[i], 3*li[i][1] + 15, 20, color = cols[i])
                window.Draw_Text(str(li[i][1]), x = 183, y = y[i]-1, color = 'WHITE')
                window.Draw_Text(li[i][0], x = 25, y = y[i]) 
        
        xc = xc - 0.8
        
        time.sleep(.01)

        ctr = ctr + 1

        if c%10 == 0:
		if call:
			reset = reset + 1
			li = Get_Commands()
			
                	print 'COMMANDS'
			call = False
		
                xc = 1000

        if c == 30:
                reset = 0
		startTime = time.time()

                if li != []:
                        newActive = li[0][0]
                        print li
                        print "newActive: ", newActive
                
                        db.Set_Current_Command(newActive)
                else:
                        db.Set_Current_Command(DEFAULT_COMMAND)
                          
	window.Refresh()


        


        
