from pygameWrapper import PYGAMEWRAPPER
import time
import random
import pygame
from database import DATABASE
from settings import *
import math
import copy

#---Variables to keep track of time---#
startTime = time.time()
call = True
reset = 0
curr = 0
#-------------------------------------#

#-------Constants-------#
WIDTH 		= 920
HEIGHT 		= 250
FONT_SIZE	= 20
COLORS 		= ['RED', 'BLUE', 'DARKGREEN']
DB 		= DATABASE()
Y_COOR 		= [75, 125, 175]
WINDOW 		= PYGAMEWRAPPER(width = WIDTH, height = HEIGHT, fontSize = FONT_SIZE)
TIME_OF_CYCLE 	= 10  #in seconds
NUM_CYCLES 	= 18
#-----------------------#

#List format
# [ (c_1, v_1, [users]), (c_2, v_2, [users]), ... (c_n, v_n, [users]) ]


#Checks li for an instance of c
#If exists, return the index where it's located
def Return_Index(list_to_check, command_to_check):
	l = list_to_check
	c = command_to_check
	
        if l == [] or l == None:
                
                return None	#return None if list is empty
        
        index = None		#return None if c is not found

        for i in range(0,len(l)):

                if l[i][0] == c:

                        exists = True

                        return i
        
def Add_Time_Since_Start(call, cr):

        timeSinceStart = time.time() - startTime
	
        timeSinceStart = int(timeSinceStart)

	if timeSinceStart != cr:
		cr = timeSinceStart
		call = True
	
	s = NUM_CYCLES*TIME_OF_CYCLE - timeSinceStart
	
        m, s = divmod(s, 60)

	if s < 10:
		s = '0' + str(s)
	else:
		s = str(s)

        timer = ''
	
        timer = timer + str(m) + ':' + s

	WINDOW.Draw_Text("Time to next:   " + timer, x = 740, y = 200) 

	return timeSinceStart, call, cr

# 1---get commands in current cycle
# 2---get total number of votes for each command
# 3---keep track of which user voted for which command
def Get_Commands():

        cmds_to_return = []
        
        full_cmd_list = DB.Fetch_For_Command_Window(interval = (reset-1) * TIME_OF_CYCLE)
	print reset - 1
	#print 'COMMANDS'     

        for i in full_cmd_list:

                usn = i['userName'].upper()
                
                cmn = i['cmdTxt'].upper()

                index = Return_Index(cmds_to_return, cmn)
                
                if index != None:	 #if command is already in the list
                        
                        temp = cmds_to_return[index][2]

                        if usn not in temp:

                                temp.append(usn)	#add user to user list

                        command = cmds_to_return[index][0]

                        votes = cmds_to_return[index][1]

                        tup = (command, votes + 1, copy.deepcopy(temp))	#increment votes by 1

                        del cmds_to_return[index]

                        cmds_to_return.append(tup)

                else:			#if empty, create new element

                        cmds_to_return.append( (cmn.upper(), 1, [usn]) )
                        
        cmds_to_return.sort(key = lambda cmds_to_return : cmds_to_return[1])	#sort the list by vote order
        
        return cmds_to_return[::-1]


li = []
li = Get_Commands()
start_x_names = 1000
names = ['','','']

while 1:

        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                        
			WINDOW.Quit()
                        
        WINDOW.Wipe()

        WINDOW.Draw_Text('These are the top commands for the next robot to be given.'.upper(), x = 10, y = 10)
        WINDOW.Draw_Text('Please vote by typing in "!commandName"'.upper(), x = 10, y = 35)
        
	timePassed, call, curr = Add_Time_Since_Start(call, curr)
	
        size = len(li)

        if size > 3:
                size = 3

        MAX = 460
        X_VAL = 10
        for j in range (0,size):
                len_of_characters = len(li[j][0]) * 14
                if len_of_characters > X_VAL:
                        X_VAL = len_of_characters

        X_VAL = X_VAL + 25
        if X_VAL > MAX:
                X_VAL = MAX

        for i in range (0, size):
                
                WINDOW.Draw_Text(names[i].upper(), x = start_x_names, y = Y_COOR[i], color = 'DARKGRAY')
                WINDOW.Draw_Rect(X_VAL, Y_COOR[i], 3*li[i][1] + 15, 20, color = COLORS[i])
                WINDOW.Draw_Text(str(li[i][1]), x = X_VAL + 3, y = Y_COOR[i]-3, color = 'WHITE')
                WINDOW.Draw_Text(li[i][0], x = 25, y = Y_COOR[i]) 
        
        start_x_names = start_x_names - 0.8
        
        time.sleep(.01)

        if timePassed % TIME_OF_CYCLE == 0:
		if call:
			reset = reset + 1
			li = Get_Commands()
			
                	print 'COMMANDS'
			call = False
		
                start_x_names = 1000
                names = []
                for i in range (0, len(li)):
                        r = random.randint(0, len(li[i][2])-1)
                        names.append(li[i][2][r])

        if timePassed == NUM_CYCLES * TIME_OF_CYCLE:
                reset = 0
		startTime = time.time()

                if li != []:
                        newActive = li[0][0]
                        print li
                        print "newActive: ", newActive
                
                        DB.Set_Current_Command(newActive)
                else:
                        DB.Set_Current_Command(DEFAULT_COMMAND)
                          
	WINDOW.Refresh()


        


        
