from datetime import datetime
from copy import deepcopy
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import pickle
import os
import argparse
import csv

sys.path.append('../bots')
sys.path.append('../pyrosim')

import constants as c
from database import DATABASE
from settings import *

main_path = "/Users/twitchplaysrobotics/TPR-backup"
commands = {'move', 'stop'}

names = {'1': 'stickbot', '2': 'twigbot', '3': 'branchbot', '4': 'treebot', 'quadruped': 'quadruped',
         'starfishbot':'starfishbot', 'spherebot':'spherebot', 'shinbot': 'tablebot', 'snakebot':'snakebot',
         'crabbot': 'crabbot'}


def Load_Sensors_From_File(record):
    robotID = record['robotID']
    startTime = record['startTime']

    path = main_path + "/sensors/" + str(startTime.year) + "/" + str(startTime.month) + "/" + str(startTime.day) + \
           "/robot_" + str(robotID) + '_' + startTime.strftime("%Y-%m-%d-%H-%M-%S") + ".dat"

    if not os.path.isfile(path):
        print "Failed loading ", path
        return None
    sensors = Read_File(path)
    return sensors


def Read_File(filePath):
    sensors = None
    try:
        with open(filePath, 'r') as f:
            sensors = pickle.load(f)
            # print "Loading ", filePath,
    except:
        print "Failed loading ", filePath
    return sensors


def Propriceptive_Feature_Extraction(values):
    temp = np.array(values).T
    temp = temp[1::10]
    temp = np.diff(temp, axis=0)
    temp = np.absolute(temp)
    temp = np.average(temp, axis=1)
    temp = np.hstack((temp, np.array(temp[-1])))
    return np.average(temp)


def Get_Head_Location(sample):
    posX, posY, posZ = None, None, None
    for key in sample.keys():
        if key.startswith('P') and key.endswith('_X'):
            posX = sample[key]

        elif key.startswith('P') and key.endswith('_Y'):
            posY = sample[key]

        elif key.startswith('P') and key.endswith('_Z'):
            posZ = sample[key]

    features = np.array([posX, posY, posZ]).T
    # return np.linalg.norm(features[1786, :]-features[0, :])
    return np.abs(features[1786, 1]-features[0, 1])



def Get_Propriceptive_Change(sample):
    prop = []
    for key in sample.keys():
        if key.startswith('P') and (key.endswith('_X') or key.endswith('_Y') or key.endswith('_Z')):
            continue

        elif key.startswith('P'):
            prop.append(sample[key])

    return Propriceptive_Feature_Extraction(prop)


def Load_Data(mydatabase, morphology):
    sql = """SELECT d.robotID, numYes, numNo, d.cmdTxt, startTime, cmdTxt from display as d JOIN
    robots as r ON d.robotID=r.robotID WHERE d.cmdTxt in """ + '(' + ",".join(["'"+c+"'" for c in commands]) + ')' + \
          " and r.type='%s' and (numYes+numNo)>0;" % morphology

    robots = mydatabase.execute_select_sql_command(sql, "Failed to retrieve record of a dispaly...")
    print('Number of samples: ', len(robots), " Morphology: ", morphology, "Command: ", commands)

    Y, output = [], []
    for robot in robots:
        sensors = Load_Sensors_From_File(robot)
        # head = Get_Head_Location(sensors)
        head = Get_Propriceptive_Change(sensors)
        Y.append(head)
        obedience = float(robot['numYes']-robot['numNo'])/float(robot['numYes']+robot['numNo'])
        if robot['cmdTxt'] == 'stop':
            obedience *= -1*obedience
        output.append(obedience)
        # print head, obedience
    return Y, output

mydatabase = DATABASE()
fig, axes = plt.subplots(figsize=(20, 10), ncols=5, nrows=2)
ax = axes.flatten()
i = 0
for key, val in names.items():
    Y, output = Load_Data(mydatabase, key)
    ax[i].scatter(Y, output, alpha=0.8)
    # ax[i].hist(Y, 20, color='g', alpha=0.8)
    ax[i].set_title(val)
    i = i+1

    # plt.title('Histogram of Final Head Position)

plt.show()