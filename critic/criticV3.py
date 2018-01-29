from sklearn.model_selection import KFold
from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Input, Embedding, LSTM, Dense, Activation
import keras 
from datetime import datetime
from copy import deepcopy

import numpy as np
import time
import sys
import argparse
from scipy.stats.stats import ttest_ind
from keras import backend as K
import tensorflow as tf
import csv

from training_data import Training_Data

seed = 1234
# seed = 5678
np.random.seed(seed)

SENSOR_DROP_RATE = 18
num_features = 4
sequence_len = 100
MAX_POS_SAMPLES = 100
MAX_NEG_SAMPLES = 75
BALANCE_DATA = True

names = {'1': 'stickbot', '2': 'twigbot', '3': 'branchbot', '4': 'treebot', 'quadruped': 'quadruped',
         'starfishbot':'starfishbot', 'spherebot':'spherebot', 'shinbot': 'tablebot', 'snakebot':'snakebot',
         'crabbot': 'crabbot'}


class CRITIC:

    def __init__(self, params):
        self.model = None
        self.params = params

    def setup_model(self):
        """
            setup a model with desired configuration, loss function, and optimizer
            :return: model
        """
        sensor_input = Input(shape=(sequence_len, num_features), name='sensor_input')
        lstm1 = LSTM(12, return_sequences=True)(sensor_input)
        dropout1 = Dropout(0.2)(lstm1)
        lstm2 = LSTM(12, return_sequences=False)(dropout1)
        dropout2 = Dropout(0.2)(lstm2)
        output = Dense(1, activation='relu', name='output')(dropout2)
        model = Model(inputs=[sensor_input], outputs=[output])
        model.compile(optimizer='rmsprop', loss={'output': 'mse'}, loss_weights={'output': 1.}, metrics=['mae'])

        return model

    def train_model(self, sensors, obedience):
        """
            :param sensors: numpy.array(sequence of inputs)
            :param obedience: float
            :return: two numpy.arrays
        """
        cv_scores, pcv_scores = [], []

        # split the input data to k sections for training
        kfold = KFold(n_splits=self.params['n_split'], shuffle=True, random_state=seed)

        # for each training and testing datasets
        for train, test in kfold.split(sensors, obedience):
            start_time = time.time()
            model = self.setup_model()

            # train the model
            model.fit({'sensor_input': sensors[train]}, {'output': obedience[train]},
                      epochs=self.params['epochs'], batch_size=self.params['batch_size'], verbose=0)

            # test the model with non-permuted reinforcement
            scores = model.evaluate(sensors[test], obedience[test], verbose=0)

            # print 'Training duration (s) : ', time.time() - start_time,
            print "Regular Test: %s: %.4f"%(model.metrics_names[1], scores[1]),
            cv_scores.append(scores[1])

            # test the model with permuted reinforcement
            random_obedience = deepcopy(obedience[test])
            np.random.shuffle(random_obedience)
            pscores = model.evaluate(sensors[test], random_obedience, verbose=0)

            print "Permuted Test: %s: %.4f"%(model.metrics_names[1], pscores[1])
            pcv_scores.append(pscores[1])

        print("Regular Test: %.3f (+/- %.3f)" % (np.mean(cv_scores), np.std(cv_scores)))
        print("Permuted Test: %.3f (+/- %.3f)" % (np.mean(pcv_scores), np.std(pcv_scores)))
        print("Ttest simple Exp. vs Permuted", ttest_ind(cv_scores, pcv_scores))

        return pcv_scores, cv_scores


def custom_loss(y_true, y_pred):
    """
        :param y_true: target output
        :param y_pred: predicted oputput
        :return: tensors
    """
    pos_y_true = tf.gather(y_true, tf.where(tf.equal(y_true, +1)))
    pos_y_pred = tf.gather(y_pred, tf.where(tf.equal(y_true, +1)))
    pos_count = tf.reduce_sum(tf.cast(tf.equal(y_true, +1), tf.float32))

    neg_y_true = tf.gather(y_true, tf.where(tf.less(y_true, +1)))
    neg_y_pred = tf.gather(y_pred, tf.where(tf.less(y_true, +1)))
    neg_count = tf.reduce_sum(tf.cast(tf.less(y_true, +1), tf.float32))

    first_sum = tf.div(tf.reduce_sum(tf.abs(tf.subtract(pos_y_true, pos_y_pred))), 2.0*pos_count)
    second_sum = tf.div(tf.reduce_sum(tf.abs(tf.subtract(neg_y_true, neg_y_pred))), 2.0*neg_count)

    return (first_sum + second_sum) / 2.0


def main(args):
    """
        create the prediction models for each robot morphology
        :param args:
        :return:
    """

    batch_size, n_split, epoch = args.batch_size, args.n_split, args.epoch

    exp_name = '_'.join([str(n_split)+"fold", str(MAX_POS_SAMPLES)+"pos", str(MAX_NEG_SAMPLES)+"neg", "balance"+str(BALANCE_DATA)])

    commands = {'move', 'stop'}
    params = {'epochs': epoch, 'batch_size': batch_size, 'n_split': n_split}

    outfile_regular = open("critic_results_regular_"+exp_name+".csv", "w")
    outfile_permuted = open("critic_results_permuted_"+exp_name+".csv", "w")

    writer_regular = csv.writer(outfile_regular, delimiter=",")
    writer_permuted = csv.writer(outfile_permuted, delimiter=",")

    writer_permuted.writerow(['trials'] + map(str, range(n_split)))
    writer_regular.writerow(['trials'] + map(str, range(n_split)))

    c = CRITIC(params)
    td = Training_Data(commands, seed, SENSOR_DROP_RATE, MAX_POS_SAMPLES, MAX_NEG_SAMPLES)

    # for each morphology train and store the results
    for morphology, val in names.items():

        # load training data from file and database for key
        sensors, obedience = td.Load_Training_Data(morphology)
        sensors, obedience = td.Balance_Data(sensors, obedience, BALANCE_DATA)
        sensors, obedience = td.Normalize_Data(sensors, obedience)

        hist = np.histogram(np.array(obedience), bins=10)
        if hist[0][0] < MAX_NEG_SAMPLES or hist[0][9] < MAX_POS_SAMPLES:
            print "not enough data\n"
            continue

        print morphology, "Training size: ", sensors.shape, obedience.shape

        print
        continue

        # train with input=sensors and output=obedience
        pcv_scores, cv_scores = c.train_model(sensors, obedience)
        writer_permuted.writerow([val] + map(str, pcv_scores))
        writer_regular.writerow([val] + map(str, cv_scores))
        print

    outfile_regular.close()
    outfile_permuted.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Critic Model.')
    parser.add_argument('--batch_size', '-b', type=int, default=512, help='batchSize, default=512.')
    parser.add_argument('--epoch', '-e', type=int, default=100, help='Number of learning epochs, default=1000.')
    parser.add_argument('--n_split', '-n', type=int, default=10, help='Validation split, default=30.')
    args = parser.parse_args()
    main(args)
