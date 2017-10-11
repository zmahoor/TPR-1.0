from pygameWrapper import PYGAMEWRAPPER
import time
import random
from database import DATABASE
import pygame
from timer import TIMER
import numpy as np
import datetime

DB = DATABASE()
WIDTH = 900
HEIGHT = 200
FONT_SIZE = 23
UPDATE_PERIOD = 2
BLINK_PERIOD = 10
DRAW_PERIOD = 30
WSPACE = 85
#get screen
WINDOW = PYGAMEWRAPPER(width=WIDTH, height=HEIGHT, title="Robot's Information",
                       fontSize=FONT_SIZE)
SCREEN = WINDOW.screen
BG_COLOR = (30, 144, 255)
#create new table object
updateTimer = TIMER(UPDATE_PERIOD)
blinkTimer = TIMER(BLINK_PERIOD)
prev_cmd = ""


def Draw_Robot_Window( robotInfo ):
    global prev_cmd
    # print ('current robot info: ', robotInfo)
    if robotInfo is None: return None
    allTypes = {'1': 'stickbot', '2': 'twigbot', '3': 'branchbot', '4': 'treebot',
                'quadruped':'quadruped', 'shinbot': 'tablebot', 'crabbot': 'crabbot',
                'starfishbot': 'starfishbot', 'spherebot': 'spherebot', 'snakebot': 'snakebot',
                'snakeplusbot': 'snakeplusbot', 'humanoid': 'humanoid', 'crabplusbot': 'crabplusbot',
                'quadrupedplus': 'quadrupedplus'}

    typeKey    = robotInfo['robotType']
    robotType  = allTypes[typeKey]
    robotID    = robotInfo['robotID']
    color      = robotInfo['color']
    numOfKind  = robotInfo['numOfKind'] if robotInfo['numOfKind'] is not None else 0
    numYes     = robotInfo['numYes'] if robotInfo['numYes'] is not None else 0
    numNo      = robotInfo['numNo'] if robotInfo['numNo'] is not None else 0
    numLike    = robotInfo['numLike'] if robotInfo['numLike'] is not None else 0
    numDislike = robotInfo['numDislike'] if robotInfo['numDislike'] is not None else 0
    cmdTxt     = robotInfo['cmdTxt']

    dt = datetime.datetime.now() - robotInfo['birthDate']
    minute, second = divmod(dt.days*86400 + dt.seconds, 60)
    hour, minute   = divmod(minute, 60)
    day, hour      = divmod(hour, 24)

    age = "%dd %dh:%02dm:%02ds" %(day, hour, minute, second)

    myy = 10
    WINDOW.Draw_Text("This robot is trying to ", x=5, y=myy, color='WHITE', fontSize=30)

    if cmdTxt != prev_cmd:
        blinkTimer.Reset()

    if not blinkTimer.Time_Elapsed():
        WINDOW.Draw_Text(cmdTxt, x=WINDOW.text_x+WINDOW.text_width,
                        y=myy, color='YELLOW', bold=True, underline=False, fontSize=35)
    else:
        WINDOW.Draw_Text(cmdTxt, x=WINDOW.text_x+WINDOW.text_width,
                        y=myy, color='WHITE', bold=True, underline=False, fontSize=30)

    WINDOW.Draw_Text("Need help? Type ?", x=675, y=myy, color='WHITE',
                     fontSize=FONT_SIZE+5)
    myy += 40
    WINDOW.Draw_Text("If you think it is, type !"+color+"y. ("+str(numYes)+")", 
                     x=5, y=myy, color='WHITE', fontSize=FONT_SIZE)
    myy += 40
    WINDOW.Draw_Text("If not, type !"+color+"n.                ("+str(numNo)+")",
                    x=5, y=myy, color='WHITE', fontSize=FONT_SIZE)
    myy += 40
    WINDOW.Draw_Text("If you like this robot, type !"+color+"l. ("+str(numLike)+")",
                    x=5, y=myy, color='WHITE', fontSize=FONT_SIZE)
    myy += 40
    WINDOW.Draw_Text("If you dislike it, type !"+color+"d.        ("+str(numDislike)+")",
                    x=5, y=myy, color='WHITE', fontSize=FONT_SIZE)

    prev_cmd = cmdTxt


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
