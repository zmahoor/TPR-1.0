import numpy as np
import random
import time
from pygameWrapper import PYGAMEWRAPPER
from timer import TIMER
from settings import *
import database
import datetime
from time import sleep
import pygame
from copy import deepcopy

COMMAND_DURATION = 3 * 60
DB_FETCH_DURATION = 10
COMMAND_WINDOW_W = 900
COMMAND_WINDOW_H = 275
Y_COOR = [65, 115, 165]
NAME_X = [ 800, 800, 800]

COLORS      = ['RED', 'BLUE', 'DARKGREEN']

window = PYGAMEWRAPPER(width=COMMAND_WINDOW_W, height=COMMAND_WINDOW_H, fontSize=25)
animated_list = []
currentCommand = DEFAULT_COMMAND

mydatabase  = database.DATABASE()

currentTime = datetime.datetime.now()
currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")

mydatabase.Add_To_Unique_Commands_Table(DEFAULT_COMMAND, currentTime, 1.0, active=1)
mydatabase.Find_Most_Voted_Command()
mydatabase.Tobe_Animated_In_Command_Window()

def Draw_Command_Window(timeRemaining):

    global currentCommand
    global animated_list

    window.Wipe()

    myy=10
    window.Draw_Text('Type !command to vote for the next command (for example type !move).', x = 10, y = 2)
    window.Draw_Text('Top commands for the next robots are:', x = 10, y = 28)

    if timeRemaining < 0: timeRemaining = 0
    minute, second = divmod(timeRemaining, 60)
    hour, minute   = divmod(minute, 60)
    timeRemaining  = "%02d:%02d"%(minute, second)

    MAX = 460

    size = min(len(animated_list), 3)
    if size == 0:     
        X_VAL = 10
    else:
        X_VAL = max(10, max(len(animated_list[i]['cmdTxt']*14) for i in range(0, size)))

    X_VAL = X_VAL + 25
    if X_VAL > MAX: X_VAL = MAX

    for i in range(0, min(len(animated_list), 3)):

        cmdTxt = animated_list[i]['cmdTxt']
        votes  = animated_list[i]['votes']
        users  = animated_list[i]['users']

        # print NAME_X

        if len(users) != 0:
            name = users[0]

            if  NAME_X[i] >= 700:
                window.Draw_Text(name, x = NAME_X[i], y = Y_COOR[i], color = 'DARKGRAY')
                NAME_X[i] -= 1          

            else:
                NAME_X[i] = 800
                animated_list[i]['users'].pop(0)

        window.Draw_Rect(X_VAL, Y_COOR[i]+8, 3*votes + 15, 20, color = COLORS[i])
        window.Draw_Text(str(votes), x = X_VAL + 2, y = Y_COOR[i]-1, color = 'WHITE')
        window.Draw_Text(cmdTxt, x = 25, y = Y_COOR[i]) 


    window.Draw_Text("Command with the most votes will be sent to the robot in " + timeRemaining, x = 10, y = 220) 
    window.Draw_Text("Need help? Type ?votes ", x = 675, y = 220) 


    window.Refresh()

def process( tobe_animated ):

    global animated_list

    for item in tobe_animated:
        cmdTxt   = item['cmdTxt']
        userName = item['userName']

        match =  next((item for item in animated_list if item['cmdTxt'] == cmdTxt), None)

        if match != None:
            match['votes']+=1
            match['users'].append(userName)

        else:
            temp = {'cmdTxt':cmdTxt, 'votes': 1, 'users':[userName]}
            animated_list.append(temp)

    animated_list = sorted(animated_list, key=lambda k:k['votes'], reverse=True)

    print animated_list
    print

def main():

    global currentCommand
    global animated_list

    commandTimer = TIMER(COMMAND_DURATION)
    smallTimer   = TIMER(DB_FETCH_DURATION)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.Quit()

        if commandTimer.Time_Elapsed():

            animated_list[:] = []
            temp = mydatabase.Find_Most_Voted_Command()

            print "Most voted command: ", temp

            if temp!= None:  currentCommand = temp['cmdTxt']
            else: currentCommand = DEFAULT_COMMAND

            mydatabase.Set_Current_Command(currentCommand)
            commandTimer.Reset()

        elif not commandTimer.Time_Elapsed():

            if smallTimer.Time_Elapsed():

                tobe_animated = mydatabase.Tobe_Animated_In_Command_Window()
                if tobe_animated != None:
                    process( tobe_animated)

                smallTimer.Reset()

            Draw_Command_Window(commandTimer.Time_Remaining())

main()


