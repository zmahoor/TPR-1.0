from pyrosim import PYROSIM
import numpy as np
import random
from individualTemplate import INDIVIDUAL
from copy import deepcopy
from time import *
import sys 
import pickle
import os 
from termcolor import colored
import constants as c

sys.path.append('../bots')

from database import DATABASE
from settings import *

# INDIVIDUAL_DURATION = 30
GENOME_SHAPE = [5, 8]
# GENOME_SHAPE =[4, 1]

colorIndex = 0
currentColor = validColors[colorIndex % len(validColors)]
numAliveIndividuals = 5
mydatabase = DATABASE()
changeCommand = False
popularCommand = {'cmdCount':0, 'cmdTxt':"stay still"}
robotType = "4leg"

def loadRobotFromFile(robotID):
    brainPath = '../brains/r_' + str(robotID) + '.txt'

    if os.path.isfile(brainPath):
        with open(brainPath,'r') as f:
            ind = pickle.load(f)
            return ind
    else:
        return INDIVIDUAL(0, GENOME_SHAPE)

def announcement(cmdCurrent, currentColor):
    print('-'*70)
    print colored("Type !"+ currentColor[0] +\
        "y if the current robot is following the command ["+\
         cmdCurrent+"].", currentColor)
    print
    print colored("Type !"+ currentColor[0] +\
        "n if the current robot is NOT following the command ["+\
         cmdCurrent+"].", currentColor)
    print
    print colored("Type !command to change the command.", 'cyan')
    print
    # print colored("Next robot is in: " + str(c.evaluationTime*0.05)+" seconds", nextColor)
    print('-'*70)

def updateDatabase(robotType):
    global colorIndex
    global currentColor
    global popularCommand
    
    #get the current time
    currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())

    #get the color that is used for displaying the current robot
    currentColor = validColors[colorIndex % len(validColors)]

    #add a new robot to the robots table and return the id
    robotID = mydatabase.Add_Robot(robotType)

    print("New individual after mutation: ", robotID)

    #add a new entry in the display talble for this robot and the command
    mydatabase.Add_Command_To_Display(robotID, popularCommand['cmdTxt'], currentColor[0],
     currentTime)

    #print an announcment for this robot and a robot comes next
    announcement(popularCommand['cmdTxt'], currentColor)

    #move the color index by one
    colorIndex += 1

    return robotID

def display(newInd, robotID):
    global currentColor

    #set the id based off the 
    newInd.Set_ID(robotID)

    #set the color of this robot
    newInd.Set_Color(currentColor)

    #evaluate this individual
    newInd.Evaluate(False, False)

    #compute the fitness for this robot
    newInd.Compute_Fitness()

    #store the controller of this robot into a file
    newInd.Store()

    del newInd

def compete(pop):
    pop_len = len(pop)

    ind1 =  np.random.randint(pop_len)
    ind2 =  np.random.randint(pop_len)

    if pop_len > 1:
        while ind2 == ind1: 
            ind2 =  np.random.randint(pop_len)

    if pop[ind1]['totalFitness'] > pop[ind2]['totalFitness']: 
        return (ind1, ind2)

    return (ind2, ind1)

def replace(loser, winner):

    mydatabase.Kill_Robot(loser['robotID'])

    newInd = loadRobotFromFile( winner['robotID'])
    newInd.Mutate()

    return newInd


def main(argv):

    generation = 1

    global robotType
    global changeCommand
    global popularCommand


    while True:
        print("G: ", generation)

        #return all the alive individuals
        aliveIndividuals = mydatabase.Fetch_Alive_Robots(robotType)

        print "(Alive individuals: ",
        for ind in aliveIndividuals: print str(ind['robotID']) + ":" + str(ind['totalFitness']),
        print ")"

            #find the most popular command for this new robot
        if(generation % 6 == 0):
            popularCommand = mydatabase.Fetch_Popular_Command()
            # changeCommand = False

        if len(aliveIndividuals) < numAliveIndividuals:

            newInd = INDIVIDUAL(0, GENOME_SHAPE)

            robotID = updateDatabase(robotType)

            robotID = updateDatabase(robotType)

            display(newInd, robotID)

        else:

            (winner, loser) = compete(aliveIndividuals)

            print("winner: ", aliveIndividuals[winner]['robotID'], 
                "loser: ", aliveIndividuals[loser]['robotID'])

            newInd = replace(aliveIndividuals[loser], aliveIndividuals[winner])

            robotID = updateDatabase(robotType)

            display(newInd, robotID)

        generation += 1

        print

        if generation == 100: break

if __name__ == "__main__":
   main(sys.argv[1:])


