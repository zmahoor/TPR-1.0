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

SENSOR_DROP_RATE = 12
data_generation  = False
synthetic_data   = True

class CRITIC:

    def __init__(self, params):

        self.model = None
        self.params = params

    def setup_model(self):

        layers = self.params['layers']

        sensor_input = Input(shape=(150, 6), name='sensor_input')

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

    def train_model(self, mydatabase):

        if not data_generation:

            print('Not using data generation...')

            if synthetic_data:
                print('Generate synthetic data.')
                data = Generate_Synthetic_Data( 10000 )
            else:
                data = Load_Training_Data( mydatabase )    

            sensors, wordToVec, obedience = data

            print "range: "
            print np.min(np.min(sensors, axis=1), axis=0)
            print np.max(np.max(sensors, axis=1), axis=0)

            sensors = self.normalize_data( sensors )

            print "range: "
            print np.min(np.min(sensors, axis=1), axis=0)
            print np.max(np.max(sensors, axis=1), axis=0)

            print wordToVec.shape, sensors.shape, obedience.shape

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
                self.model.fit_generator(Generate_Data(10, mydatabase), steps_per_epoch=10, epochs=5)
            except Exception as e:
                print str(e)

        self.model.save('critic_model.h5')  # creates a HDF5 file 'my_model.h5'

        print 'Training duration (s) : ', time.time() - start_time

    def normalize_data(self, data):

        self._min = np.min(np.min(data, axis=1), axis=0)
        self._max  = np.max(np.max(data, axis=1), axis=0)

        return (data - self._min) / (self._max - self._min)

    def predict(self, data):
        
        predicted = self.model.predict(data)
        predicted = np.reshape(predicted, (predicted.size,))

        print "predicted: ", predicted.shape
        
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

def Delete_Sensor_File(record):

    robotID   = record['robotID']
    startTime = record['startTime']
    
    path = "../sensors/"+ str(startTime.year) + "/" + str(startTime.month)+\
        "/" + str(startTime.day)+ "/robot_" + str(robotID) + '_' +\
         startTime.strftime("%Y-%m-%d %H:%M:%S") + ".dat"

    print path

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

            Delete_Sensor_File(record)

def Generate_Data(batch_size, mydatabase):
    
    records = mydatabase.Fetch_From_Disply_Table('all_yes_or_no')

    print('Number of possible samples: ', len(records))

    if records == () or records == None: 
        print 'No data was found for critic.' 
        exit()

    sensor_input = []
    word_input   = []
    output       = []
    numSamples   = 0

    while True:

        for record in records:

            sensors = Load_Sensors_From_File(record)
            if sensors == None: 
                # print('Not able to load the sensor file.') 
                continue

            features = Extract_Features( sensors )
            if features == None: 
                continue

            tfeatures  = features[0]
            if tfeatures.shape != (c.evaluationTime/SENSOR_DROP_RATE, 6): 
                continue
            
            obedience = float(record['numYes'] - record['numNo']) \
                                / float(record['numYes'] + record['numNo'])

            if 'wordToVec' in record.keys(): 
                ntfeatures = record['wordToVec']
            else: ntfeatures = 0.0

            sensor_input.append(tfeatures)
            word_input.append(ntfeatures)
            output.append(obedience)

            numSamples = numSamples + 1
            
            if numSamples == batch_size:
                
                print numSamples, len(sensor_input), len(word_input), len(output)

                yield ({'sensor_input': np.array(sensor_input),\
                       'word_input': np.array(word_input)},\
                       {'output': np.array(output)})

                sensor_input = []
                word_input   = []
                output       = []
                numSamples   = 0

def Load_Training_Data(mydatabase):
    
    records = mydatabase.Fetch_From_Disply_Table('all_yes_or_no')

    print('Number of possible samples: ', len(records))

    if records == () or records == None: 
        print 'No data was found for critic.' 
        exit()

    sensor_input = []
    word_input   = []
    output       = []

    for record in records:

        sensors = Load_Sensors_From_File(record)
        if sensors == None: 
            # print('Not able to load the sensor file.') 
            continue

        features = Extract_Features( sensors )
        if features == None: continue

        tfeatures  = features[0]
        if tfeatures.shape != (c.evaluationTime/SENSOR_DROP_RATE, 6): continue
        
        obedience  = float(record['numYes'] - record['numNo']) \
                            / float(record['numYes'] + record['numNo'])

        if 'wordToVec' in record.keys(): 
            ntfeatures = record['wordToVec']
        else: ntfeatures = 0.0

        sensor_input.append(tfeatures)
        word_input.append(ntfeatures)
        output.append(obedience)

    return (np.array(sensor_input), np.array(word_input), np.array(output))

def Load_Sensors_From_File(record):

    robotID   = record['robotID']
    startTime = record['startTime']
    
    path = "../sensors/"+ str(startTime.year) + "/" + str(startTime.month)+\
        "/" + str(startTime.day)+ "/robot_" + str(robotID) + '_' +\
         startTime.strftime("%Y-%m-%d %H:%M:%S") + ".dat"

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
        print "Successful loading ", filePath
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

    features = np.array([posX[:], posY, posZ, ray, touch, prop]).T

    # print 'sensors: ', timeSeriedFeatures.shape

    return (features, True)

def Generate_Synthetic_Data( num_samples ):

    num_features   = 6
    num_time_steps = 150

    sensors    = 2*np.random.rand( num_samples, num_time_steps, num_features)-1
    word_input = np.random.rand(num_samples, 1)
    obedience  = 2*np.random.rand(num_samples, 1)-1
    
    return (sensors, word_input, obedience)

def main(argv):
    
    if synthetic_data == False:
        mydatabase = DATABASE()
    else: mydatabase = None

    params = {'epochs':1, 'batch_size': 512, 'layers':[1, 32, 64, 1],\
    'validation_split':0.05}

    c = CRITIC(params)
    c.setup_model()
    c.train_model(mydatabase)

    if synthetic_data:
        testing_data = Generate_Synthetic_Data(100)

        sensors = (testing_data[0] - c._min) / (c._max - c._min)

        print "range: "
        print np.min(np.min(sensors, axis=1), axis=0)
        print np.max(np.max(sensors, axis=1), axis=0)

        print c.predict( {'sensor_input': sensors, 'word_input': testing_data[1]})

        score = c.model.evaluate({'sensor_input': sensors,\
            'word_input': testing_data[1]}, {'output': testing_data[2]},\
            batch_size=32, verbose=1, sample_weight=None)

        print c.model.metrics_names, score

if __name__ == "__main__":
    main(sys.argv[1:])

