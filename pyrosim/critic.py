
from pyrosim import PYROSIM
import numpy as np
import random
from individual import INDIVIDUAL
from copy import deepcopy
import sys 
import pickle
import os 
import constants as c
from timer import TIMER

sys.path.append('../bots')

from database import DATABASE
from settings import *

mydatabase = DATABASE()

def Read_From_Database(displayTime):

    return mydatabase.Fetch_From_Disply_Table(displayTime)

def Remove_Sensor_File(fileToBeRemoved):

    try:
        os.remove(fileToBeRemoved)
    except:
        print "unable to remove this file.."

def Load_Sensors_From_File():

    # get directory
    path = "../sensors/"

    dataForCritic = []

    # recursively find all the sensor files.
    sensorFiles = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(path)
    for f in files if f.endswith('.dat')]

    print "num of sensor files: ", len(sensorFiles)
    if len(sensorFiles) == 0: return None

    for path in sensorFiles:

        if not os.path.isfile(path): 
            continue

        # load the sensors.
        sensors = Read_File(path)

        # load the crowd inputs from database.
        start   = path.rfind('_')
        end     = path.rfind('.')
        displayTime = path[start+1:end]
        record =  Read_From_Database(displayTime)

        if record == None:
            continue

        # ignore this evaluation and remove this sensor file if it has not received
        # any inputs from the crowd.
        if record['numYes'] == 0 and record['numNo'] == 0 and \
            record['numLike'] ==0 and record['numDislike'] == 0:

            # Remove_Sensor_File(path)
            continue

        # ignore this evaluation if it has not received any yes or no from the crowd.
        if record['numYes'] == 0 and record['numNo'] == 0:
            continue

        # calculate obedience and add it to the dictionary.
        obedience = float(rewards['numYes']-rewards['numNo'])/float(rewards['numYes']+rewards['numNo'])
        rewards['obedience'] = obedience

        # remove unnecessary keys.
        map(rewards.pop, ['numLike','numDislike', 'numNo', 'numYes'])

        dataForCritic.append( dict(sensors.items() + record.items()))

    return dataForCritic

def Prepare_Training_Features(dataForCritic):

    for sample in dataForCritic:

        

def Read_File(filePath):

    sensors = None

    try:
        with open(filePath, 'r') as f:
            sensors = pickle.load(f)

        print "Successful loading ", filePath
    except:
        print "Failed loading ", filePath 
    
    return sensors

dataForCritic = Load_Sensors_From_File()
print "samples for critic: ", len(dataForCritic)

trainingData  = Prepare_Training_Data(dataForCritic)

