from pyrosim import PYROSIM
import numpy as np
import random
from individual import INDIVIDUAL
from copy import deepcopy
import datetime
import sys 
import pickle
import os 
import glob
import constants as c
from timer import TIMER
from keras.models import load_model
import pygame
import argparse

import critic as ct

sys.path.append('../bots')

from database import DATABASE
from settings import *
from pygameWrapper import PYGAMEWRAPPER

SUB_POPULATION_SIZE = 5
REWARD_WINDOW_W     = 910
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
injectionFlag  = False
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
        os.remove(brainPaths[randomIndex])
        print "Successfully removed the injected robot from the diversity pool.."
    
    except KeyboardInterrupt:
        sys.exit()

    except:
        print "Was not able to remove the injected robot from the diversity pool.."

def Draw_Reinforcment_Window():

    global currentCommand
    global currentColor
    global window

    window.Wipe()

    cmdTxt = currentCommand['cmdTxt']

    myy = 10

    window.Draw_Text("New here? Type", x= 10, y=myy)
    window.Draw_Text("?", x= 14*12, y=myy, color='BROWN')

    myy += 40
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "y", x= 60, y=myy, color=currentColor.upper())
    window.Draw_Text(" if the ["+ currentColor[0].upper() + "]"+ currentColor[1:]+\
     " robot is obeying the command", x= 90, y=myy)
    window.Draw_Text("["+ cmdTxt +"].", x=500, y=myy, color='BROWN')

    myy += 40
    window.Draw_Text("Type", x= 10, y= myy)
    window.Draw_Text("!"+ currentColor[0] + "n", x= 60, y=myy, color=currentColor.upper())
    window.Draw_Text(" if the ["+ currentColor[0].upper() + "]"+ currentColor[1:]+\
     " robot is [N]ot obeying the command", x= 90, y=myy)
    window.Draw_Text("["+ cmdTxt +"].", x= 540, y=myy, color='BROWN')

    myy += 40
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "l", x= 60, y=myy, color=currentColor.upper())
    window.Draw_Text(" if you [L]ike the ["+ currentColor[0].upper() + "]"+\
        currentColor[1:]+ " robot." , x= 90, y=myy)
    
    myy += 40
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "d", x= 60, y=myy, color=currentColor.upper())
    window.Draw_Text(" if you [D]islike the ["+ currentColor[0].upper() + "]"+\
     currentColor[1:]+ " robot." , x= 90, y=myy)

    myy += 60

    # window.Draw_Text("A new robot will be born in " + str(injectionTimer.Time_Remaining())\
    #  + " s.", x=10, y=myy) 
    window.Draw_Text("Need help? Type", x= 650, y=myy) 
    window.Draw_Text("?rewards", x= 810, y=myy, color='BROWN')

    window.Refresh()

def Select_Random_Individual(popSize):
    return np.random.randint(popSize)

def Compete_While_Waiting_For(pop, ignoreIndex):

    pop_len = len(pop)
    if (pop_len <= 2) : 
        return None

    while True:
        ind1 = Select_Random_Individual(len(pop))
        if ind1 != ignoreIndex:
            break

    while True:
        ind2 = Select_Random_Individual(len(pop))
        if ind2 != ind1 and ind2 != ignoreIndex:
            break
    print "Competing controllers: ", pop[ind1]['robotID'], " and " , pop[ind2]['robotID']
    print pop[ind1]
    print pop[ind2]

    # neither have shown to the crowd.
    if pop[ind1]['numEvals'] == 0 and pop[ind2]['numEvals'] == 0:
        return Compete_Based_On_Obedience(pop[ind1], pop[ind2])

    # both have shown to the crowd.
    elif pop[ind1]['numEvals'] != 0 and pop[ind2]['numEvals'] != 0:
        return Compete_Based_On_Dominance(pop[ind1], pop[ind2])

    # only one has shown to the crowd.
    else:
        return None

def Compete_Based_On_Obedience(record1, record2):

    global currentCommand

    try:
        critic = load_model('critic_model.h5')
        print 'Successfully loaded the critic model.'

    except KeyboardInterrupt:
        print 'Unable loading the critic model.'
        return None

    individual1 = Load_Controller_From_File(record1['robotID'], record1['type'])
    individual2 = Load_Controller_From_File(record2['robotID'], record2['type'])

    if individual1 == None or individual2 == None: return None

    # run in blind mode and collect sensors.
    individual1.Start_Evaluate(False, True, wordVector)
    individual2.Start_Evaluate(False, True, wordVector)

    individual1.Wait_For_Me()
    individual2.Wait_For_Me()

    sensorValues1 = individual1.Get_Raw_Sensors()
    sensorValues2 = individual2.Get_Raw_Sensors()

    del individual2
    del individual1

    print sensorValues1.keys(), sensorValues2.keys()

    features1 = ct.Extract_Features( sensorValues1 )
    features2 = ct.Extract_Features( sensorValues2 )

    if features1 == None or features2 == None: 
        print 'Features are not calculated properly' 
        return None

    print features1[0].shape, features2[0].shape
    assert features1[0].shape == features1[0].shape

    sensor_input = np.stack((features1[0], features2[0]))
    word_input   = np.array(2*[currentCommand['wordToVec']])

    print 'samples to be send to critic: ', sensor_input.shape, word_input.shape
    sample       = {'sensor_input': sensor_input, 'word_input': word_input}

    try:
        pred_obedience = critic.predict(sample)

    except KeyboardInterrupt:
        sys.exit()

    except:
        print 'Unable predicting obedience...'
        return None

    print 'pred_obedience: ', pred_obedience[0], pred_obedience[1]

    if pred_obedience[0] > pred_obedience[1]: 
        winner, loser = record1, record2

    elif pred_obedience[1] > pred_obedience[0]: 
        winner, loser = record2, record1

    else: return None

    print "Winner is: ", winner['robotID'], " loser is: ", loser['robotID']
    print "Killing the loser...", loser['robotID']

    db.Kill_Robot(loser['robotID'])

    winnerIndividual = Load_Controller_From_File(winner['robotID'], winner['type'])
    if winnerIndividual == None:  
        db.Kill_Robot(winner['robotID'])
    
    mutatedOne = Create_Mutation(winnerIndividual)

    return mutatedOne

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

    global currentCommand
    global currentColor
    global colorIndex
    global wordVector
    global injectionFlag
    global db

    aliveIndividuals = db.Fetch_Alive_Robots("all")

    print "Num of alive individuals: ", len(aliveIndividuals)
    assert len(aliveIndividuals) > 2, 'Not enough individuals in the population. Run with --initPopulation flag.'

    index = Select_Random_Individual(len(aliveIndividuals))

    if injectionFlag:

        print 'Time to inject a new individual..'

        zeroEvalsFlag = False
        for i in range(len(aliveIndividuals)): 
            if aliveIndividuals[i]['numEvals'] == 0: 
                zeroEvalsFlag = True
                break

        if zeroEvalsFlag:
            
            print 'There is a spot for the newbie...'
            injectionFlag    = False
            randomType       = validRobots[np.random.randint(0, len(validRobots))]
            randomIndividual = Load_From_Diversity_Pool(randomType)

            if randomIndividual == None:
                randomIndividual = INDIVIDUAL(0, randomType)

            robotID = Add_New_Robot(randomIndividual)
            db.Kill_Robot(aliveIndividuals[i]['robotID'])

            aliveIndividuals = db.Fetch_Alive_Robots("all")

            for i in range(len(aliveIndividuals)): 

                if aliveIndividuals[i]['robotID'] == robotID: 
                    index = i
        else:
            print 'There is NO spots for the newbie...'

    robotID   = aliveIndividuals[index]['robotID']
    robotType = aliveIndividuals[index]['type']
    randomIndividual = Load_Controller_From_File(robotID, robotType)
        
    if randomIndividual == None:
        print "Could not load robot ", robotID, " with type: ", robotType
        db.Kill_Robot(robotID)
        return

    currentColor   = validColors[colorIndex % len(validColors)]
    currentTime    = datetime.datetime.now()
    currentCommand = db.Get_Current_Command()

    if currentCommand == None or currentCommand == ():
        currentCommand = {'wordToVec': 1.0, 'cmdTxt': DEFAULT_COMMAND}

    wordVector     = c.NUM_BIAS_NEURONS*[1.0] + [currentCommand['wordToVec']]

    Draw_Reinforcment_Window()

    db.Add_Command_To_Display_Table(robotID, currentCommand['cmdTxt'], currentColor[0], currentTime)

    print "Displaying robot ", randomIndividual.id, ". type: ", randomIndividual.robotType,\
     ", with color: ", currentColor, " and current command: ", currentCommand['cmdTxt'],\
     " and current time: ", currentTime
    
    randomIndividual.Set_Color(currentColor)
    randomIndividual.Start_Evaluate(False, False, wordVector)

    newIndividual = Compete_While_Waiting_For(aliveIndividuals, index)
    if newIndividual != None:
        Add_New_Robot(newIndividual)

    randomIndividual.Wait_For_Me()

    Store_Sensors_To_File(randomIndividual, currentTime)

    colorIndex += 1
    print

def main(args):

    global injectionFlag
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.Quit()

        print "Generation: ", generation

        Steady_State()

        if injectionTimer.Time_Elapsed():

            print 'Injection timer elapsed'

            injectionTimer.Reset()
            injectionFlag = True

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



