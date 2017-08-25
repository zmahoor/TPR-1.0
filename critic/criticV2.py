from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Input, Embedding, LSTM, Dense, Activation, concatenate
import keras 
from keras.models import load_model, save_model
from keras.callbacks import ModelCheckpoint

import numpy as np
import time
import matplotlib.pyplot as plt
import h5py
import sys 
import pickle
import os 
from datetime import datetime
import argparse

np.random.seed(1234)

sys.path.append('../bots')
sys.path.append('../pyrosim')

import constants as c
from database import DATABASE
from settings import *

SENSOR_DROP_RATE = 18
num_features     = 4
sequence_len     = c.evaluationTime/SENSOR_DROP_RATE
synthetic_data   = False

valid_commands   = {'move'}

main_path = "/Users/twitchplaysrobotics/TPR-backup"

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
        
        x = Dense(12, activation='relu')(dropout2)

        output = Dense(1, activation='linear', name='output')(x)

        self.model = Model(inputs=[sensor_input], outputs=[output])

        start = time.time()

        self.model.compile(optimizer='rmsprop', loss={'output': 'mse'},
            loss_weights={'output': 1.})

        self.checkpointer = ModelCheckpoint(filepath='model.h5', 
            verbose=1, save_best_only=True)
        
        print "Compilation Time : ", time.time() - start

    def train_model(self, data):

        sensors, obedience = data

        print sensors.shape, obedience.shape

        _min = np.min(np.min(sensors, axis=1), axis=0)
        _max = np.max(np.max(sensors, axis=1), axis=0)

        sensors = (sensors - _min) / (_max - _min)

        print "sensors range: ",
        print np.min(np.min(sensors, axis=1), axis=0),
        print np.max(np.max(sensors, axis=1), axis=0)

        _min = np.min(obedience)
        _max = np.max(obedience)

        obedience = (obedience - _min) / (_max - _min)

        # np.random.shuffle(obedience)

        print "obedience range: ",
        print np.min(obedience),
        print np.max(obedience)

        start_time = time.time()

        try:
            self.model.fit({'sensor_input': sensors}, {'output': obedience},
                epochs=self.params['epochs'], batch_size=self.params['batch_size'],
                validation_split=self.params['validation_split'], 
                callbacks=[self.checkpointer])

        except KeyboardInterrupt:
            print 'Training duration (s) : ', time.time() - start_time

        self.model.save('model.h5')  # creates a HDF5 file 'my_model.h5'

        print 'Training duration (s) : ', time.time() - start_time

    def predict(self, data):
        
        predicted = self.model.predict(data)
        predicted = np.reshape(predicted, (predicted.size,))

        print "predicted: ", predicted.shape
        
        return predicted

def Load_Training_Data(mydatabase):
    
    records = mydatabase.Fetch_From_Disply_Table('all_yes_or_no')

    print('Number of possible samples: ', len(records))

    if records == () or records == None: 
        print 'No data was found for critic.' 
        exit()

    sensor_input = []
    output       = []

    for record in records:

        command = record['cmdTxt']
        if command not in valid_commands: continue

        print command,
        sensors = Load_Sensors_From_File(record)
        if sensors == None: 
            # print('Not able to load the sensor file.') 
            continue

        features = Extract_Features( sensors )
        if features == None: continue

        tfeatures  = features[0]
        # print tfeatures.shape

        if tfeatures.shape != (sequence_len, num_features): 
            continue
        
        obedience  = float(record['numYes'] - record['numNo']) \
                            / float(record['numYes'] + record['numNo'])

        print tfeatures.shape, obedience

        sensor_input.append(tfeatures)
        output.append(obedience)

    return (np.array(sensor_input), np.array(output))

def Load_Sensors_From_File(record):

    robotID   = record['robotID']
    startTime = record['startTime']
    
    path = main_path + "/sensors/"+ str(startTime.year) + "/" + str(startTime.month)+\
        "/" + str(startTime.day)+ "/robot_" + str(robotID) + '_' +\
         startTime.strftime("%Y-%m-%d-%H-%M-%S") + ".dat"

    # print path

    if not os.path.isfile(path): 
        return None

    sensors = Read_File(path)

    return sensors

def Read_File(filePath):

    sensors = None

    try:
        with open(filePath, 'r') as f:
            sensors = pickle.load(f)
        print "Loading ", filePath,

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

    if len(prop) != 0:
        prop = Propriceptive_Feature_Extraction(prop)
    else: return None

    if len(touch) != 0:
        touch = Touch_Feature_Extraction(touch)
    else: return None

    # features = np.array([posX, posY, posZ, ray, touch, prop]).T

    features = np.array([posX, posY, posZ, prop]).T

    # features = np.array([touch]).T

    # print 'sensors: ', timeSeriedFeatures.shape

    return (features, True)

def main(args):
            
    batch_size = args.batch_size
    val_split  = args.val_split
    epoch      = args.epoch

    mydatabase = DATABASE()

    params = {'epochs':epoch, 'batch_size': batch_size,'validation_split':val_split}

    c = CRITIC(params)
    c.setup_model()

    data = Load_Training_Data( mydatabase )

    c.train_model(data)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Critic Model.')
    
    parser.add_argument('--batch_size', '-b', type = int, default=512, help=\
        'batchSize, default=512.')

    parser.add_argument('--epoch', '-e', type = int, default=1000, help=\
        'Number of learning epochs, default=1000.')

    parser.add_argument('--val_split', '-v', type = float, default=0.3, help=\
        'Validation split, default=0.3.')

    args = parser.parse_args()

    main(args)

