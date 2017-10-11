from pyrosim import PYROSIM
import numpy as np
from copy import deepcopy
import datetime
import sys 
import pickle
import os 
import glob
import argparse
import time

from individual import INDIVIDUAL
from timer import TIMER
import constants as c

sys.path.append('../bots')

from database import DATABASE
from settings import *

MAIN_PATH = 'TPR_Sept'
SUB_POPULATION_SIZE = 5
INJECTION_PERIOD = 60 * 60

colorIndex = 0
currentColor = validColors[colorIndex % len(validColors)]
wordVector = []
currentCommand = {'wordToVec': 1.0, 'cmdTxt': DEFAULT_COMMAND}

db = None
injectionTimer = None
removeInjected = False


def Store_Sensors_To_File(individual, currentTime):
    # get directory
    path = "../" + MAIN_PATH + "/sensors/"+ str(currentTime.year) + "/" + str(currentTime.month)+\
        "/" + str(currentTime.day)
    # print path
    if not os.path.exists(path):
        os.makedirs(path)

    # create file
    currentTime = currentTime.strftime("%Y-%m-%d-%H-%M-%S")
    path += '/robot_' + str(individual.id) + "_" + currentTime + ".dat"
    sensorValues = individual.Get_Raw_Sensors()
    Write_File(path, sensorValues)


def Store_Controller_To_File(individual, robotType):
    # get directory
    path = ".." + MAIN_PATH + "/controllers/"+ robotType
    if not os.path.exists(path):
        os.makedirs(path)

    # get filename and extension
    path += '/robot_' + str(individual.id) + ".dat"
    Write_File(path, individual)


def Load_Controller_From_File(robotID, robotType):
    brainPath = "../" + MAIN_PATH + "controllers/" + robotType + "/robot_" + str(robotID) + ".dat"
    if not os.path.isfile(brainPath): 
        return None
    return Read_File(brainPath)


def Load_From_Diversity_Pool(robotType):
    global removeInjected
    path = "../diversity_pool/" + robotType + "/*.dat"
    brainPaths = list(glob.iglob(path))
    if len(brainPaths) == 0: return None

    randomIndex = np.random.randint(low=0, high=len(brainPaths))
    if not os.path.isfile(brainPaths[randomIndex]): 
        return None

    ind = Read_File(brainPaths[randomIndex])
    print "removeInjected: ", removeInjected
    if removeInjected:
        Remove_File(brainPaths[randomIndex])
    return ind


def Read_File(filePath):
    try:
        f = open(filePath,'r')
        individual = pickle.load(f)
        f.close
        print "Successful loading ", filePath
        return individual
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "Failed loading ", filePath 
        return None


def Write_File(filePath, data):
    try:
        f = open(filePath,'wb')
        pickle.dump(data, f)
        f.close
        print "Successful writing ", filePath
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "Failed writing ", filePath 


def Remove_File(filePath):
    try:
        os.remove(filePath)
        print "Successfully removed the injected robot from the diversity pool.."
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "Was not able to remove the injected robot from the diversity pool.."


def Select_Individual(pop):
    print 'Select an individual to display...'
    robotID = db.Minimum_Evaluation(currentCommand['cmdTxt'])
    if robotID > 0 :
        return next((item for item in pop if item['robotID'] == robotID), None)
    else:
        return pop[np.random.randint(len(pop))]


def Compete_While_Waiting_For(pop, ignoreID):
    pop_len = len(pop)
    if pop_len <= 2: return None
    while True:
        ind1 = np.random.randint(len(pop))
        if pop[ind1]['robotID'] != ignoreID:
            break

    while True:
        ind2 = np.random.randint(len(pop))
        if ind2 != ind1 and pop[ind2]['robotID'] != ignoreID:
            break
    print "Competing controllers: ", pop[ind1]['robotID'], " and " , pop[ind2]['robotID']
    print pop[ind1]
    print pop[ind2]

    # both have shown to the crowd.
    if pop[ind1]['numEvals'] != 0 and pop[ind2]['numEvals'] != 0:
        return Compete_Based_On_Dominance(pop[ind1], pop[ind2])
    # else.
    else:
        return None


def Compete_Based_On_Dominance(lh_individual, rh_individual):
    winner, loser = lh_individual, rh_individual
    if Dominance(rh_individual, lh_individual):
        winner, loser = rh_individual, lh_individual
    elif not Dominance(lh_individual, rh_individual):
        return None

    print "Winner is: ", winner['robotID']
    print "Loser is: ", loser['robotID']
    print "Killing the loser..."

    db.Kill_Robot(loser['robotID'])

    winnerIndividual = Load_Controller_From_File(winner['robotID'], winner['type'])

    if winnerIndividual is None:
        print 'Not able loading it from the file...Killing robot ', winner['robotID']
        db.Kill_Robot(winner['robotID'])
        print 'Replacing with a random one from the same type.'
        mutatedOne = INDIVIDUAL(0, winner['type'])

    else:
        mutatedOne = Create_Mutation(winnerIndividual)
    Add_New_Robot(mutatedOne, winner['robotID'])


def Create_Mutation(individual):
    newIndividual = deepcopy(individual)
    newIndividual.Mutate()
    print 'Mutate the brain or the body of robot: ', newIndividual.id
    return newIndividual


def Dominance(lh_individual, rh_individual):
    notShownMore = lh_individual['numEvals'] <= rh_individual['numEvals']
    if (lh_individual['sumYes']+lh_individual['sumNo']) == 0:
        lh_obedience = 0
    else:
        lh_obedience = float(lh_individual['sumYes']-lh_individual['sumNo'])/\
                       (lh_individual['sumYes']+lh_individual['sumNo'])

    if (rh_individual['sumYes']+rh_individual['sumNo']) == 0:
        rh_obedience = 0
    else:
        rh_obedience = float(rh_individual['sumYes']-rh_individual['sumNo'])/\
                       (rh_individual['sumYes']+rh_individual['sumNo'])
    moreObedient = lh_obedience > rh_obedience
    return notShownMore and moreObedient


def Add_New_Robot(newIndividual, parentID=0):
    robotID = db.Add_To_Robot_Table(newIndividual.robotType, parentID)
    print 'New robot added... type: ', newIndividual.robotType, ' and ID:',robotID, 'parentID: ', parentID
    newIndividual.Set_ID(robotID)
    Store_Controller_To_File(newIndividual, newIndividual.robotType)
    return robotID


def Initialize_Global_Population():
    print "\n\n"
    print "Initializing the global population..."
    for robotType in validRobots:
        for i in range(0, SUB_POPULATION_SIZE):
            newIndividual = Load_From_Diversity_Pool(robotType)
            if newIndividual is None:
                newIndividual = INDIVIDUAL(0, robotType)
            Add_New_Robot(newIndividual)
    print '\n'


def Steady_State():
    global injectionTimer
    global currentCommand
    global currentColor
    global colorIndex
    global wordVector

    generation = 1

    while True:
        print "Generation: ", generation
        aliveIndividuals = db.Fetch_Alive_Robots("all")
        print "Num of alive individuals: ", len(aliveIndividuals)

        if len(aliveIndividuals) <= 2:
            print 'Not enough individuals in the population. Run with --initPopulation flag.'
            print 'ctrl + c to break from this program...sorry I have no better way to kill you..'
            break

        if injectionTimer.Time_Elapsed():
            print "Time to inject a new individual.."
            injectionTimer.Reset()

            min_Evaluated_Robot = min(aliveIndividuals, key=lambda x:x['numEvals'])
            print "To be killed to make space fot the incoming robot :(", min_Evaluated_Robot

            injectionType = validRobots[np.random.randint(0, len(validRobots))]
            toBe_Injected = Load_From_Diversity_Pool(injectionType)

            if toBe_Injected is None:
                toBe_Injected = INDIVIDUAL(0, injectionType)

            robotID = Add_New_Robot(toBe_Injected)
            db.Kill_Robot(min_Evaluated_Robot['robotID'])

            aliveIndividuals = db.Fetch_Alive_Robots("all")

            toBe_Displayed = next((item for item in aliveIndividuals if item['robotID'] == robotID), None)
            if toBe_Displayed is None: continue

            currentColor = specialColor

        else:
            # find a controller that was not evaluated under the current command
            toBe_Displayed = Select_Individual(aliveIndividuals)
            currentColor = validColors[colorIndex % len(validColors)]

        # print toBe_Displayed

        robotID, robotType = toBe_Displayed['robotID'], toBe_Displayed['type']
        randomIndividual = Load_Controller_From_File(robotID, robotType)
        
        if randomIndividual is None:
            print "Could not load robot ", robotID, " with type: ", robotType
            db.Kill_Robot(robotID)
            continue

        tempCurrentCommand = db.Get_Current_Command()
        if tempCurrentCommand is not None:
            currentCommand = tempCurrentCommand

        wordVector = c.NUM_BIAS_NEURONS*[1.0] + [currentCommand['wordToVec']]
        currentTime = datetime.datetime.now()

        db.Add_Command_To_Display_Table(robotID, currentCommand['cmdTxt'], currentColor[0], currentTime)

        print "Displaying robot: ", toBe_Displayed
        print "Displaying color: ", currentColor
        print "Acting command: ", currentCommand
        print "Current time: ", currentTime
        print "wordVector: ", wordVector
        
        randomIndividual.Set_Color(currentColor)
        randomIndividual.Start_Evaluate(False, False, wordVector)
        
        Compete_While_Waiting_For(aliveIndividuals, robotID)
        randomIndividual.Wait_For_Me()
        Store_Sensors_To_File(randomIndividual, currentTime)

        colorIndex += 1
        print
        generation += 1
        print


def main(args):
    global db
    global removeInjected
    global injectionTimer

    db = DATABASE()

    initPopulation = args.initPopulation
    removeInjected = args.removeInjected

    if initPopulation:
        Initialize_Global_Population()

    injectionTimer = TIMER(INJECTION_PERIOD)
    Steady_State()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Steady state Version 5.')
    
    parser.add_argument('--initPopulation', action='store_true',
                        help='initialize the population.')

    parser.add_argument('--removeInjected', action='store_true',
                        help='remove an injected individual from the diversity pool.')

    args = parser.parse_args()

    main(args)



