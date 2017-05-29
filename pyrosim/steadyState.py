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
from pygameWrapper import PYGAMEWRAPPER
from timer import TIMER

sys.path.append('../bots')

from database import DATABASE
from settings import *

colorIndex = 0
morphologyIndex = 0
numAliveIndividuals = 20

MORPHOLOGY_DURATION =  1 * 60
INDIVIDUAL_DURATION = 30

currentColor = validColors[colorIndex % len(validColors)]
robotType = validRobots[morphologyIndex % len(validRobots)]

mydatabase = DATABASE()

window = PYGAMEWRAPPER(width=1000,height=250)

currentCommand = {'cmdCount':0, 'cmdTxt':"roll"}

def store_Sensors_To_File(individual, currentTime):

    sensorValues = individual.Get_Raw_Sensors()

    id = individual.id

    path = "../sensors/"+ str(currentTime.year) + "/" + str(currentTime.month)+\
        "/" + str(currentTime.day)

    # print path

    if not os.path.exists(path):

        os.makedirs(path)

    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")

    path += '/robot_' + str(individual.id) + "_" + currentTime + ".dat"

    with open( path , 'wb' ) as f:

        pickle.dump(sensorValues, f)


def store_Controller_To_File(individual):

    id = individual.id

    path = "../controllers/"+ robotType

    if not os.path.exists(path):

        os.makedirs(path)

    path += '/robot_' + str(individual.id) + ".dat"

    with open( path , 'wb' ) as f:

        pickle.dump(individual, f)


def load_Controller_From_File(robotID):

    brainPath = "../controllers/"+ robotType +"/robot_"+ str(robotID) +".dat" 

    print brainPath

    if not os.path.isfile(brainPath): return None

    individual = None

    with open(brainPath,'r') as f:

        individual = pickle.load(f)

    return individual


def load_From_Diversity_Pool(robotType):

    path = "../diversity_pool/"+ robotType + "/*.dat" 

    brainPaths = list()

    for f in glob.iglob(path): brainPaths.append(f)

    print path, robotType, len(brainPaths)

    randomIndex = np.random.randint(low=0, high=len(brainPaths))

    if not os.path.isfile(brainPaths[randomIndex]): return None

    individual = None

    with open(brainPaths[randomIndex],'r') as f:

        individual = pickle.load(f)

    return individual

def draw_Reinforcment_Window():

    global currentCommand
    global currentColor

    window.Wipe()

    cmdTxt = currentCommand['cmdTxt']

    myy = 10
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "y", x= 80, y=myy, color=currentColor)
    window.Draw_Text(" if the current robot is obeying the command", x= 130, y=myy)
    window.Draw_Text("["+ cmdTxt +"].", x= 800, y=myy, color='brown')

    
    myy += 40
    window.Draw_Text("Type", x= 10, y= myy)
    window.Draw_Text("!"+ currentColor[0] + "n", x= 80, y=myy, color=currentColor)
    window.Draw_Text(" if the current robot is NOT obeying the command", x= 130, y=myy)
    window.Draw_Text("["+ cmdTxt +"].", x= 800, y=myy, color='brown')

    myy += 40
    
    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "l", x= 80, y=myy, color=currentColor)
    window.Draw_Text(" if you LIKE the current robot." , x= 130, y=myy)
    
    myy += 40

    window.Draw_Text("Type", x= 10, y=myy)
    window.Draw_Text("!"+ currentColor[0] + "d", x= 80, y=myy, color=currentColor)
    window.Draw_Text(" if you DISLIKE the current robot." , x= 130, y=myy)

    myy += 60

    window.Draw_Text("Need help: type", x= 700, y=myy) 
    window.Draw_Text("?", x= 920, y=myy, color='brown')

    window.Refresh()

def select_Random_Individual(pop):

    pop_len = len(pop)

    return np.random.randint(pop_len)

def compete_While_Waiting_For(pop, ignoreIndex):

    pop_len = len(pop)

    if (pop_len <= 2) : return None

    ind1 =  np.random.randint(pop_len)
    ind2 =  np.random.randint(pop_len)

    while ind1 == ignoreIndex:
        ind1 =  np.random.randint(pop_len)

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

    newInd = load_Controller_From_File(winner['robotID'])

    print("winner: ", winner['robotID'])

    if newInd == None:  

        mydatabase.Kill_Robot(winner['robotID'])

    else:
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

def morphology_Cycle(morphology_timer):

    global robotType
    global currentCommand
    global currentColor
    global colorIndex
    global morphologyIndex

    while not morphology_timer.Time_Elapsed():

        currentColor = validColors[colorIndex % len(validColors)]

        aliveIndividuals = mydatabase.Fetch_Alive_Robots(robotType)

        temp = mydatabase.Fetch_Popular_Command()

        if temp != None: currentCommand = temp

        # print currentColor, len(aliveIndividuals), numAliveIndividuals

        if len(aliveIndividuals) < numAliveIndividuals:

            if np.random.uniform(0, 1) >=1.0:

                newIndividual = INDIVIDUAL(0, robotType)

            else:

                newIndividual = load_From_Diversity_Pool(robotType)

            robotID = mydatabase.Add_Robot(robotType)

            print "newIndividual", robotID

            newIndividual.Set_ID(robotID)

            store_Controller_To_File(newIndividual)

        else:

            index = select_Random_Individual(aliveIndividuals)

            randomIndividual = load_Controller_From_File(aliveIndividuals[index]['robotID'])

            print "randomIndividual", aliveIndividuals[index]['robotID']

            if randomIndividual == None:

                mydatabase.Kill_Robot(aliveIndividuals[index]['robotID'])

                continue

            draw_Reinforcment_Window()

            currentTime = datetime.datetime.now()

            mydatabase.Add_Command_To_Display(aliveIndividuals[index]['robotID'],
                currentCommand['cmdTxt'], currentColor[0], currentTime)

            randomIndividual.Set_Color(currentColor)

            randomIndividual.Start_Evaluate(False, False, [1.0])

            newIndividual = compete_While_Waiting_For(aliveIndividuals, index)

            if newIndividual != None:

                robotID = mydatabase.Add_Robot(robotType)

                print("child: ", robotID)
                
                newIndividual.Set_ID(robotID)

                newIndividual.store_Controller_To_File()

            randomIndividual.Wait_For_Me()

            store_Sensors_To_File(randomIndividual, currentTime)

        colorIndex += 1

def main(argv):

    global robotType
    global morphologyIndex

    generation = 1

    while True:
        print("G: ", generation)

        morphology_timer = TIMER(MORPHOLOGY_DURATION)

        robotType = validRobots[morphologyIndex % len(validRobots)]

        morphology_Cycle(morphology_timer)

        morphologyIndex += 1

        generation += 1
        print


if __name__ == "__main__":
   main(sys.argv[1:])

