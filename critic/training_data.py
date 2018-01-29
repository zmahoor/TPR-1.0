import numpy as np
import time
import sys
import pickle
import os

sys.path.append('../bots')
from database import DATABASE
from settings import *

num_features = 4
sequence_len = 100
main_path = "/Users/twitchplaysrobotics/TPR-backup"


class Training_Data:

    def __init__(self, commands, seed, sensor_drop_rate, mas_pos_samples, max_neg_samples):
        """

        :param commands:
        :param seed:
        :param sensor_drop_rate:
        :param mas_pos_samples:
        :param max_neg_samples:
        """
        np.random.seed(seed)
        self.commands = commands
        self.sensor_drop_rate = sensor_drop_rate
        self.max_pos_samples = mas_pos_samples
        self.max_neg_samples = max_neg_samples
        # connect to database
        self.mydatabase = DATABASE()

    def Load_Training_Data(self, morphology):
        """
            find all the evaluations for _MORPHOLOGY and commands with at least one reinforcement
            load the sensors for those evaluations
            extract features from the sequence of sensors
            :param mydatabase: OBJECT
            :return: numpy.array for input of the model and numpy.array for the output of the model
        """
        sql = """SELECT d.robotID, numYes, numNo, d.cmdTxt, startTime, cmdTxt from display as d JOIN
         robots as r ON d.robotID=r.robotID WHERE d.cmdTxt in """ + '(' + ",".join(
            ["'" + c + "'" for c in self.commands]) + ')' + " and r.type='%s' and (numYes+numNo)>0;" % morphology

        robots = self.mydatabase.execute_select_sql_command(sql, "Failed to retrieve record of a display...")
        print('Number of samples: ', len(robots), " Morphology: ", morphology, "Command: ", self.commands)

        np.random.shuffle(robots)
        sensor_input, output = [], []

        for robot in robots:
            sensors = self.Load_Sensors_From_File(robot)
            tfeatures = self.Extract_Features(sensors)

            obedience = float(robot['numYes'] - robot['numNo']) / float(robot['numYes'] + robot['numNo'])
            if robot['cmdTxt'] == 'stop': obedience *= -1
            # if -1 < obedience < +1: obedience = -1

            sensor_input.append(tfeatures)
            output.append(obedience)

        return np.array(sensor_input), np.array(output)

    def Clean_Up_Data(self, sensor_input, output):
        """

        :param sensor_input:
        :param output:
        :return:
        """
        dictionary_of_data = {}
        new_sensor_input = []
        new_output = []

        for i, sample in enumerate(sensor_input):

            sample = np.reshape(sample, (sequence_len * num_features), 1)
            sample = tuple(sample.tolist())

            if sample not in dictionary_of_data:
                dictionary_of_data[sample] = [0, 0]

            index = 1 if output[i] == +1 else 0
            dictionary_of_data[sample][index] += 1

        # print len(dictionary_of_data), dictionary_of_data.values()

        for key, val in dictionary_of_data.items():
            sample = np.array(key)
            sample = np.reshape(sample, (sequence_len, num_features), 1)

            # print sample.shape

            if val[0] == 0 and val[1] > 0:
                for i in range(val[1]):
                    if new_output.count(+1) < self.max_pos_samples:
                        new_sensor_input.append(sample)
                        new_output.append(+1)

            if val[0] > 0:
                for i in range(val[0]):
                    if new_output.count(-1) < self.max_pos_samples:
                        new_sensor_input.append(sample)
                        new_output.append(-1)

        # print np.histogram(np.array(new_output), bins=10)
        # print len(new_output), len(new_sensor_input)
        return new_sensor_input, new_output

    def Balance_Data(self, sensor_input, output, oversample=True):
        """
        Balance data by oversampling the under represented data points
        :param sensor_input: array
        :param output: array
        :param oversample: Boolean
        :return: Two numpy arrays
        """
        sensor_input, output = list(sensor_input), list(output)
        balanced_output, balanced_sensor_input = [], []

        print "Histogram of normalized reward before balance: ", np.histogram(np.array(output), bins=10)

        diff = self.max_pos_samples - output.count(+1)
        max_pos = min(output.count(+1), self.max_pos_samples)

        # re-sample positive samples
        pos_indices = [idx for idx in range(len(output)) if output[idx] == +1]
        keep_indices = np.random.choice(pos_indices, max_pos, replace=False)
        balanced_sensor_input.extend([sensor_input[idx] for idx in keep_indices])
        balanced_output.extend([+1 for _ in range(max_pos)])

        if balanced_output.count(+1) < self.max_pos_samples and oversample:
            extra_indices = np.random.choice(pos_indices, abs(diff))
            balanced_sensor_input.extend([sensor_input[idx] for idx in extra_indices])
            balanced_output.extend([+1 for _ in range(diff)])

        print "Histogram of normalized reward middle balance: ", np.histogram(np.array(balanced_output), bins=10)

        diff = self.max_neg_samples - output.count(-1)
        max_neg = min(output.count(-1), self.max_neg_samples)
        neg_indices = [idx for idx in range(len(output)) if output[idx] == -1]

        keep_indices = np.random.choice(neg_indices, max_neg, replace=False)
        balanced_sensor_input.extend([sensor_input[idx] for idx in keep_indices])
        balanced_output.extend([-1 for _ in range(max_neg)])

        # re-sample negative samples
        if balanced_output.count(-1) < self.max_neg_samples and oversample:
            extra_indices = np.random.choice(neg_indices, abs(diff))
            balanced_sensor_input.extend([sensor_input[idx] for idx in extra_indices])
            balanced_output.extend([-1 for _ in range(diff)])

        print "Histogram of normalized reward after balance: ", np.histogram(np.array(balanced_output), bins=10)

        return np.array(balanced_sensor_input), np.array(balanced_output)

    def Normalize_Data(self, model_input, model_output):
        """
        normalize the input and output features to [0,1]
        :param model_input: array
        :param model_output: array
        :return:
        """
        _min = np.min(np.min(model_input, axis=1), axis=0)
        _max = np.max(np.max(model_input, axis=1), axis=0)
        model_input = (model_input - _min) / (_max - _min)

        model_output = (model_output - np.min(model_output)) / (np.max(model_output) - np.min(model_output))
        print "Histogram of normalized reward after normalization: ", np.histogram(np.array(model_output), bins=10)

        return model_input, model_output

    def Load_Sensors_From_File(self, record):
        """
        return sensors for a robot's evaluation
        :param record: Dict
        :return: LIST[Dict]
        """
        robotID, startTime = record['robotID'], record['startTime']
        path = main_path + "/sensors/" + str(startTime.year) + "/" + str(startTime.month) + "/" + str(startTime.day) + \
            "/robot_" + str(robotID) + '_' + startTime.strftime("%Y-%m-%d-%H-%M-%S") + ".dat"

        if not os.path.isfile(path):
            print "Failed loading ", path
            return None
        sensors = self.Read_File(path)
        return sensors

    def Read_File(self, filePath):
        sensors = None
        try:
            with open(filePath, 'r') as f:
                sensors = pickle.load(f)
                # print "Loading ", filePath,
        except:
            print "Failed loading ", filePath

        return sensors

    def Propriceptive_Feature_Extraction(self, values):
        """
            Combine the proprioceptive features into one feature
            :param values: List[list[float]]
            :return: 2D numpy array
        """
        temp = []
        for row in values:
            temp.append(row[1::self.sensor_drop_rate])

        temp = np.array(temp).T
        temp = np.diff(temp, axis=0)
        temp = np.absolute(temp)
        temp = np.average(temp, axis=1)
        temp = np.hstack((temp, np.array(temp[-1])))
        return temp
        # return temp[1::self.sensor_drop_rate]

    def Position_Feature_Extraction(self, values):
        return values[1::self.sensor_drop_rate]

    def Extract_Features(self, sample):
        """
        extract features from a robot's sensors and return
        :param sample: DICT
        :return: 2D numpy array
        """
        prop = []
        posX, posY, posZ, features = None, None, None, None
        # print sample.keys()

        for key in sample.keys():
            if key.startswith('P') and key.endswith('_X'):
                posX = self.Position_Feature_Extraction(sample[key])

            elif key.startswith('P') and key.endswith('_Y'):
                posY = self.Position_Feature_Extraction(sample[key])

            elif key.startswith('P') and key.endswith('_Z'):
                posZ = self.Position_Feature_Extraction(sample[key])

            # proprioceptive sensor
            elif key.startswith('P'):
                prop.append(sample[key])

        prop = self.Propriceptive_Feature_Extraction(prop)

        # features = np.array([prop]).T
        # features = np.array([posX, posY]).T
        # features = np.array([posX, posY, posZ]).T
        features = np.array([posX, posY, posZ, prop]).T
        # features = np.average(features, axis=0)
        # features = np.reshape(features, (1, num_features))
        return features

