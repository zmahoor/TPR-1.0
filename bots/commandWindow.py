import numpy as np
import random
import time
from pygameWrapper import PYGAMEWRAPPER
from timer import TIMER
from settings import *
import database
import datetime

COMMAND_DURATION = 1 * 60
COMMAND_WINDOW_W = 950
COMMAND_WINDOW_H = 280

window = PYGAMEWRAPPER(width=COMMAND_WINDOW_W, height=COMMAND_WINDOW_H)

currentCommand = DEFAULT_COMMAND

mydatabase = database.DATABASE()

currentTime = datetime.datetime.now()
currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")

mydatabase.Add_To_Unique_Commands_Table(currentCommand, currentTime, 1.0)

mydatabase.Set_Current_Command(currentCommand)

def DRAW_COMMNAND_WINDOW(timeRemaining):
    global currentCommand

    window.Wipe()

    myy=10
    window.Draw_Text("Type !newcommand to change the current command. ",x= 10, y=myy) 
    # window.Draw_Text(currentCommand, x= 500, y=myy, color='brown')

    myy += 40
    window.Draw_Text(str(timeRemaining) + " seconds until the next command.", x= 10, y=myy)

    window.Refresh()


def main():

    global currentCommand

    commandTimer = TIMER(COMMAND_DURATION)

    while True:

        commandTimer.Reset()

        while not commandTimer.Time_Elapsed():

            DRAW_COMMNAND_WINDOW(commandTimer.Time_Remaining())

        temp = mydatabase.Find_Most_Popular_Command()

        print "popular command: ", temp

        if temp!= None: 
            currentCommand = temp['cmdTxt']
            mydatabase.Set_Current_Command(currentCommand)

        else:
            currentCommand = DEFAULT_COMMAND
            mydatabase.Set_Current_Command(currentCommand)

main()


