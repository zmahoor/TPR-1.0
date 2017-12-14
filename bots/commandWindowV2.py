"""
this script displays a window prompting users to vote for the next command.
"""
import numpy as np
from pygameWrapper import PYGAMEWRAPPER
from timer import TIMER
from settings import *
import database
import datetime
import pygame

COMMAND_DURATION = 3 * 60
DB_FETCH_DURATION = 5
COMMAND_WINDOW_W = 900
COMMAND_WINDOW_H = 210
Y_COOR = [65, 115, 165]
NAME_X = [ 800, 800, 800]
WSPACE = 5
FONT_SIZE = 23
TITLE = "TPR-  Top Voted Commands"
COLORS = ['RED', 'BLUE', 'DARKGREEN']
DEFAULT_COMMANDS = ['jump', 'stop', 'backflip', 'spin', 'roll', 'walk', 'move backward',
                    'move forward', 'dance', 'run', 'flip']

window = PYGAMEWRAPPER(width=COMMAND_WINDOW_W, height=COMMAND_WINDOW_H, title=TITLE, fontSize=23)
animated_list = []
currentCommand = DEFAULT_COMMANDS[np.random.randint(0, len(DEFAULT_COMMANDS))]
mydatabase = database.DATABASE()

currentTime = datetime.datetime.now()
currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")

print 'Setting the default command as the active command...'
mydatabase.add_to_unique_commands_table(DEFAULT_COMMAND, currentTime, 1.0, active=1)
mydatabase.set_current_command(DEFAULT_COMMAND)

print 'Flushing previous unprocessed commands...'
mydatabase.find_most_voted_command()
mydatabase.tobe_animated_in_command_window()


def draw_command_window(timeRemaining):
    global currentCommand
    global animated_list

    window.Wipe()
    myy = 10
    window.Draw_Text("To vote for the next command, type in the chat a command preceded by ! (for example !walk).",
                     x=10, fontSize=FONT_SIZE)

    window.Draw_Text('Top voted commands are:', x=10, y=40, fontSize=FONT_SIZE)

    if timeRemaining < 0:
        timeRemaining = 0
    minute, second = divmod(timeRemaining, 60)
    hour, minute = divmod(minute, 60)
    timeRemaining = "%02dm:%02ds" %(minute, second)

    MAX = 500
    size = min(len(animated_list), 3)
    if size == 0:     
        X_VAL = 10
    else:
        X_VAL = max(10, max(len(animated_list[i]['cmdTxt']*14) for i in range(0, size)))

    X_VAL = X_VAL+25
    if X_VAL > MAX:
        X_VAL = MAX

    for i in range(0, min(len(animated_list), 3)):
        cmdTxt, votes, users = animated_list[i]['cmdTxt'], animated_list[i]['votes'], animated_list[i]['users']
        # print NAME_X

        if len(users) != 0:
            name = users[0]
            if NAME_X[i] >= 700:
                window.Draw_Text(name, x=NAME_X[i], y=Y_COOR[i], color='DARKGRAY', fontSize=FONT_SIZE)
                NAME_X[i] -= 1
            else:
                NAME_X[i] = 800
                animated_list[i]['users'].pop(0)

        window.Draw_Rect(X_VAL, Y_COOR[i]+8, 3*votes+15, 22, color=COLORS[i])
        window.Draw_Text(str(votes), x=X_VAL+2, y=Y_COOR[i]-1, color='WHITE', fontSize=FONT_SIZE)
        window.Draw_Text("votes", x=X_VAL+2+3*votes+15, y=Y_COOR[i]-1, fontSize=FONT_SIZE)

        if len(cmdTxt) > 50:
            cmdTxt = cmdTxt[0:50]

        window.Draw_Text(cmdTxt, x=25, y=Y_COOR[i], fontSize=FONT_SIZE)

    window.Draw_Text("Voting ends in "+timeRemaining, x=10, y=220, fontSize=FONT_SIZE)
    window.Draw_Text("Need help? Type", x=675, y=220, fontSize=FONT_SIZE)
    window.Draw_Text("?votes", x=window.text_x+window.text_width+WSPACE, y=220, color='BROWN', fontSize=FONT_SIZE)
    window.Refresh()


def process(tobe_animated):
    global animated_list

    for item in tobe_animated:
        cmdTxt, userName = item['cmdTxt'], item['userName']
        match = next((item for item in animated_list if item['cmdTxt'] == cmdTxt), None)
        if match is not None:
            match['votes'] += 1
            match['users'].append(userName)
        else:
            temp = {'cmdTxt': cmdTxt, 'votes': 1, 'users': [userName]}
            animated_list.append(temp)

    animated_list = sorted(animated_list, key=lambda k: k['votes'], reverse=True)
    print animated_list
    print


def main():
    global currentCommand
    global animated_list
    commandTimer, smallTimer = TIMER(COMMAND_DURATION), TIMER(DB_FETCH_DURATION)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.Quit()

        if commandTimer.Time_Elapsed():
            animated_list[:] = []
            temp = mydatabase.find_most_voted_command()
            print "Most voted command: ", temp

            if temp is not None:  currentCommand = temp['cmdTxt']
            else: currentCommand = DEFAULT_COMMANDS[np.random.randint(0, len(DEFAULT_COMMANDS))]
            mydatabase.set_current_command(currentCommand)
            commandTimer.Reset()

        elif not commandTimer.Time_Elapsed():
            if smallTimer.Time_Elapsed():
                tobe_animated = mydatabase.tobe_animated_in_command_window()
                if tobe_animated is not None:
                    process( tobe_animated)
                smallTimer.Reset()

            draw_command_window(commandTimer.Time_Remaining())


main()


