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
sys.path.append('../critic')

import critic as ct
from database import DATABASE
from settings import *
from pygameWrapper import PYGAMEWRAPPER

SUB_POPULATION_SIZE = 5
REWARD_WINDOW_W     = 900
REWARD_WINDOW_H     = 280
FONT_SIZE           = 23
INJECTION_PERIOD    = 30 * 60

colorIndex     = 0
currentColor   = validColors[colorIndex % len(validColors)]
wordVector     = []
currentCommand = {'wordToVec': 1.0, 'cmdTxt': DEFAULT_COMMAND}

db     = None
injectionTimer = None
removeInjected = False
window = PYGAMEWRAPPER(width=REWARD_WINDOW_W, height=REWARD_WINDOW_H, title="Reinforcements", fontSize=FONT_SIZE)

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


def Draw_Reinforcment_Window(run_event):

    global currentCommand
    global currentColor
    global injectionTimer

    WSPACE = 5
    
    while run_event.is_set():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.Quit()

        window.Wipe()

        cmdTxt    = currentCommand['cmdTxt']

        myy = 10
        window.Draw_Text("New here? Type", x= 700, y=myy, fontSize=FONT_SIZE)
        window.Draw_Text("?", x=window.text_x+window.text_width+WSPACE, y=myy-5, color='BROWN',\
         fontSize=FONT_SIZE+8)

        myy += 40
        window.Draw_Text("Type", x= 10, y=myy, fontSize=FONT_SIZE)
        window.Draw_Text("!"+ currentColor[0] + "y", x=window.text_x+window.text_width+WSPACE,\
         y=myy, color=currentColor.upper(), fontSize=FONT_SIZE)

        window.Draw_Text("if Yes, the ["+ currentColor[0].upper() + "]"+ currentColor[1:]+\
         " robot is obeying the command", x=window.text_x+window.text_width+WSPACE, y=myy,\
          fontSize=FONT_SIZE)

        window.Draw_Text("["+ cmdTxt +"].", x=window.text_x+window.text_width+WSPACE,\
         y=myy, color='BROWN', fontSize=FONT_SIZE)

        myy += 40
        window.Draw_Text("Type", x= 10, y= myy, fontSize=FONT_SIZE)
        window.Draw_Text("!"+ currentColor[0] + "n", x=window.text_x+window.text_width+WSPACE,\
         y=myy, color=currentColor.upper(), fontSize=FONT_SIZE)

        window.Draw_Text("if No, the ["+ currentColor[0].upper() + "]"+ currentColor[1:]+\
         " robot is [N]ot obeying the command", x=window.text_x+window.text_width+WSPACE, y=myy,\
          fontSize=FONT_SIZE)

        window.Draw_Text("["+ cmdTxt +"].", x= window.text_x+window.text_width+WSPACE,\
         y=myy, color='BROWN', fontSize=FONT_SIZE)

        myy += 40
        window.Draw_Text("Type", x= 10, y=myy, fontSize=FONT_SIZE)

        window.Draw_Text("!"+ currentColor[0] + "l ", x=window.text_x+window.text_width+WSPACE,\
         y=myy, color=currentColor.upper(), fontSize=FONT_SIZE)

        window.Draw_Text("if you [L]ike the ["+ currentColor[0].upper() + "]"+\
            currentColor[1:]+ " robot." , x=window.text_x+window.text_width+WSPACE, y=myy, fontSize=FONT_SIZE)
        
        myy += 40
        window.Draw_Text("Type", x= 10, y=myy,fontSize=FONT_SIZE)
        window.Draw_Text("!"+ currentColor[0] + "d", x=window.text_x+window.text_width+WSPACE,\
         y=myy, color=currentColor.upper(), fontSize=FONT_SIZE)

        window.Draw_Text("if you [D]islike the ["+ currentColor[0].upper() + "]"+\
         currentColor[1:]+ " robot." , x=window.text_x+window.text_width+WSPACE, y=myy, fontSize=FONT_SIZE)

        myy += 60
        rtime = injectionTimer.Time_Remaining()
        if rtime < 0: rtime = 0
        minute, second = divmod(rtime, 60)
        hour, minute   = divmod(minute, 60)
        rtime = "%02dm:%02ds"%(minute, second)

        window.Draw_Rect(10, myy, 570, 30 , color = 'TAN')
        window.Draw_Text("An unseen silver robot will be added to the population in " + rtime,\
         x=10, y=myy, color='BROWN', fontSize=FONT_SIZE) 

        window.Draw_Text("Need help? Type", x= 600, y=myy, fontSize=FONT_SIZE) 
        window.Draw_Text("?reinforcement", x=window.text_x+window.text_width+WSPACE, y=myy, color='BROWN', fontSize=FONT_SIZE)
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
        critic = load_model('../critic/model.h5')
        print 'Successfully loaded the critic model.'

    except KeyboardInterrupt:
        sys.exit()
    except:
        print 'Unable loading the critic model.'
        return None

    try:
        with open('../critic/data_stats.dat') as f:
            data_stats = pickle.load(f)
            _min = data_stats['_min']
            _max = data_stats['_max']

    except KeyboardInterrupt:
        sys.exit()
    except:
        print 'Unable loading the normalization data.'
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

    print _min, _max

    features1 = ct.Extract_Features( sensorValues1 )
    features2 = ct.Extract_Features( sensorValues2 )

    if features1 == None or features2 == None: 
        print 'Features are not calculated properly' 
        return None

    print features1[0].shape, features2[0].shape
    assert features1[0].shape == features1[0].shape

    # normalize the sensor data for both individuals.
    normalizedSensors1 = (features1[0] - _min) / (_max - _min)
    normalizedSensors2 = (features2[0] - _min) / (_max - _min)

    sensor_input = np.stack(( normalizedSensors1, normalizedSensors2))
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
        print 'Not able loading it from the file...Killing robot ', winner['robotID']
        db.Kill_Robot(winner['robotID'])
        print 'Replacing it with a random one from the same type.'
        mutatedOne = INDIVIDUAL(0, winner['type'])

    else:
        mutatedOne = Create_Mutation(winnerIndividual)

    Add_New_Robot(mutatedOne, winner['robotID'])

def Compete_Based_On_Dominance(individual1, individual2):

    winner, loser = individual1, individual2
    if Dominance(individual2, individual1):
        winner, loser = individual2, individual1
    elif not Dominance(individual1, individual2):
        return None

    print "Winner is: ", winner['robotID']
    print "Loser is: ", loser['robotID']
    print "Killing the loser..."

    db.Kill_Robot(loser['robotID'])

    winnerIndividual = Load_Controller_From_File(winner['robotID'], winner['type'])

    if winnerIndividual == None:  
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
    print 'Mutate the brain of robot: ', newIndividual.id

    return newIndividual

def Dominance(individual1, individual2):

    notShownMore    = individual1['numEvals'] <= individual2['numEvals']
    likedMore       = individual1['totalLikeability'] > individual2['totalLikeability']
    moreObedient    = individual1['totalFitness'] > individual2['totalFitness']
    return notShownMore and likedMore and moreObedient

def Add_New_Robot(newIndividual, parentID=0):

    print 'Trying to add a new robot...'
    robotID = db.Add_To_Robot_Table(newIndividual.robotType, parentID)
    print 'New robot added... type: ', newIndividual.robotType, ' and ID:', robotID, 'parentID: ', parentID

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

def Steady_State(run_event):

    global injectionTimer
    global currentCommand
    global currentColor
    global colorIndex
    global wordVector
    global robotInfo

    generation  = 1

    while run_event.is_set():

        print "Generation: ", generation

        aliveIndividuals = db.Fetch_Alive_Robots("all")

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
                toBe_Injected = INDIVIDUAL(0, injectionType)

            robotID = Add_New_Robot(toBe_Injected)
            db.Kill_Robot(min_Evaluated_Robot['robotID'])

            aliveIndividuals = db.Fetch_Alive_Robots("all")

            toBe_Displayed = next((item for item in aliveIndividuals if item['robotID'] == robotID), None)

            if toBe_Displayed == None: return

            currentColor = specialColor

        else:
            toBe_Displayed_Index = Select_Random_Individual(len(aliveIndividuals))
            toBe_Displayed = aliveIndividuals[toBe_Displayed_Index]
            currentColor   = validColors[colorIndex % len(validColors)]

        # print toBe_Displayed

        robotID   = toBe_Displayed['robotID']
        robotType = toBe_Displayed['type']
        randomIndividual = Load_Controller_From_File(robotID, robotType)
        
        if randomIndividual == None:
            print "Could not load robot ", robotID, " with type: ", robotType
            db.Kill_Robot(robotID)
            return

        tempCurrentCommand = db.Get_Current_Command()
        if tempCurrentCommand != None:
            currentCommand = tempCurrentCommand

        wordVector     = c.NUM_BIAS_NEURONS*[1.0] + [currentCommand['wordToVec']]
        currentTime    = datetime.datetime.now()

        db.Add_Command_To_Display_Table(robotID, currentCommand['cmdTxt'], currentColor[0], currentTime)

        print "Displaying robot: ", toBe_Displayed
        print "Displaying color: ", currentColor
        print "Acting command: ", currentCommand
        print "Current time: ", currentTime
        
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
    
    parser.add_argument('--initPopulation', action='store_true',\
     help='initialize the population.')

    parser.add_argument('--removeInjected', action='store_true',\
     help='remove an injected individual from the diversity pool.')

    args = parser.parse_args()

    main(args)


