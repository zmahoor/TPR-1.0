from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Input, Embedding, LSTM, Dense, Activation, concatenate
import keras 
from keras.models import load_model, save_model
import numpy as np
import time
import matplotlib.pyplot as plt
import h5py
import sys 
import pickle
import os 
import constants as c
from datetime import datetime
import argparse

np.random.seed(1234)

sys.path.append('../bots')

from database import DATABASE
from settings import *

SENSOR_DROP_RATE  = 6
# mydatabase = DATABASE()

class CRITIC:

    def __init__(self, params):

        self.model = None
        self.params = params

    def setup_model(self):

        layers = self.params['layers']

        sensor_input = Input(shape=(30, 6), name='sensor_input')

        lstm1    = LSTM(12, return_sequences=True)(sensor_input)
        dropout1 = Dropout(0.2)(lstm1)

        lstm2    = LSTM(12, return_sequences=True)(dropout1)
        dropout2 = Dropout(0.2)(lstm2)

        lstm3    = LSTM(12, return_sequences=False)(dropout2)
        dropout3 = Dropout(0.2)(lstm3)
        
        word_input = Input(shape=(1,), name='word_input')
        x = keras.layers.concatenate([dropout3, word_input])

        x = Dense(12, activation='relu')(x)
        x = Dense(12, activation='relu')(x)
        x = Dense(12, activation='relu')(x)

        output = Dense(1, activation='linear', name='output')(x)

        self.model = Model(inputs=[sensor_input, word_input], outputs=[output])

        start = time.time()

        self.model.compile(optimizer='rmsprop', loss={'output': 'mse'},
            loss_weights={'output': 1.})
        
        print "Compilation Time : ", time.time() - start

    def train_model(self, data):

        wordToVec, sensors, obedience = data
        print wordToVec.shape, sensors.shape, obedience.shape
                
        if not data_generation:

            print('Not using data generation...')

            start_time = time.time()
            try:
                self.model.fit({'sensor_input': sensors, 'word_input': wordToVec},
                    {'output': obedience},
                    epochs=self.params['epochs'], batch_size=self.params['batch_size'],
                    validation_split=self.params['validation_split'])

            except KeyboardInterrupt:
                print 'Training duration (s) : ', time.time() - start_time
        else:

            print('Using data generation...')
            start_time = time.time()
            try:
                self.model.fit_generator(Generate_Data(), steps_per_epoch=10000, epochs=10)
            except Exception as e::
                print str(e)

        self.model.save('critic_model.h5')  # creates a HDF5 file 'my_model.h5'

        print 'Training duration (s) : ', time.time() - start_time

    def predict(self, data):
        
        wordToVec, sensors, obedience = data
        print wordToVec.shape, sensors.shape, obedience.shape

        predicted = self.model.predict({'sensor_input': sensors, 'word_input': wordToVec})
        predicted = np.reshape(predicted, (predicted.size,))

        print predicted.shape
        
        # self.plot_results(obedience, predicted)

        return predicted

    def plot_results(self, y_test, predicted):

        assert y_test.shape == predicted.shape

        x = 200
        try:

            fig, ax = plt.subplots()
            line1,  = ax.plot(y_test, '-', linewidth=2,
                 label='True obedience')

            line2,  = ax.plot(predicted, '-', linewidth=2,
                 label='Predicted obedience')

            ax.legend(loc='upper right')
            plt.show()

        except Exception as e:
            print str(e)

def Delete_Sensor_File(startTime):

    startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")

    path = "../sensors/"+ str(currentTime.year) + "/" + str(currentTime.month)+\
        "/" + str(currentTime.day)

    if not os.path.isfile(path): return

    try:
        os.remove(fileToBeRemoved)
    except:
        print "unable to remove this file.."

def Delete_Useless_Sensor_Files():

    records = mydatabase.Fetch_From_Disply_Table('all')

    for record in records:

        if record['numYes'] == 0 and record['numNo'] == 0 and \
            record['numLike'] ==0 and record['numDislike'] == 0:

            print 'zero feedback...removing it.'

            startTime = record['startTime']
            Delete_Sensor_File(startTime)

def Generate_Data():
    while 1:
    records = mydatabase.Fetch_From_Disply_Table('all')

    if records == (): 
        print 'No data was found for critic.' 
        exit()

    for record in records:
        if record['numYes'] == 0 and record['numNo'] == 0:
            continue

        record['obedience'] = float(record['numYes'] - record['numNo']) \
                            / float(record['numYes'] + record['numNo'])

        # remove unnecessary keys.
        map(record.pop, ['numLike','numDislike', 'numNo', 'numYes'])

        startTime = record['startTime']
        sensors   = Load_Sensors_From_File(startTime)

        output = record['obedience']
        tfeatures, ntfeatures = Extract_Features( dict(sensors.items() + record.items() ))

        yield ({'sensor_input': tfeatures, 'word_input': ntfeatures}, {'output': output})

def Load_Sensors_From_File(startTime):
    
    startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")

    path = "../sensors/"+ str(startTime.year) + "/" + str(startTime.month)+\
        "/" + str(startTime.day)

    if not os.path.isfile(path): return None

    sensors = Read_File(path)

    return sensors

def Read_File(filePath):

    sensors = None

    try:
        with open(filePath, 'r') as f:
            sensors = pickle.load(f)
        print "Successful loading ", filePath
    except:
        print "Failed loading ", filePath 
    
    return sensors

def Propriceptive_Feature_Extraction(values):

    values = np.array(values).T

    temp   = np.diff(values, axis=0)
    # print "joint features: ", temp.shape

    temp   = np.average(temp, axis=1)
    # print "joint features: ", temp[-1],temp.shape

    temp   = np.hstack((temp, np.array(temp[-1])))
    # print "joint features: ", temp.shape

    return temp[1::SENSOR_DROP_RATE]

def Ray_Feature_Extraction(values):
    
    return values[1::SENSOR_DROP_RATE]

def Position_Feature_Extraction(values):

    return values[1::SENSOR_DROP_RATE]

def Touch_Feature_Extraction(values):

    values = np.array(values).T
    # print 'touch features:', values.shape

    temp   = np.average(values, axis=1)
    # print 'touch features:', temp.shape

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
            # print key, sample[key].shape
            posX = Position_Feature_Extraction(sample[key])
        
        # position_y sensor
        elif key.startswith('P') and key.endswith('_Y'):
            # print key, sample[key].shape
            posY = Position_Feature_Extraction(sample[key])

        # position_z sensor
        elif key.startswith('P') and key.endswith('_Z'):
            # print key, sample[key].shape
            posZ = Position_Feature_Extraction(sample[key])

        # touch sensor
        elif key.startswith('T'):
            # print key, sample[key].shape
            touch.append(sample[key])

        # ray sensor 
        elif key.startswith('R0'):
            # print key, sample[key].shape
            ray = Ray_Feature_Extraction(sample[key])

        # propriceptive sensor
        elif key.startswith('P'):
            # print key, sample[key].shape
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

    return (timeSeriedFeatures, nonTimedSeriedFeatures)

def make_sudo_data(num_samples=10000):
    num_dim     = 6
    time_steps  = 30
    words       = [0.5, 0.7]

    wordToVec  = [ words[np.random.randint(len(words))] for i in range(num_samples) ]
    sensors    = 2*np.random.rand(num_samples, time_steps, num_dim) - 1
    obedience  = np.random.rand(num_samples)

    return np.array(wordToVec), sensors, obedience

def main():
    # Delete_Useless_Sensor_Files()

    # Genereate_Data(records)

    params = {'epochs':1, 'batch_size': 512, 'layers':[1, 32, 64, 1],\
    'validation_split':0.05}

    training_data = make_sudo_data(1000)
    testing_data  = make_sudo_data(200)

    c = CRITIC(params)
    c.setup_model()
    c.train_model(training_data)

    predicted = c.predict(testing_data)


main()

