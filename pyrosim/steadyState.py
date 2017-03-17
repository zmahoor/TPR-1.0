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

robotType = "4leg"

def loadRobotFromFile(robotID):
    brainPath = '../brains/r_' + str(robotID) + '.txt'

    if os.path.isfile(brainPath):
        with open(brainPath,'r') as f:
            ind = pickle.load(f)
            return ind
    else:
        return INDIVIDUAL(0, GENOME_SHAPE)

def announcement(cmdCurrent, currentColor, nextColor):

    print('-'*70)
    print colored("Type !"+ currentColor[0] +\
        "y if the current robot is following the command ["+\
         cmdCurrent+"].", currentColor)
    print
    print colored("Type !"+ currentColor[0] +\
        "n if the current robot is NOT following the command ["+\
         cmdCurrent+"].", currentColor)
    print
    print colored("Type !"+ nextColor[0] +\
        "command to issue a command to the next robot.", nextColor)
    print('-'*70)

def display(newInd, robotType):
    global colorIndex
    global currentColor

    #store the robot's info in the database 
    currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    
    robotID = mydatabase.Add_Robot(robotType)
    print("New individual with mutation: ", robotID)
    (cmdNum, cmdCurrent) = mydatabase.Fetch_Command(currentColor)

    currentColor = validColors[colorIndex % len(validColors)]
    colorIndex += 1
    nextColor = validColors[colorIndex % len(validColors)]

    mydatabase.Add_Display(robotID, cmdCurrent, currentColor[0], currentTime)

    announcement(cmdCurrent, currentColor, nextColor)

    # display an individual and store the controller into a file
    newInd.Set_ID(robotID)
    newInd.Set_Color(currentColor)
    newInd.Evaluate(False, False)
    newInd.Compute_Fitness()
    newInd.Store()

    del newInd

    mydatabase.Update_Total_Fitness(robotID)

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

    while True:
        print("Generation: ", generation)

        aliveIndividuals = mydatabase.Fetch_Alive_Robots(robotType)
        print("Number of alive individuals: ", len(aliveIndividuals))
        if len(aliveIndividuals) < numAliveIndividuals:

            newInd = INDIVIDUAL(0, GENOME_SHAPE)

            display(newInd, robotType)

        else:

            (winner, loser) = compete(aliveIndividuals)
            print("winner, loser: ", aliveIndividuals[winner]['robotID'], aliveIndividuals[loser]['robotID'])
            newInd = replace(aliveIndividuals[loser], aliveIndividuals[winner])

            display(newInd, robotType)

        generation += 1

        print

        if generation == 2: break

if __name__ == "__main__":
   main(sys.argv[1:])


