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

def load_Robot_From_File(robotID):
    brainPath = '../brains/r_' + str(robotID) + '.txt'

    if os.path.isfile(brainPath):
        with open(brainPath,'r') as f:
            ind = pickle.load(f)
            return ind
    else:
        return INDIVIDUAL(0, GENOME_SHAPE)

def print_Message(cmdCurrent, currentColor):
    print('-'*70)
    print
    print colored("Type !"+ currentColor[0] +\
        "y if the current robot is obeying the command ["+\
         cmdCurrent+"].", currentColor)
    print
    print colored("Type !"+ currentColor[0] +\
        "n if the current robot is NOT obeying the command ["+\
         cmdCurrent+"].", currentColor)
    print
    print colored("Type !"+ currentColor[0] +\
        "l if You LIKE the current robot.", currentColor)
    print
    print colored("Type !"+ currentColor[0] +\
        "d if You DISLIKE the current robot.", currentColor)
    print
    print colored("Type !command to change the current command.", 'cyan')
    print
    # print colored("Next robot is in: " + str(c.evaluationTime*0.05)+" seconds", nextColor)
    print('-'*70)

def update_Database(robotType):
    global popularCommand
    
    #get the current time
    currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())

    #add a new robot to the robots table and return the id
    robotID = mydatabase.Add_Robot(robotType)

    #add a new entry in the display table for this robot and the command
    mydatabase.Add_Command_To_Display(robotID, popularCommand['cmdTxt'], 
        currentColor[0], currentTime)

    mydatabase.Update_Robot_Evaluation(aliveIndividuals[index]['robotID'])

    return robotID

def select_Random_Individual(pop):

    pop_len = len(pop)

    return np.random.randint(pop_len)

def compete_While_Waiting_For(pop, ignoreIndex):

    pop_len = len(pop)

    ind1 =  np.random.randint(pop_len)
    ind2 =  np.random.randint(pop_len)

    while ind1 == ignoreIndex:
        ind1 =  np.random.randint(pop_len)

    if pop_len > 1:
        while ind2 == ind1 or ind2 == ignoreIndex: 
            ind2 =  np.random.randint(pop_len)

    print pop[ind1]
    print pop[ind2]

    return compete_Based_On_Dominance(pop[ind1], pop[ind2])

def compete_Based_On_Dominance(individual1, individual2):

    if dominance(individual1, individual2):
        winner, loser = individual1, individual2

    elif dominance(individual2, individual1):
        winner, loser = individual2, individual1

    else:
        return None

    mydatabase.Kill_Robot(loser['robotID'])

    newInd = load_Robot_From_File(winner['robotID'])

    newInd.Mutate()

    return newInd

def dominance(individual1, individual2):

    notShownMore    = individual1['numEvals'] <= individual2['numEvals']
    likedMore       = individual1['totalLikeability'] > individual2['totalLikeability']
    moreObedient    = individual1['totalFitness'] > individual2['totalFitness']

    if notShownMore and likedMore and moreObedient:
        return True
    else:
        return False

def main(argv):

    generation = 0

    global robotType
    global popularCommand
    global currentColor
    global colorIndex

    while True:
        # print("G: ", generation)

        #get the color that is used for displaying the current robot
        currentColor = validColors[colorIndex % len(validColors)]

        #return all the alive individuals
        aliveIndividuals = mydatabase.Fetch_Alive_Robots(robotType)

        # print "(Alive individuals: ",
        # for ind in aliveIndividuals: 
        #     print str(ind['robotID']) + ":" + str(ind['totalFitness']),
        # print ")"

        #find the most popular command
        if(generation % 6 == 0):
            popularCommand = mydatabase.Fetch_Popular_Command()
            # print(popularCommand)

        if len(aliveIndividuals) < numAliveIndividuals:

            newIndividual = INDIVIDUAL(0, GENOME_SHAPE)

            robotID = update_Database(robotType)

            newIndividual.Set_Color(currentColor)

            #print a message for users on screen
            print_Reward_Message(popularCommand['cmdTxt'], currentColor)

            newIndividual.Evaluate(False, False)

            newIndividual.Wait_For_Me()

            newIndividual.store_Robot_To_File()

        else:

            #select a ranodm one from the list of living robots
            index = select_Random_Individual(aliveIndividuals)

            #load that random individual from a stored file
            randomIndividual = load_Robot_From_File(aliveIndividuals[index]['robotID'])

            #print a message for users on screen
            print_Message(popularCommand['cmdTxt'], currentColor)

            currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())

            #add this random individual to the display table
            mydatabase.Add_Command_To_Display(aliveIndividuals[index]['robotID'],
                popularCommand['cmdTxt'], currentColor[0], currentTime)

            #set the color of this robot
            randomIndividual.Set_Color(currentColor)

            print("Evaluating: ", aliveIndividuals[index]['robotID'])

            #evaluate this individual and show on the screen
            randomIndividual.Evaluate(False, False)

            mydatabase.Update_Robot_Evaluation(aliveIndividuals[index]['robotID'])

            #compete a pair
            newIndividual = compete_While_Waiting_For(aliveIndividuals, index)

            #add this new individual to the robot table
            if newIndividual != None:
                robotID = mydatabase.Add_Robot(robotType)

                newIndividual.Set_ID(robotID)

                #store this individual to a file
                newIndividual.store_Robot_To_File()

            #finish simulating the random individual
            randomIndividual.Wait_For_Me()

            #store that random individual in case
            randomIndividual.store_Robot_To_File()

        generation += 1
        colorIndex += 1

        print

        if generation == 6: break

if __name__ == "__main__":
   main(sys.argv[1:])

