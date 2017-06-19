
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

SENSOR_DROP_RATE  = 6
mydatabase = DATABASE()

def Read_From_Database(displayTime):

    record= mydatabase.Fetch_From_Disply_Table(displayTime)

    if record == None: return None

    # ignore this evaluation and remove this sensor file if it has not received
    # any inputs from the crowd.
    # if record['numYes'] == 0 and record['numNo'] == 0 and \
    #     record['numLike'] ==0 and record['numDislike'] == 0:

    #     # Remove_Sensor_File(path)
    #     return None

    # ignore this evaluation if it has not received any yes or no from the crowd.
    # if record['numYes'] == 0 and record['numNo'] == 0:
    #     return None

    # calculate obedience and add it to the dictionary.
    try:
        obedience = float(record['numYes']-record['numNo'])/float(record['numYes']+record['numNo'])
    except:
        obedience = 0

    record['obedience'] = obedience

    # remove unnecessary keys.
    map(record.pop, ['numLike','numDislike', 'numNo', 'numYes'])

    return record

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

        sample = Extract_Features(dict(sensors.items() + record.items()))

        # dataForCritic.append( dict(sensors.items() + record.items()))

    return dataForCritic

def Propriceptive_Feature_Extraction(values):

    values = np.array(values).T

    temp = np.diff(values, axis=0)
    print "joint features: ", temp.shape

    temp = np.average(temp, axis=1)
    print "joint features: ", temp[-1],temp.shape

    temp = np.hstack((temp, np.array(temp[-1])))
    print "joint features: ", temp.shape

    return temp[1::SENSOR_DROP_RATE]

def Ray_Feature_Extraction(values):
    
    return values[1::SENSOR_DROP_RATE]

def Position_Feature_Extraction(values):

    return values[1::SENSOR_DROP_RATE]

def Touch_Feature_Extraction(values):

    values = np.array(values).T
    print 'touch features:', values.shape
    temp   = np.average(values, axis=1)
    print 'touch features:', temp.shape

    return temp[1::SENSOR_DROP_RATE]

def Extract_Features(sample):

    touch = []
    prop  = []
    ray   = None
    posX  = None
    posY  = None
    posZ  = None

    print sample.keys()
    
    if 'R0' not in sample.keys(): return None

    for key in sample.keys():

        # position_x sensor
        if key.startswith('P') and key.endswith('_X') :
            print key, sample[key].shape
            posX = Position_Feature_Extraction(sample[key])
        
        # position_y sensor
        elif key.startswith('P') and key.endswith('_Y'):
            print key, sample[key].shape
            posY = Position_Feature_Extraction(sample[key])

        # position_z sensor
        elif key.startswith('P') and key.endswith('_Z'):
            print key, sample[key].shape
            posZ = Position_Feature_Extraction(sample[key])

        # touch sensor
        elif key.startswith('T'):
            print key, sample[key].shape
            touch.append(sample[key])

        # ray sensor 
        elif key.startswith('R0'):
            print key, sample[key].shape
            ray = Ray_Feature_Extraction(sample[key])

        # propriceptive sensor
        elif key.startswith('P'):
            print key, sample[key].shape
            prop.append(sample[key])

    if len(prop) != 0:
        prop = Propriceptive_Feature_Extraction(prop)
    else: return None

    if len(touch) != 0:
        touch = Touch_Feature_Extraction(touch)
    else: return None

    timeSeriedFeatures     = np.array([posX[:], posY, posZ, ray, touch, prop]).T

    print 'sensors: ', np.array(timeSeriedFeatures).shape

    nonTimedSeriedFeatures = sample['wordToVec']

    output                 = sample['obedience']

    return (timeSeriedFeatures, nonTimedSeriedFeatures, output)

def Prepare_Training_Features(dataForCritic):

    sensor_data = []
    word_data   = []
    output      = []

    for sample in dataForCritic:

        tfeatures, ntfeatures, output = Extract_Features(sample)
        sensor_data.append(tfeatures)
        word_data.append(ntfeatures)
        outputs.append(output)

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

trainingData  = Prepare_Training_Features(dataForCritic)

