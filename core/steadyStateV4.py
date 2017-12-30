from pyrosim import PYROSIM
import numpy as np
from copy import deepcopy
import datetime
import sys 
import pickle
import os 
import glob
from keras.models import load_model
import pygame
import argparse
from threading import Thread, Event
import time

from individual import INDIVIDUAL
from timer import TIMER
import constants as c

sys.path.append('../bots')

from database import DATABASE
from settings import *
from pygameWrapper import PYGAMEWRAPPER

SUB_POPULATION_SIZE = 5
REWARD_WINDOW_W = 900
REWARD_WINDOW_H = 280
FONT_SIZE = 23
INJECTION_PERIOD = 60 * 60

colorIndex = 0
currentColor = validColors[colorIndex % len(validColors)]
wordVector = []
currentCommand = {'wordToVec': 1.0, 'cmdTxt': DEFAULT_COMMAND}

db = None
injectionTimer = None
removeInjected = False
window = PYGAMEWRAPPER(width=REWARD_WINDOW_W, height=REWARD_WINDOW_H, 
                       title="Reinforcements", fontSize=FONT_SIZE)


def Store_Sensors_To_File(individual, currentTime):
    """
    store sensor data for an evaluation to a file
    :param individual: INDIVIDUAL
    :param currentTime: time
    :return: None
    """
    # get directory
    path = "../sensors/"+ str(currentTime.year) + "/" + str(currentTime.month) + \
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
    """
    store controller data of a robot to a file
    :param individual: INDIVIDUAL
    :param robotType: string
    :return: None
    """
    # get directory
    path = "../controllers/"+ robotType
    if not os.path.exists(path):
        os.makedirs(path)

    # get filename and extension
    path += '/robot_' + str(individual.id) + ".dat"
    Write_File(path, individual)


def Load_Controller_From_File(robotID, robotType):
    """
    load a robot controller from a file
    :param robotID: int
    :param robotType: string
    :return: INDIVIDUAL
    """

    brainPath = "../controllers/" + robotType + "/robot_" + str(robotID) + ".dat"
    if not os.path.isfile(brainPath): 
        return None

    return Read_File(brainPath)


def Load_From_Diversity_Pool(robotType):
    """
    add a random robot controller from the diversity pool and remove it from that pool
    :param robotType: string
    :return: INDIVIDUAL
    """
    global removeInjected

    path = "../diversity_pool/" + robotType + "/*.dat"
    brainPaths = list(glob.iglob(path))
    if len(brainPaths) == 0:
        return None

    randomIndex = np.random.randint(low=0, high=len(brainPaths))
    if not os.path.isfile(brainPaths[randomIndex]): 
        return None

    ind = Read_File(brainPaths[randomIndex])

    print "removeInjected: ", removeInjected
    if removeInjected:
        Remove_File(brainPaths[randomIndex])

    return ind


def Read_File(filePath):
    """
    read a robot controller given its path
    :param filePath: string
    :return: INDIVIDUAL
    """

    try:
        f = open(filePath, 'r')
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
    """
    write a data into a file
    :param filePath: string
    :param data: object
    :return:
    """
    try:
        f = open(filePath, 'wb')
        pickle.dump(data, f)
        f.close
        print "Successful writing ", filePath

    except KeyboardInterrupt:
        sys.exit()

    except:
        print "Failed writing ", filePath 


def Remove_File(filePath):
    """
    delete a file given its path
    :param filePath: string
    :return: None
    """
    try:
        os.remove(filePath)
        print "Successfully removed the injected robot from the diversity pool.."
    
    except KeyboardInterrupt:
        sys.exit()

    except:
        print "Was not able to remove the injected robot from the diversity pool.."


def Draw_Reinforcment_Window(run_event):
    """
    dispay a window that prompts users to provide reinforcement to the displaying robots
    :param run_event:
    :return:
    """
    global currentCommand
    global currentColor
    global injectionTimer
    WSPACE = 5
    
    while run_event.is_set():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.Quit()

        window.Wipe()

        cmdTxt = currentCommand['cmdTxt']

        myy = 10
        window.Draw_Text("New here? Type", x=700, y=myy, fontSize=FONT_SIZE)
        window.Draw_Text("?", x=window.text_x+window.text_width+WSPACE, y=myy-5, color='BROWN',
                        fontSize=FONT_SIZE+8)

        myy += 40
        window.Draw_Text("Type", x=10, y=myy, fontSize=FONT_SIZE)
        window.Draw_Text("!" + currentColor[0] + "y", x=window.text_x+window.text_width+WSPACE,
         y=myy, color=currentColor.upper(), fontSize=FONT_SIZE)

        window.Draw_Text("if Yes, the [" + currentColor[0].upper() + "]" + currentColor[1:] +
                         " robot is obeying the command", x=window.text_x+window.text_width+WSPACE, y=myy,
                          fontSize=FONT_SIZE)

        window.Draw_Text("[" + cmdTxt + "].", x=window.text_x+window.text_width+WSPACE,
                        y=myy, color='BROWN', fontSize=FONT_SIZE)

        myy += 40
        window.Draw_Text("Type", x=10, y=myy, fontSize=FONT_SIZE)
        window.Draw_Text("!" + currentColor[0] + "n", x=window.text_x+window.text_width+WSPACE,
                        y=myy, color=currentColor.upper(), fontSize=FONT_SIZE)

        window.Draw_Text("if No, the ["+ currentColor[0].upper() + "]" + currentColor[1:] +
                         " robot is [N]ot obeying the command", x=window.text_x+window.text_width+WSPACE, y=myy,
                          fontSize=FONT_SIZE)

        window.Draw_Text("["+ cmdTxt + "].", x=window.text_x+window.text_width+WSPACE,
                        y=myy, color='BROWN', fontSize=FONT_SIZE)

        myy += 40
        window.Draw_Text("Type", x=10, y=myy, fontSize=FONT_SIZE)

        window.Draw_Text("!" + currentColor[0] + "l ", x=window.text_x+window.text_width+WSPACE,
                        y=myy, color=currentColor.upper(), fontSize=FONT_SIZE)

        window.Draw_Text("if you [L]ike the [" + currentColor[0].upper() + "]" +
                         currentColor[1:] + " robot.", x=window.text_x+window.text_width+WSPACE, y=myy, fontSize=FONT_SIZE)
        
        myy += 40
        window.Draw_Text("Type", x=10, y=myy,fontSize=FONT_SIZE)
        window.Draw_Text("!"+ currentColor[0] + "d", x=window.text_x+window.text_width+WSPACE,
                        y=myy, color=currentColor.upper(), fontSize=FONT_SIZE)

        window.Draw_Text("if you [D]islike the [" + currentColor[0].upper() + "]" +
                        currentColor[1:] + " robot.", x=window.text_x+window.text_width+WSPACE, y=myy, fontSize=FONT_SIZE)

        myy += 60
        rtime = injectionTimer.Time_Remaining()
        if rtime < 0: rtime = 0
        minute, second = divmod(rtime, 60)
        hour, minute = divmod(minute, 60)
        rtime = "%02dm:%02ds"%(minute, second)

        window.Draw_Rect(10, myy, 420, 30, color='TAN')
        # window.Draw_Text("The next silver robot will be born into the population in " + rtime,\
        #  x=10, y=myy, color='BLACK', fontSize=FONT_SIZE) 

        window.Draw_Text("The next silver robot will be displayed in " + rtime,
                        x=10, y=myy, color='BLACK', fontSize=FONT_SIZE)

        window.Draw_Text("Need help? Type", x=600, y=myy, fontSize=FONT_SIZE)
        window.Draw_Text("?reinforcement", x=window.text_x+window.text_width+WSPACE, y=myy, color='BROWN', fontSize=FONT_SIZE)
        window.Refresh()


def Select_Random_Individual(popSize):
    """
    select a random index from the population of robots
    :param popSize: int
    :return: int
    """
    return np.random.randint(popSize)


def Compete_While_Waiting_For(pop, ignoreID):
    """
    choose two random robots different from the one is being displayed (ingnoreID) and let them compete
    :param pop: List
    :param ignoreID: int
    :return: None
    """
    pop_len = len(pop)
    if pop_len <= 2:
        return None

    # find a random robot ignoring igonreID
    while True:
        ind1 = Select_Random_Individual(len(pop))
        if pop[ind1]['robotID'] != ignoreID:
            break

    # find a random robot ignoring igonreID and the previous random robot
    while True:
        ind2 = Select_Random_Individual(len(pop))
        if ind2 != ind1 and pop[ind2]['robotID'] != ignoreID:
            break
    print "Competing controllers: ", pop[ind1]['robotID'], " and ", pop[ind2]['robotID']
    print pop[ind1]
    print pop[ind2]

    # if both have shown to the crowd then compete based on dominance
    if pop[ind1]['numEvals'] != 0 and pop[ind2]['numEvals'] != 0:
        return Compete_Based_On_Dominance(pop[ind1], pop[ind2])

    # only one has shown to the crowd.
    else:
        return None


def Compete_Based_On_Dominance(lh_individual, rh_individual):
    """
    the two robots compete based on dominance.
    the one is more fit kills the other one and reproduce
    :param lh_individual: dict
    :param rh_individual: dict
    :return: None
    """
    winner, loser = lh_individual, rh_individual
    if Dominance(rh_individual, lh_individual):
        winner, loser = rh_individual, lh_individual
    elif not Dominance(lh_individual, rh_individual):
        return None

    print "Winner is: ", winner['robotID']
    print "Loser is: ", loser['robotID']
    print "Killing the loser..."

    # kill the loser robot
    db.Kill_Robot(loser['robotID'])

    # load the winning robot from the file
    winnerIndividual = Load_Controller_From_File(winner['robotID'], winner['type'])

    # create a mutated version of the winning robot
    if winnerIndividual is None:
        print 'Not able loading it from the file...Killing robot ', winner['robotID']
        db.Kill_Robot(winner['robotID'])
        print 'Replacing with a random one from the same type.'
        mutatedOne = INDIVIDUAL(0, winner['type'])

    else:
        mutatedOne = Create_Mutation(winnerIndividual)
    # add the new robot to the primary population
    Add_New_Robot(mutatedOne, winner['robotID'])


def Create_Mutation(individual):
    """
    create a mutated version of a given robot and return it
    :param individual: INDIVIDUAL
    :return: INDIVIDUAL
    """
    newIndividual = deepcopy(individual)
    newIndividual.Mutate()
    print 'Mutate the brain of robot: ', newIndividual.id
    return newIndividual


def Dominance(lh_individual, rh_individual):
    """
    compare the two robots with each other and return tru if the first one is more fit
    :param lh_individual: dict
    :param rh_individual: dict
    :return: Boolean
    """
    notShownMore = lh_individual['numEvals'] <= rh_individual['numEvals']
    likedMore = (lh_individual['sumLike']-lh_individual['sumDislike']) > (rh_individual['sumLike']-rh_individual['sumDislike'])
    moreObedient = (lh_individual['sumYes']-lh_individual['sumNo']) > (rh_individual['sumYes']-rh_individual['sumNo'])
    return notShownMore and likedMore and moreObedient


def Add_New_Robot(newIndividual, parentID=0):
    """
    add a new robot to the primary population and return its id
    :param newIndividual: INDIVIDUAL
    :param parentID: int
    :return: int
    """
    robotID = db.Add_To_Robot_Table(newIndividual.robotType, parentID)
    print 'New robot added... type: ', newIndividual.robotType, ' and ID:', robotID, 'parentID: ', parentID
    newIndividual.Set_ID(robotID)
    Store_Controller_To_File(newIndividual, newIndividual.robotType)
    return robotID


def Initialize_Global_Population():
    """
    initialize the primary population of robots
    :return: None
    """
    print "\n\n"
    print "Initializing the global population..."
    for robotType in validRobots:
        for i in range(0, SUB_POPULATION_SIZE):
            newIndividual = Load_From_Diversity_Pool(robotType)
            if newIndividual is None:
                newIndividual = INDIVIDUAL(0, robotType)
            Add_New_Robot(newIndividual)
    print '\n'


def Steady_State(run_event):
    """
    master program that selects a robot to be displayed and choose robots to compete
    :param run_event:
    :return: None
    """
    global injectionTimer
    global currentCommand
    global currentColor
    global colorIndex
    global wordVector
    global robotInfo

    generation = 1

    while run_event.is_set():

        print "Generation: ", generation
        # find all the alive robots in the primary population
        aliveIndividuals = db.Fetch_Alive_Robots("all")

        print "Num of alive individuals: ", len(aliveIndividuals)

        if len(aliveIndividuals) <= 2:
            print 'Not enough individuals in the population. Run with --initPopulation flag.'
            run_event.clear()
            print 'ctrl + c to break from this program...sorry I have no better way to kill you..'
            break

        # time to inject a robot from secondary population to primary one
        if injectionTimer.Time_Elapsed():

            print 'Time to inject a new individual..'
            injectionTimer.Reset()

            # find the robot with minimum number of evaluations from the primary population
            min_Evaluated_Robot = min(aliveIndividuals, key=lambda x: x['numEvals'])
            print "To be killed to make space fot the incoming robot :(", min_Evaluated_Robot

            # load a random robot from the secondary population
            injectionType = validRobots[np.random.randint(0, len(validRobots))]
            toBe_Injected = Load_From_Diversity_Pool(injectionType)

            if toBe_Injected is None:
                toBe_Injected = INDIVIDUAL(0, injectionType)

            # add the incoming robot to the primary population
            robotID = Add_New_Robot(toBe_Injected)

            # kill a robot from the primary population
            db.Kill_Robot(min_Evaluated_Robot['robotID'])

            aliveIndividuals = db.Fetch_Alive_Robots("all")

            # find the robot that has to displayed
            toBe_Displayed = next((item for item in aliveIndividuals if item['robotID'] == robotID), None)
            if toBe_Displayed is None:
                continue

            # assign the color to the special color
            currentColor = specialColor

        # not time for injection
        else:
            # choose a random robot from the primary population of robots to be displayed
            toBe_Displayed_Index = Select_Random_Individual(len(aliveIndividuals))
            toBe_Displayed = aliveIndividuals[toBe_Displayed_Index]
            currentColor = validColors[colorIndex % len(validColors)]

        # print toBe_Displayed

        robotID = toBe_Displayed['robotID']
        robotType = toBe_Displayed['type']
        randomIndividual = Load_Controller_From_File(robotID, robotType)
        
        if randomIndividual is None:
            print "Could not load robot ", robotID, " with type: ", robotType
            db.Kill_Robot(robotID)
            continue

        # find the next candidate command
        tempCurrentCommand = db.Get_Current_Command()
        if tempCurrentCommand is not None:
            currentCommand = tempCurrentCommand

        wordVector = c.NUM_BIAS_NEURONS*[1.0] + [currentCommand['wordToVec']]
        currentTime = datetime.datetime.now()

        # add a new row to the display table
        db.Add_Command_To_Display_Table(robotID, currentCommand['cmdTxt'], currentColor[0], currentTime)

        print "Displaying robot: ", toBe_Displayed
        print "Displaying color: ", currentColor
        print "Acting command: ", currentCommand
        print "Current time: ", currentTime
        print "wordVector: ", wordVector

        # set the color and start evaluating the chosen robot
        randomIndividual.Set_Color(currentColor)
        randomIndividual.Start_Evaluate(False, False, wordVector)

        # let two random robots compete while evaluating the chosen robot
        Compete_While_Waiting_For(aliveIndividuals, robotID)
        randomIndividual.Wait_For_Me()

        # store the sensor data of the displayed robot
        Store_Sensors_To_File(randomIndividual, currentTime)

        colorIndex += 1
        print

        generation += 1
        print

def main(args):
    """

    :param args:
    :return:
    """

    global db
    global removeInjected
    global injectionTimer

    db = DATABASE()

    initPopulation = args.initPopulation
    removeInjected = args.removeInjected

    # if initPopulation:
    #     Initialize_Global_Population()

    injectionTimer = TIMER(INJECTION_PERIOD)

    run_event = Event()
    run_event.set()

    dthread = Thread(target=Draw_Reinforcment_Window, args=[run_event])
    dthread.daemon = True

    sthread = Thread(target=Steady_State, args=[run_event])
    sthread.daemon = True

    dthread.start()
    sthread.start()

    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print('Closing both windows with ctrl+c...')
        run_event.clear()
        dthread.join()
        sthread.join()
        print('Closed both threads successfully... Have a good day:)')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Steady state Version 4.')
    parser.add_argument('--initPopulation', action='store_true', help='initialize the population.')
    parser.add_argument('--removeInjected', action='store_true', help=
                        'remove an injected individual from the diversity pool.')
    args = parser.parse_args()
    main(args)



