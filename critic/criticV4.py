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

_COMMAND    = {'move'}
_MORPHOLOGY = '3'

main_path = "/Users/twitchplaysrobotics/TPR-backup"

# fix random seed for reproducibility
np.random.seed(1234)

class CRITIC:

    def __init__(self, params):

        self.model = None
        self.params = params

    def setup_model(self):

        sensor_input = Input(shape=(sequence_len, num_features), name='sensor_input')

        lstm1    = LSTM(12, return_sequences=True)(sensor_input)
        dropout1 = Dropout(0.2)(lstm1)
        lstm2    = LSTM(12, return_sequences=False)(dropout1)
        dropout2 = Dropout(0.2)(lstm2)
        output   = Dense(1, activation='relu', name='output')(dropout2)

        model = Model(inputs=[sensor_input], outputs=[output])
        model.compile(optimizer='rmsprop', loss={'output': 'mse'},
                    loss_weights={'output': 1.}, metrics=['mae'])

        return model
        
    def train_model(self, sensors, obedience):

        cv_scores  = []
        pcv_scores = []
        rcv_scores = []

        kfold = KFold(n_splits=self.params['n_split'], shuffle=True,
                    random_state=seed)

        for train, test in kfold.split(sensors, obedience):

            start_time = time.time()
            model = self.setup_model()

            scores = model.evaluate(sensors[test], obedience[test], verbose=0)
            rcv_scores.append(scores[1])
            print "Random control Test: %s: %.4f"%(model.metrics_names[1], scores[1]),

            # train the model
            model.fit({'sensor_input': sensors[train]}, {'output': obedience[train]},
                epochs=self.params['epochs'], batch_size=self.params['batch_size'],
                verbose=0)
            print 'Training duration (s) : ', time.time() - start_time,

            # test the model with non-permutated reinforcements
            scores = model.evaluate(sensors[test], obedience[test], verbose=0)
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
        print("Random Test: %.3f (+/- %.3f)" % (np.mean(rcv_scores), np.std(rcv_scores)))

        print("Ttest simple Exp. vs Permuted", ttest_ind(cv_scores, pcv_scores))
        print("Ttest simple Exp. vs Random", ttest_ind(cv_scores, rcv_scores))

def Load_Training_Data(mydatabase):
    
    sql = """SELECT d.robotID, sum(numYes) as sumYes, sum(numNo) as sumNo, d.cmdTxt 
    from display as d JOIN robots as r ON d.robotID=r.robotID 
    WHERE d.cmdTxt='%s' and r.type='%s' group by d.robotID having 
    (sumNo+sumYes)>0;"""%('move', _MORPHOLOGY)

    err_msg = "Failed to retrieve record of a dispaly..."
    robots  = mydatabase.Execute_Select_Sql_Command(sql, err_msg)

    print('Number of samples: ', len(robots))

    sensor_input = []
    output       = []

    for robot in robots:

        robotID = robot['robotID']

        sql = """SELECT startTime, robotID from display where robotID=%d and 
            cmdTxt='%s' and (numYes<>0 or numNo<>0);"""%(robotID, 'move')

        record  = mydatabase.Execute_SelectOne_Sql_Command(sql, err_msg)

        sensors = Load_Sensors_From_File(record)
        if sensors == None: 
            # print('Not able to load the sensor file.') 
            continue

        features = Extract_Features( sensors )
        if features == None: continue
        tfeatures  = features[0]
        if tfeatures.shape != (sequence_len, num_features): 
            continue
        
        obedience = float(robot['sumYes']-robot['sumNo']) \
                    / float(robot['sumYes']+robot['sumNo'])

        # print tfeatures.shape, obedience

        sensor_input.append(tfeatures)
        output.append(obedience)

    sql = """SELECT d.robotID, sum(numYes) as sumYes, sum(numNo) as sumNo, d.cmdTxt 
    from display as d JOIN robots as r ON d.robotID=r.robotID 
    WHERE d.cmdTxt='%s' and r.type='%s' group by d.robotID having 
    (sumNo+sumYes)>0;"""%('stop', _MORPHOLOGY)

    err_msg = "Failed to retrieve record of a dispaly..."
    robots  = mydatabase.Execute_Select_Sql_Command(sql, err_msg)

    print('Number of samples: ', len(robots))

    for robot in robots:
        robotID = robot['robotID']
        sql = """SELECT startTime, robotID from display where robotID=%d and 
            cmdTxt='%s' and (numYes<>0 or numNo<>0);"""%(robotID, 'stop')

        record  = mydatabase.Execute_SelectOne_Sql_Command(sql, err_msg)
        sensors = Load_Sensors_From_File(record)

        features = Extract_Features( sensors )
        if features == None: continue
        tfeatures  = features[0]
        if tfeatures.shape != (sequence_len, num_features): 
            continue
        
        obedience  =-float(robot['sumYes']-robot['sumNo']) \
                    / float(robot['sumYes']+robot['sumNo'])

        # print tfeatures.shape, obedience

        sensor_input.append(tfeatures)
        output.append(obedience)

    return (np.array(sensor_input), np.array(output))

def Load_Sensors_From_File(record):

    robotID   = record['robotID']
    startTime = record['startTime']
    
    path = main_path + "/sensors/"+ str(startTime.year) + "/" + str(startTime.month)+\
        "/" + str(startTime.day)+ "/robot_" + str(robotID) + '_' +\
         startTime.strftime("%Y-%m-%d-%H-%M-%S") + ".dat"

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

    values = np.array(values).T
    temp   = np.diff(values, axis=0)
    temp   = np.absolute(values)
    temp   = np.average(temp, axis=1)
    temp   = np.hstack((temp, np.array(temp[-1])))

    return temp[1::SENSOR_DROP_RATE]

def Ray_Feature_Extraction(values):
    
    return values[1::SENSOR_DROP_RATE]

def Position_Feature_Extraction(values):

    return values[1::SENSOR_DROP_RATE]

def Touch_Feature_Extraction(values):

    values = np.array(values).T
    temp   = np.average(values, axis=1)

    return temp[1::SENSOR_DROP_RATE]

def Extract_Features(sample):

    touch = []
    prop  = []
    ray   = None
    posX  = None
    posY  = None
    posZ  = None

    features = None
    # print sample.keys()
    
    if 'R0' not in sample.keys(): 
        print 'R0 is missing in sensors.'
        return None

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

    head = np.array([posX, posY, posZ])
    # print posX.shape, head.shape

    head = np.linalg.norm(head, axis=0)

    # print head.shape

    if len(prop) != 0:
        prop = Propriceptive_Feature_Extraction(prop)
    else: return None

    if len(touch) != 0:
        touch = Touch_Feature_Extraction(touch)
    else: return None

    features = np.array([posX, posY, posZ , prop]).T
    # features = np.array([head, prop]).T

    # print features.shape

    # print 'sensors: ', timeSeriedFeatures.shape

    return (features, True)

def main(args):
            
    batch_size = args.batch_size
    n_split    = args.n_split
    epoch      = args.epoch

    mydatabase = DATABASE()

    params = {'epochs':epoch, 'batch_size':batch_size, 'n_split':n_split}

    c = CRITIC(params)
    c.setup_model()

    data = Load_Training_Data( mydatabase )
    sensors, obedience = data

    print np.histogram(obedience, bins=10)

    print sensors.shape, obedience.shape

    _min = np.min(np.min(sensors, axis=1), axis=0)
    _max = np.max(np.max(sensors, axis=1), axis=0)
    sensors = (sensors - _min) / (_max - _min)

    obedience = (obedience-np.min(obedience))/(np.max(obedience)-np.min(obedience))        

    c.train_model(sensors, obedience)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Critic Model.')
    
    parser.add_argument('--batch_size', '-b', type = int, default=512, help=\
        'batchSize, default=512.')

    parser.add_argument('--epoch', '-e', type = int, default=100, help=\
        'Number of learning epochs, default=1000.')

    parser.add_argument('--n_split', '-n', type = int, default=10, help=\
        'Validatio split, default=10.')

    args = parser.parse_args()

    main(args)
