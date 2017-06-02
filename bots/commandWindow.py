import numpy as np
import random
import time
from pygameWrapper import PYGAMEWRAPPER
from timer import TIMER
from settings import *
import database

COMMAND_DURATION = 1 * 60
COMMAND_WINDOW_W = 950
COMMAND_WINDOW_H = 280
DEFAULT_COMMAND = "move"

window = PYGAMEWRAPPER(width=COMMAND_WINDOW_W, height=COMMAND_WINDOW_H)

currentCommand = DEFAULT_COMMAND
prevCommand = ""
mydatabase = database.DATABASE()

def DRAW_COMMNAND_WINDOW(timeRemaining):
    global currentCommand

    window.Wipe()

    myy=10
    window.Draw_Text("Type !newcommand to change the command ",x= 10, y=myy) 
    window.Draw_Text(currentCommand, x= 500, y=myy, color='brown')

    myy += 40
    window.Draw_Text(str(timeRemaining) + " seconds until the next command.", x= 10, y=myy)

    window.Refresh()


def main():

    global currentCommand
    global prevCommand

    commandTimer = TIMER(COMMAND_DURATION)

    while True:

        commandTimer.Reset()

        while not commandTimer.Time_Elapsed():

            DRAW_COMMNAND_WINDOW(commandTimer.Time_Remaining())

        temp = mydatabase.Fetch_Popular_Command()

        print "popular command: ", temp
        if temp!= None: 

            prevCommand    = currentCommand
            currentCommand = temp['cmdTxt']

            if currentCommand != prevCommand:
                mydatabase.Set_Current_Command(currentCommand)

main()


