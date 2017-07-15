from pygameWrapper import PYGAMEWRAPPER
import time
import random
from database import DATABASE
import pygame
from timer import TIMER
import numpy as np
import datetime

DB = DATABASE()
WIDTH     = 900
HEIGHT    = 150
FONT_SIZE = 23
UPDATE_PERIOD = 2
DRAW_PERIOD   = 30
WSPACE = 85
#get screen
WINDOW = PYGAMEWRAPPER(width = WIDTH, height = HEIGHT, title="Robot's Information", fontSize = FONT_SIZE)
SCREEN = WINDOW.screen
BG_COLOR = (0,191,255)
#create new table object
updateTimer = TIMER(UPDATE_PERIOD)

def Draw_Robot_Window( robotInfo ):

        # print ('current robot info: ', robotInfo)
        if robotInfo == None: return None

        allTypes = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot',\
        'quadruped':'quadruped', 'shinbot': 'tablebot', 'crabbot': 'crabbot',\
         'starfishbot':'starfishbot', 'spherebot':'spherebot', 'snakebot':'snakebot'}

        typeKey    = robotInfo['robotType']
        robotType  = allTypes[typeKey]

        robotID    = robotInfo['robotID']
        numOfKind  = robotInfo['numOfKind'] if robotInfo['numOfKind'] != None else 0
        numYes     = robotInfo['numYes'] if robotInfo['numYes'] != None else 0
        numNo      = robotInfo['numNo'] if robotInfo['numNo'] != None else 0
        numLike    = robotInfo['numLike'] if robotInfo['numLike'] != None else 0
        numDislike = robotInfo['numDislike'] if robotInfo['numDislike'] != None else 0
        cmdTxt     = robotInfo['cmdTxt']

        if robotInfo['birthDate']!=None:
            dt = robotInfo['birthDate'] - datetime.datetime.now()
        else:
            dt = robotInfo['firstDisplay']- robotInfo['lastDisplay']

        minute, second = divmod(dt.seconds, 60)
        hour, minute   = divmod(minute, 60)
        day, hour      = divmod(hour, 24)

        age = "%dd %dh:%02dm:%02ds"%(day, hour, minute, second)

        title = ["robotID", "Age", "Type", "Yes's", "No's", "Likes", "Dislikes"]

        value = [str(robotID), str(age), "1 of "+str(numOfKind)+" "+robotType+"s",str(numYes),\
         str(numNo), str(numLike), str(numDislike)]

        x_pos = [5, 120, 275, 500, 580, 690, 780]

        for i in range(0, len(value)):

            WINDOW.Draw_Text(title[i], x=x_pos[i], y=10, color='WHITE', fontSize=23)
            WINDOW.Draw_Text(value[i], x=x_pos[i], y=40, color='WHITE', fontSize=23)
        
        WINDOW.Draw_Text("Robot is trying to: ", x=5, y=110, color='WHITE', fontSize=30)
        WINDOW.Draw_Text(cmdTxt ,x=WINDOW.text_x+WINDOW.text_width,\
         y= 110, color='WHITE', bold=True, underline=False, fontSize=30)

        WINDOW.Draw_Text("Need help? Type ?robots", x=675, y=90, color='WHITE', fontSize=23)

robotInfo = DB.Fetch_Robot_Information()
 
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            WINDOW.Quit()
                        
    WINDOW.Wipe(BG_COLOR)    

    if updateTimer.Time_Elapsed():

        # fetch from database
        robotInfo = DB.Fetch_Robot_Information()
        updateTimer.Reset()

    Draw_Robot_Window(robotInfo)
    WINDOW.Refresh()
