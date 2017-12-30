import numpy as np
import sys
import pickle
import os
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt

sys.path.append('../bots')
sys.path.append('../pyrosim')

from database import DATABASE
from settings import *

# X_LABEL = 'Average Change in Head Location'
# X_LABEL = 'Average Change in Joint Position'
X_LABEL = 'Absolute Change in Head Location'

DROP_RATE = 18
POS_SAMPLES = 100
main_path = "/Users/twitchplaysrobotics/TPR-backup"
commands = {'move', 'stop'}

names = {'3': 'branchbot', '4': 'treebot', 'quadruped': 'quadruped', 'starfishbot':'starfishbot',
         'spherebot':'spherebot', 'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot'}


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
    temp = []
    for row in values:
        temp.append(row[1::DROP_RATE])
    temp = np.array(temp).T
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
    # return np.linalg.norm(features[900, :]-features[0, :])
    return np.linalg.norm(features[1786, :]-features[0, :])
    # return np.abs(features[1786, 1]-features[0, 1])


def Get_Average_Change_Head_Location(sample):
    posX, posY, posZ = None, None, None
    for key in sample.keys():
        if key.startswith('P') and key.endswith('_X'):
            posX = sample[key][1::DROP_RATE]
            posX = np.average(np.absolute(np.diff(posX)))

        elif key.startswith('P') and key.endswith('_Y'):
            posY = sample[key][1::DROP_RATE]
            posY = np.average(np.absolute(np.diff(posY)))

        elif key.startswith('P') and key.endswith('_Z'):
            posZ = sample[key][1::DROP_RATE]
            posZ = np.average(np.absolute(np.diff(posZ)))

    # print posX, posY, posZ
    return posX, posY, posZ


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

    Y, X = [], []
    for robot in robots:
        sensors = Load_Sensors_From_File(robot)

        obedience = float(robot['numYes']-robot['numNo'])/float(robot['numYes']+robot['numNo'])

        if robot['cmdTxt'] == 'stop': obedience *= -1
        if -1 < obedience < +1: continue
        if obedience == +1 and X.count(+1) >= POS_SAMPLES: continue

        # Y.append(Get_Head_Location(sensors))
        Y.append(Get_Propriceptive_Change(sensors))
        # Y.append(np.linalg.norm([Get_Average_Change_Head_Location(sensors)]))

        X.append(obedience)

    return Y, X


def Balance_Data(Y, X):
    """
        Balance data by oversampling the under represented data points
        :param sensor_input: LIST
        :param output: List
        :return: Two Lists
    """
    # count negative and positive samples
    neg_count, pos_count = X.count(-1), X.count(+1)
    diff = abs(neg_count - pos_count)

    # re-sample positive samples if number of negative samples are larger than the positive ones
    if neg_count > pos_count:
        extra_indices = np.random.choice([idx for idx in range(len(X)) if X[idx] == +1], diff)
        Y.extend([Y[idx] for idx in extra_indices])
        X.extend([+1 for _ in range(diff)])

    # re-sample negative samples if number of positive samples are more than the negative ones
    elif neg_count < pos_count:
        extra_indices = np.random.choice([idx for idx in range(len(X)) if X[idx] == -1], diff)
        Y.extend([Y[idx] for idx in extra_indices])
        X.extend([-1 for _ in range(diff)])

    counts, bins = np.histogram(np.array(X), bins=10)
    print bins, counts
    return Y, X


mydatabase = DATABASE()
fig, axes = plt.subplots(figsize=(20, 10), ncols=4, nrows=2)
ax = axes.flatten()
ax[0].set_ylabel("Normalized Reinforcement Signals")
ax[6].set_xlabel(X_LABEL)

i = 0
for key, val in names.items():
    Y, X = Load_Data(mydatabase, key)
    Balance_Data(Y, X)
    # sns.regplot(x=np.array(Y), y=np.array(X), color="g", ax=ax[i])
    ax[i].hist(Y, 20, color='g', alpha=0.8)
    ax[i].set_title(val)
    i = i+1
    # plt.title('Histogram of Final Head Position)

plt.show()
