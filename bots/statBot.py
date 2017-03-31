import numpy as np
import random
from copy import deepcopy
from time import *
import sys 
import os 
from termcolor import colored
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE
from settings import *

robotType = "4leg"

mydatabase = DATABASE();

def main():
    
    topn = 10
    cmdVals = []
    cmdTxt = []

    pos = np.arange(topn)+.5    # the bar centers on the y axis
    print pos

    plt.ion() ## Note this correction
    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.axvline(0, color='k', lw=3)   # poor man's zero level

    ax.set_xlabel('# of times called')
    ax.set_title('Top Commands Ever Called')

    i=0

    while True:

        cmdVals = []
        cmdTxt = []

        commands = mydatabase.Fetch_All_Commands(topn)
        if commands == None : continue

        for cmd in commands:
            cmdVals.append(cmd['numIssued'])
            cmdTxt.append(cmd['cmdTxt'])

        print cmdVals
        print cmdTxt

        ax.barh(pos, cmdVals, align='center', height=0.4)
        ax.set_yticks(pos)
        ax.set_yticklabels(cmdTxt)

        plt.show()
        plt.pause(10.)

        i+=1


main()

