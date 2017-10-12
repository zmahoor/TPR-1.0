from pyrosim import PYROSIM
import numpy as np
from copy import deepcopy
import datetime
import sys 
import pickle
import os 
import glob
import pygame
import argparse

from individual import INDIVIDUAL
from timer import TIMER
import constants as c

sys.path.append('../bots')

from database import DATABASE
from settings import *
from pygameWrapper import PYGAMEWRAPPER

SUB_POPULATION_SIZE = 5
REWARD_WINDOW_W     = 900
REWARD_WINDOW_H     = 280
FONT_SIZE           = 23
INJECTION_PERIOD    = 60 * 60

colorIndex     = 0
currentColor   = validColors[colorIndex % len(validColors)]
currentCommand = {}
wordVector     = []

window = None
db     = None
injectionTimer = None
removeInjected = False

def Store_Sensors_To_File(individual, currentTime):

    # get directory
    path = "../sensors/"+ str(currentTime.year) + "/" + str(currentTime.month)+\
        "/" + str(currentTime.day)
    # print path
    if not os.path.exists(path):
        os.makedirs(path)

    # create file
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    path += '/robot_' + str(individual.id) + "_" + currentTime + ".dat"
    sensorValues = individual.Get_Raw_Sensors()
    Write_File(path, sensorValues)

def Store_Controller_To_File(individual, robotType):

    # get directory
    path = "../controllers/"+ robotType
    if not os.path.exists(path):
        os.makedirs(path)

    # get filename and extension
    path += '/robot_' + str(individual.id) + ".dat"
    Write_File(path, individual)

def Load_Controller_From_File(robotID, robotType):

    brainPath = "../controllers/"+ robotType +"/robot_"+ str(robotID) +".dat" 

    if not os.path.isfile(brainPath): 
        return None

    return Read_File(brainPath)

def Load_From_Diversity_Pool(robotType):

    global removeInjected

    path = "../diversity_pool/"+ robotType + "/*.dat" 

    brainPaths = list(glob.iglob(path))

    if len(brainPaths) == 0: return None

    randomIndex = np.random.randint(low=0, high=len(brainPaths))
    if not os.path.isfile(brainPaths[randomIndex]): 
        return None

    ind = Read_File(brainPaths[randomIndex])

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

def Draw_Reinforcment_Window():

    global currentCommand
    global currentColor
    global window

    WSPACE = 5
    window.Wipe()

    cmdTxt = currentCommand['cmdTxt']

    myy = 10

    window.Draw_Text("New here? Type", x= 10, y=myy)
    window.Draw_Text("?", x=window.text_x+window.text_width+WSPACE, y=myy, color='BROWN')

    myy += 40
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "y", x=window.text_x+window.text_width+WSPACE,\
     y=myy, color=currentColor.upper())

    window.Draw_Text("if the ["+ currentColor[0].upper() + "]"+ currentColor[1:]+\
     " robot is obeying the command", x=window.text_x+window.text_width+WSPACE, y=myy)

    window.Draw_Text("["+ cmdTxt +"].", x=window.text_x+window.text_width+WSPACE, y=myy, color='BROWN')

    myy += 40
    window.Draw_Text("Type", x= 10, y= myy)
    window.Draw_Text("!"+ currentColor[0] + "n", x=window.text_x+window.text_width+WSPACE,\
     y=myy, color=currentColor.upper())

    window.Draw_Text("if the ["+ currentColor[0].upper() + "]"+ currentColor[1:]+\
     " robot is [N]ot obeying the command", x=window.text_x+window.text_width+WSPACE, y=myy)

    window.Draw_Text("["+ cmdTxt +"].", x= window.text_x+window.text_width+WSPACE, y=myy, color='BROWN')

    myy += 40
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "l ", x=window.text_x+window.text_width+WSPACE,\
     y=myy, color=currentColor.upper())
    window.Draw_Text("if you [L]ike the ["+ currentColor[0].upper() + "]"+\
        currentColor[1:]+ " robot." , x=window.text_x+window.text_width+WSPACE, y=myy)
    
    myy += 40
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "d", x=window.text_x+window.text_width+WSPACE,\
     y=myy, color=currentColor.upper())

    window.Draw_Text("if you [D]islike the ["+ currentColor[0].upper() + "]"+\
     currentColor[1:]+ " robot." , x=window.text_x+window.text_width+WSPACE, y=myy)

    myy += 60

    minute, second = divmod(injectionTimer.Time_Remaining(), 60)
    hour, minute   = divmod(minute, 60)
    rtime = "%d:%02d:%2d"%(hour, minute, second)

    window.Draw_Rect(10, myy, 320, 30 , color = 'TAN')
    window.Draw_Text("A new robot will be born in " + rtime, x=10, y=myy, color='BROWN') 

    window.Draw_Text("Need help? Type", x= 640, y=myy) 
    window.Draw_Text("?rewards", x=window.text_x+window.text_width+WSPACE, y=myy, color='BROWN')

    window.Refresh()

def Select_Random_Individual(popSize):
    return np.random.randint(popSize)

def Compete_While_Waiting_For(pop, ignoreID):

    pop_len = len(pop)
    if (pop_len <= 2) : 
        return None

    while True:
        ind1 = Select_Random_Individual(len(pop))
        if pop[ind1]['robotID'] != ignoreID:
            break

    while True:
        ind2 = Select_Random_Individual(len(pop))
        if ind2 != ind1 and pop[ind2]['robotID'] != ignoreID:
            break
    print "Competing controllers: ", pop[ind1]['robotID'], " and " , pop[ind2]['robotID']
    print pop[ind1]
    print pop[ind2]

    if pop[ind1]['numEvals'] != 0 and pop[ind2]['numEvals'] != 0:
        return Compete_Based_On_Dominance(pop[ind1], pop[ind2])

    else:
        return None

def Compete_Based_On_Dominance(individual1, individual2):

    winner, loser = individual1, individual2
    if Dominance(individual2, individual1):
        winner, loser = individual2, individual1
    elif not Dominance(individual1, individual2):
        return None

    print "Winner is: ", winner['robotID'], " loser is: ", loser['robotID']
    print "Killing the loser...", loser['robotID']

    db.Kill_Robot(loser['robotID'])

    winnerIndividual = Load_Controller_From_File(winner['robotID'], winner['type'])
    if winnerIndividual == None:  
        db.Kill_Robot(winner['robotID'])
    
    mutatedOne = Create_Mutation(winnerIndividual)

    return mutatedOne

def Create_Mutation(individual):

    if individual == None:
        return None

    else:
        newIndividual = deepcopy(individual)
        newIndividual.Mutate()
        print 'Mutate the brain of robot: ', newIndividual.id

        return newIndividual

def Dominance(individual1, individual2):

    notShownMore    = individual1['numEvals'] <= individual2['numEvals']
    likedMore       = individual1['totalLikeability'] > individual2['totalLikeability']
    moreObedient    = individual1['totalFitness'] > individual2['totalFitness']
    return notShownMore and likedMore and moreObedient

def Add_New_Robot(newIndividual):

    robotID = db.Add_To_Robot_Table(newIndividual.robotType)

    print 'New robot added... type: ', newIndividual.robotType, ' and ID:', robotID
    newIndividual.Set_ID(robotID)
    Store_Controller_To_File(newIndividual, newIndividual.robotType)

    return robotID

def Initialize_Sub_Population(numToBeFilled, robotType):

    print 'Empty slots in sub population of ', robotType, " is: ", numToBeFilled
    while numToBeFilled > 0 :

        newIndividual = Load_From_Diversity_Pool(robotType)
        if newIndividual == None:
            newIndividual = INDIVIDUAL(0, robotType)
        Add_New_Robot(newIndividual)

        numToBeFilled -= 1
        
    print '\n'

def Initialize_Global_Population():

    print "\n\n"
    print "Initializing the global population..."

    aliveIndividuals = db.Fetch_Alive_Robots("all")

    print "Num of alive individuals: ", len(aliveIndividuals)
    print '\n'

    for rtype in validRobots:

        count = 0
        for robot in aliveIndividuals: 
            if robot['type'] == rtype:
                count += 1 

        print 'Create: ', SUB_POPULATION_SIZE-count, ' new individuals from type; ', rtype

        if count< SUB_POPULATION_SIZE: 
            Initialize_Sub_Population(SUB_POPULATION_SIZE-count, rtype)
    print '\n'

def Steady_State():

    global injectionTimer
    global currentCommand
    global currentColor
    global colorIndex
    global wordVector
    global db

    aliveIndividuals = db.fetch_alive_robots("all")

    print "Num of alive individuals: ", len(aliveIndividuals)
    assert len(aliveIndividuals) > 2, 'Not enough individuals in the population. Run with --initPopulation flag.'

    if injectionTimer.Time_Elapsed():

        print 'Time to inject a new individual..'
        injectionTimer.Reset()

        min_Evaluated_Robot = min(aliveIndividuals, key=lambda x:x['numEvals'])
        print "To be killed to make space fot the incoming robot :(", min_Evaluated_Robot

        injectionType = validRobots[np.random.randint(0, len(validRobots))]
        toBe_Injected = Load_From_Diversity_Pool(injectionType)

        if toBe_Injected == None:
            toBe_Injected = INDIVIDUAL(0, randomType)

        robotID = Add_New_Robot(toBe_Injected)
        db.kill_robot(min_Evaluated_Robot['robotID'])

        aliveIndividuals = db.fetch_alive_robots("all")

        toBe_Displayed = next((item for item in aliveIndividuals if item['robotID'] == robotID), None)

        if toBe_Displayed == None: return

    else:
        toBe_Displayed_Index = Select_Random_Individual(len(aliveIndividuals))
        toBe_Displayed = aliveIndividuals[toBe_Displayed_Index]

    robotID   = toBe_Displayed['robotID']
    robotType = toBe_Displayed['type']
    randomIndividual = Load_Controller_From_File(robotID, robotType)
        
    if randomIndividual == None:
        print "Could not load robot ", robotID, " with type: ", robotType
        db.kill_robot(robotID)
        return

    currentColor   = validColors[colorIndex % len(validColors)]
    currentTime    = datetime.datetime.now()
    currentCommand = db.get_current_command()

    if currentCommand == None or currentCommand == ():
        currentCommand = {'wordToVec': 1.0, 'cmdTxt': DEFAULT_COMMAND}

    wordVector     = c.NUM_BIAS_NEURONS*[1.0] + [currentCommand['wordToVec']]

    Draw_Reinforcment_Window()

    db.add_command_to_display_table(robotID, currentCommand['cmdTxt'], currentColor[0], currentTime)

    print "Displaying robot ", randomIndividual.id, ". type: ", randomIndividual.robotType,\
     ", with color: ", currentColor, " and current command: ", currentCommand['cmdTxt'],\
     " and current time: ", currentTime
    
    randomIndividual.Set_Color(currentColor)
    randomIndividual.Start_Evaluate(False, False, wordVector)

    newIndividual = Compete_While_Waiting_For(aliveIndividuals, robotID)
    if newIndividual != None:
        Add_New_Robot(newIndividual)

    randomIndividual.Wait_For_Me()

    Store_Sensors_To_File(randomIndividual, currentTime)

    colorIndex += 1
    print

def main(args):

    global injectionTimer
    global db
    global window
    global removeInjected

    db = DATABASE()

    initPopulation = args.initPopulation
    removeInjected = args.removeInjected

    if initPopulation:
        Initialize_Global_Population()

    window = PYGAMEWRAPPER(width=REWARD_WINDOW_W, height=REWARD_WINDOW_H, fontSize=FONT_SIZE)
    injectionTimer = TIMER(INJECTION_PERIOD)
    generation  = 1

    while True:

        print "Generation: ", generation

        Steady_State()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.Quit()


        generation += 1
        print

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Steady state Version 4.')
    
    parser.add_argument('--initPopulation', action='store_true',\
     help='initialize the population.')

    parser.add_argument('--removeInjected', action='store_true',\
     help='remove an injected individual from the diversity pool.')

    args = parser.parse_args()

    main(args)



