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

sys.path.append('../bots')

from database import DATABASE
from settings import *
from pygameWrapper import PYGAMEWRAPPER

colorIndex = 0
morphologyIndex = 0

SUB_POPULATION_SIZE = 5
MORPHOLOGY_DURATION = 1 * 60
INDIVIDUAL_DURATION = 30
REWARD_WINDOW_W     = 950
REWARD_WINDOW_H     = 280

currentColor = validColors[colorIndex % len(validColors)]
robotType = validRobots[morphologyIndex % len(validRobots)]

mydatabase = DATABASE()

window = PYGAMEWRAPPER(width=REWARD_WINDOW_W, height=REWARD_WINDOW_H, fontSize=23)

currentCommand = {}

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
    with open( path , 'wb' ) as f:
        pickle.dump(sensorValues, f)

def Store_Controller_To_File(individual):

    # get directory
    path = "../controllers/"+ robotType
    if not os.path.exists(path):
        os.makedirs(path)

    # get filename and extension
    path += '/robot_' + str(individual.id) + ".dat"
    with open( path , 'wb' ) as f:
        pickle.dump(individual, f)

def Load_Controller_From_File(robotID):

    brainPath = "../controllers/"+ robotType +"/robot_"+ str(robotID) +".dat" 

    if not os.path.isfile(brainPath): 
        return None

    return Read_File(brainPath)

def Load_From_Diversity_Pool(robotType):

    path = "../diversity_pool/"+ robotType + "/*.dat" 

    brainPaths = list(glob.iglob(path))

    if len(brainPaths) == 0: return None

    randomIndex = np.random.randint(low=0, high=len(brainPaths))
    if not os.path.isfile(brainPaths[randomIndex]): 
        return None

    return Read_File(brainPaths[randomIndex])

def Read_File(filePath):

    try:
        f = open(filePath,'r')
        individual = pickle.load(f)
        f.close

        print "Successful loading ", filePath
        return individual
    except:
        print "Failed loading ", filePath 
        return None

def Draw_Reinforcment_Window():

    global currentCommand
    global currentColor

    window.Wipe()

    cmdTxt = currentCommand['cmdTxt']

    myy = 10
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "y", x= 70, y=myy, color=currentColor.upper())
    window.Draw_Text(" if the ["+ currentColor[0].upper() + "]"+ currentColor[1:]+\
        " robot is obeying the command", x= 110, y=myy)
    window.Draw_Text("["+ cmdTxt +"].", x= 580, y=myy, color='BROWN')

    myy += 40
    window.Draw_Text("Type", x= 10, y= myy)
    window.Draw_Text("!"+ currentColor[0] + "n", x= 70, y=myy, color=currentColor.upper())
    window.Draw_Text(" if the ["+ currentColor[0].upper() + "]"+ currentColor[1:]+\
     " robot is [N]ot obeying the command", x= 110, y=myy)
    window.Draw_Text("["+ cmdTxt +"].", x= 635, y=myy, color='BROWN')

    myy += 40
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "l", x= 70, y=myy, color=currentColor.upper())
    window.Draw_Text(" if you [L]ike the ["+ currentColor[0].upper() + "]"+\
        currentColor[1:]+ " robot." , x= 110, y=myy)
    
    myy += 40
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "d", x= 70, y=myy, color=currentColor.upper())
    window.Draw_Text(" if you [D]islike the ["+ currentColor[0].upper() + "]"+\
     currentColor[1:]+ " robot." , x= 110, y=myy)

    myy += 60
    window.Draw_Text("Need help? Type", x= 700, y=myy) 
    window.Draw_Text("?", x= 880, y=myy, color='BROWN')

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

    return Compete_Based_On_Dominance(pop[ind1], pop[ind2])

def Compete_Based_On_Dominance(individual1, individual2):

    winner, loser = individual1, individual2
    if Dominance(individual2, individual1):
        winner, loser = individual2, individual1
    elif not Dominance(individual1, individual2):
        return None
    print "Winner is: ", winner['robotID'], " loser is: ", loser['robotID']

    mydatabase.kill_robot(loser['robotID'])

    newInd = Load_Controller_From_File(winner['robotID'])
    if newInd == None:  
        mydatabase.kill_robot(winner['robotID'])
    else:
        newInd.Mutate()

    return newInd

def Dominance(individual1, individual2):

    notShownMore    = individual1['numEvals'] <= individual2['numEvals']
    likedMore       = individual1['totalLikeability'] > individual2['totalLikeability']
    moreObedient    = individual1['totalFitness'] > individual2['totalFitness']
    return notShownMore and likedMore and moreObedient

def Add_New_Robot(newIndividual):

    robotID = mydatabase.add_to_robot_table(robotType)
    newIndividual.Set_ID(robotID)
    Store_Controller_To_File(newIndividual)

def Initialize_Sub_Population(numToBeFilled):

    print "Empty slots in sub population of ", robotType, " is: ", numToBeFilled
    while numToBeFilled > 0 :

        newIndividual = Load_From_Diversity_Pool(robotType)
        if newIndividual == None:
            newIndividual = INDIVIDUAL(0, robotType)
        Add_New_Robot(newIndividual)

        numToBeFilled -= 1

def Morphology_Cycle(morphologyTimer):

    global robotType
    global currentCommand
    global currentColor
    global colorIndex
    global morphologyIndex

    while not morphologyTimer.Time_Elapsed():

        aliveIndividuals = mydatabase.fetch_alive_robots(robotType)

        Initialize_Sub_Population(SUB_POPULATION_SIZE - len(aliveIndividuals))

        index    = Select_Random_Individual(len(aliveIndividuals))
        robotID   = aliveIndividuals[index]['robotID']
        randomIndividual = Load_Controller_From_File(robotID)

        if randomIndividual == None:
            mydatabase.kill_robot(aliveIndividuals[index]['robotID'])
            continue

        currentColor   = validColors[colorIndex % len(validColors)]
        currentTime    = datetime.datetime.now()
        currentCommand = mydatabase.get_current_command()
        
        if currentCommand == None or currentCommand == ():
            currentCommand = {'wordToVec': 1.0, 'cmdTxt': DEFAULT_COMMAND}

        wordVector = c.NUM_BIAS_NEURONS*[1.0] + [currentCommand['wordToVec']]

        Draw_Reinforcment_Window()

        mydatabase.add_command_to_display_table(aliveIndividuals[index]['robotID'],
                                                currentCommand['cmdTxt'], currentColor[0], currentTime)

        print "Displaying controller ", randomIndividual.id, " of type ", robotType,\
         " with color: ", currentColor, " and current command: ", currentCommand['cmdTxt'],\
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

def main(argv):

    global robotType
    global morphologyIndex

    generation = 1

    while True:
        print("G: ", generation)

        morphologyTimer = TIMER(MORPHOLOGY_DURATION)

        robotType = validRobots[morphologyIndex % len(validRobots)]

        Morphology_Cycle(morphologyTimer)

        morphologyIndex += 1

        generation += 1
        print

if __name__ == "__main__":
   main(sys.argv[1:])

