from sklearn.model_selection import KFold
from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Input, Embedding, LSTM, Dense, Activation
import keras 
from datetime import datetime
from copy import deepcopy

import numpy as np
import time
import matplotlib.pyplot as plt
import h5py
import sys 
import pickle
import os 
import argparse
from scipy.stats.stats import ttest_ind
from keras import backend as K
import tensorflow as tf
import csv

seed = 1234
np.random.seed(seed)

sys.path.append('../bots')
sys.path.append('../pyrosim')

import constants as c
from database import DATABASE
from settings import *

SENSOR_DROP_RATE = 18
num_features     = 4
sequence_len     = c.evaluationTime/SENSOR_DROP_RATE
synthetic_data   = False

_COMMAND = {'move', 'stop'}
MAX_POS_SAMPLES = 150
_MORPHOLOGY = 'quadruped'
main_path = "/Users/twitchplaysrobotics/TPR-backup"

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot', 'quadruped':'quadruped', 'starfishbot':'starfishbot',
         'spherebot':'spherebot', 'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot'}

# fix random seed for reproducibility
np.random.seed(1234)


class CRITIC:

    def __init__(self, params):
        self.model = None
        self.params = params

    def setup_model(self):
        sensor_input = Input(shape=(sequence_len, num_features), name='sensor_input')
        lstm1 = LSTM(12, return_sequences=True)(sensor_input)
        dropout1 = Dropout(0.2)(lstm1)
        lstm2 = LSTM(12, return_sequences=False)(dropout1)
        dropout2 = Dropout(0.2)(lstm2)
        # output1 = Dense(12, activation='tanh')(dropout2)
        output = Dense(1, activation='relu', name='output')(dropout2)
        model = Model(inputs=[sensor_input], outputs=[output])
        model.compile(optimizer='rmsprop', loss={'output': 'mse'}, loss_weights={'output': 1.}, metrics=['mae'])

        return model

    def train_model(self, sensors, obedience):
        cv_scores, pcv_scores, rcv_scores = [], [], []
        kfold = KFold(n_splits=self.params['n_split'], shuffle=True, random_state=seed)

        for train, test in kfold.split(sensors, obedience):
            start_time = time.time()
            model = self.setup_model()

            scores = model.evaluate(sensors[test], obedience[test], verbose=0)
            rcv_scores.append(scores[1])
            print "Random control Test: %s: %.4f"%(model.metrics_names[1], scores[1]),

            # train the model
            model.fit({'sensor_input': sensors[train]}, {'output': obedience[train]},
                epochs=self.params['epochs'], batch_size=self.params['batch_size'], verbose=0)

            # test the model with non-permuted reinforcements
            scores = model.evaluate(sensors[test], obedience[test], verbose=0)

            # print 'Training duration (s) : ', time.time() - start_time,
            print "Regular Test: %s: %.4f"%(model.metrics_names[1], scores[1]),
            cv_scores.append(scores[1])

            # test the model with permuted reinforcements
            random_obedience = deepcopy(obedience[test]) #np.random.uniform(0, 1, len(test))
            np.random.shuffle(random_obedience)
            pscores = model.evaluate(sensors[test], random_obedience, verbose=0)

            print "Permuted Test: %s: %.4f"%(model.metrics_names[1], pscores[1])
            pcv_scores.append(pscores[1])

        print("Regular Test: %.3f (+/- %.3f)" % (np.mean(cv_scores), np.std(cv_scores)))
        print("Permuted Test: %.3f (+/- %.3f)" % (np.mean(pcv_scores), np.std(pcv_scores)))
        # print("Random Test: %.3f (+/- %.3f)" % (np.mean(rcv_scores), np.std(rcv_scores)))

        print("Ttest simple Exp. vs Permuted", ttest_ind(cv_scores, pcv_scores))
        # print("Ttest simple Exp. vs Random", ttest_ind(cv_scores, rcv_scores))
        return pcv_scores, cv_scores


def custom_loss(y_true, y_pred):
    pos_y_true = tf.gather( y_true, tf.where( tf.equal( y_true, +1)))
    pos_y_pred = tf.gather( y_pred, tf.where( tf.equal( y_true, +1)))
    pos_count  = tf.reduce_sum(tf.cast(tf.equal(y_true, +1), tf.float32))

    neg_y_true = tf.gather( y_true, tf.where( tf.less( y_true, +1)))
    neg_y_pred = tf.gather( y_pred, tf.where( tf.less( y_true, +1)))
    neg_count  = tf.reduce_sum(tf.cast(tf.less(y_true, +1), tf.float32))

    first_sum = tf.div(tf.reduce_sum(tf.abs(tf.subtract(pos_y_true, pos_y_pred))), 2.0*pos_count)
    second_sum= tf.div(tf.reduce_sum(tf.abs(tf.subtract(neg_y_true, neg_y_pred))), 2.0*neg_count)

    return (first_sum + second_sum) / 2.0


def Load_Training_Data(mydatabase):
    sql = """SELECT d.robotID, numYes, numNo, d.cmdTxt, startTime, cmdTxt from display as d JOIN
     robots as r ON d.robotID=r.robotID WHERE d.cmdTxt in """ + '(' + ",".join(["'"+c+"'" for c in _COMMAND]) + ')' + \
          " and r.type='%s' and (numYes+numNo)>0;"%_MORPHOLOGY
    robots = mydatabase.Execute_Select_Sql_Command(sql, "Failed to retrieve record of a dispaly...")
    print('Number of samples: ', len(robots), " Morphology: ", _MORPHOLOGY, "Command: ", _COMMAND)

    sensor_input, output = [], []

    pos_count = 0
    for robot in robots:
        sensors = Load_Sensors_From_File(robot)
        if sensors is None: continue

        tfeatures = Extract_Features(sensors)
        if tfeatures is None or tfeatures.shape != (sequence_len, num_features): continue
        
        obedience = float(robot['numYes']-robot['numNo'])/float(robot['numYes']+robot['numNo'])
        if robot['cmdTxt'] == 'stop': obedience *= -1
        # print tfeatures.shape, obedience

        if obedience == +1:
            pos_count += 1
            if pos_count > MAX_POS_SAMPLES:
                continue

        sensor_input.append(tfeatures)
        output.append(obedience)

    neg_count = output.count(-1)
    pos_count = output.count(+1)
    diff = abs(neg_count - pos_count)

    if neg_count > pos_count:
        extra_indices = np.random.choice([idx for idx in range(len(output)) if output[idx] == +1], diff)
        sensor_input.extend([sensor_input[idx] for idx in extra_indices])
        output.extend([+1 for _ in range(diff)])

    elif neg_count < pos_count:
        extra_indices = np.random.choice([idx for idx in range(len(output)) if output[idx] == -1], diff)
        sensor_input.extend([sensor_input[idx] for idx in extra_indices])
        output.extend([-1 for _ in range(diff)])

    return np.array(sensor_input), np.array(output)


def Load_Sensors_From_File(record):
    robotID = record['robotID']
    startTime = record['startTime']
    
    path = main_path + "/sensors/"+ str(startTime.year) + "/" + str(startTime.month)+ "/" + str(startTime.day)+\
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
    temp = np.diff(temp, axis=0)
    temp = np.absolute(temp)
    temp = np.average(temp, axis=1)
    temp = np.hstack((temp, np.array(temp[-1])))
    return temp[1::SENSOR_DROP_RATE]


def Ray_Feature_Extraction(values):
    return values[1::SENSOR_DROP_RATE]


def Position_Feature_Extraction(values):
    return values[1::SENSOR_DROP_RATE]


def Touch_Feature_Extraction(values):
    values = np.array(values).T
    temp = np.average(values, axis=1)
    return temp[1::SENSOR_DROP_RATE]


def Extract_Features(sample):
    touch, prop = [], []
    ray, posX, posY, posZ, features = None, None, None, None, None
    # print sample.keys()

    for key in sample.keys():
        if key.startswith('P') and key.endswith('_X') :
            posX = Position_Feature_Extraction(sample[key])
        
        elif key.startswith('P') and key.endswith('_Y'):
            posY = Position_Feature_Extraction(sample[key])

        elif key.startswith('P') and key.endswith('_Z'):
            posZ = Position_Feature_Extraction(sample[key])

        elif key.startswith('T'):
            touch.append(sample[key])

        elif key.startswith('R0'):
            ray = Ray_Feature_Extraction(sample[key])

        # propriceptive sensor
        elif key.startswith('P'):
            prop.append(sample[key])

    if len(prop) != 0:
        prop = Propriceptive_Feature_Extraction(prop)
    else: return None

    if len(touch) != 0:
        touch = Touch_Feature_Extraction(touch)
    else: return None

    features = np.array([posX, posY, posZ, prop]).T
    return features


def main(args):
    global _MORPHOLOGY
    batch_size = args.batch_size
    n_split = args.n_split
    epoch = args.epoch
    mydatabase = DATABASE()

    params = {'epochs':epoch, 'batch_size':batch_size, 'n_split':n_split}

    outfile_regular = open("critic_results_regular_150.csv", "w")
    writer_regular = csv.writer(outfile_regular, delimiter=",")

    outfile_permuted = open("critic_results_permuted_150.csv", "w")
    writer_permuted = csv.writer(outfile_permuted, delimiter=",")

    writer_permuted.writerow(['trials'] + map(str, range(n_split)))
    writer_regular.writerow(['trials'] + map(str, range(n_split)))

    c = CRITIC(params)

    for key, val in names.items():

        _MORPHOLOGY = key
        c.setup_model()
        data = Load_Training_Data(mydatabase)
        sensors, obedience = data

        print sensors.shape, obedience.shape
        _min = np.min(np.min(sensors, axis=1), axis=0)
        _max = np.max(np.max(sensors, axis=1), axis=0)
        sensors = (sensors - _min) / (_max - _min)
        obedience = (obedience-np.min(obedience))/(np.max(obedience)-np.min(obedience))
        counts, bins = np.histogram(obedience, bins=10)

        if counts[-1] < MAX_POS_SAMPLES:
            print "Not enough data."
            continue
        print "Data Histogram: ", bins, counts

        pcv_scores, cv_scores = c.train_model(sensors, obedience)
        writer_permuted.writerow([val] + map(str, pcv_scores))
        writer_regular.writerow([val] + map(str, cv_scores))

    outfile_regular.close()
    outfile_permuted.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Critic Model.')
    parser.add_argument('--batch_size', '-b', type=int, default=512, help='batchSize, default=512.')
    parser.add_argument('--epoch', '-e', type=int, default=100, help='Number of learning epochs, default=1000.')
    parser.add_argument('--n_split', '-n', type=int, default=10, help='Validation split, default=10.')
    # parser.add_argument('--shuffle', '-s', action='store_true', help='Shuffle obedience.')
    args = parser.parse_args()
    main(args)
