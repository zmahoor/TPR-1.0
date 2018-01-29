import numpy as np
import sys
import pickle
import os
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt
from time import time

from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA as PCA

sys.path.append('../bots')
sys.path.append('../pyrosim')

from database import DATABASE
from settings import *

X_LABEL = "Principle Components"
# X_LABEL = 'Average Change in Head Location'
# X_LABEL = 'Average Change in Joint Position'
# X_LABEL = 'Absolute Head Displacement'

DROP_RATE = 18
POS_SAMPLES = 100
main_path = "/Users/twitchplaysrobotics/TPR-backup"
commands = {'move', 'stop'}

seed = 1234
np.random.seed(seed)

names = {'3': 'branchbot', '4': 'treebot', 'quadruped': 'quadruped', 'starfishbot':'starfishbot',
         'spherebot':'spherebot', 'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot'}

# names = {'starfishbot':'starfishbot'}

mydatabase = DATABASE()


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


def Data_For_PCA(sample):
    pass

def Propriceptive_Feature_Extraction(values):
    temp = []
    for row in values:
        temp.append(row[1::DROP_RATE])
    temp = np.array(temp).T
    temp = np.diff(temp, axis=0)
    temp = np.absolute(temp)
    temp = np.average(temp, axis=1)
    temp = np.hstack((temp, np.array(temp[-1])))
    return temp
    # return np.average(temp)


def Get_Head_Location(sample):
    posX, posY, posZ = None, None, None
    for key in sample.keys():
        if key.startswith('P') and key.endswith('_X'):
            posX = sample[key][1::DROP_RATE]
            # posX = sample[key]

        elif key.startswith('P') and key.endswith('_Y'):
            posY = sample[key][1::DROP_RATE]
            # posY = sample[key]

        elif key.startswith('P') and key.endswith('_Z'):
            posZ = sample[key][1::DROP_RATE]
            # posZ = sample[key]

    features = np.array([posX, posY, posZ]).T
    return features
    # return np.linalg.norm(features[1786, :]-features[0, :])


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
    return posX
    # return np.linalg.norm([posX, posY])


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

    # np.random.shuffle(robots)

    Y, X = [], []
    for robot in robots:
        sensors = Load_Sensors_From_File(robot)

        obedience = float(robot['numYes']-robot['numNo'])/float(robot['numYes']+robot['numNo'])

        if robot['cmdTxt'] == 'stop': obedience *= -1
        if -1 < obedience < +1: continue
        if obedience == +1 and Y.count(+1) >= POS_SAMPLES: continue

        if X_LABEL == 'Average Change in Head Location':
            X.append(Get_Average_Change_Head_Location(sensors))

        elif X_LABEL == 'Average Change in Joint Position':
            X.append(Get_Propriceptive_Change(sensors))

        elif X_LABEL == 'Absolute Head Displacement':
            X.append(Get_Head_Location(sensors))

        else:
            temp1 = Get_Propriceptive_Change(sensors)
            temp2 = Get_Head_Location(sensors).T
            temp2 = temp2.flatten()
            final = np.concatenate((temp1, temp2), axis=0)
            # print final.shape, temp1.shape, temp2.shape
            X.append(final)

        Y.append(obedience)

    return X, Y


def Balance_Data(X, Y):
    """
        Balance data by oversampling the under represented data points
        :param sensor_input: LIST
        :param output: List
        :return: Two Lists
    """
    # count negative and positive samples
    neg_count, pos_count = Y.count(-1), Y.count(+1)
    diff = abs(neg_count - pos_count)

    counts, bins = np.histogram(np.array(Y), bins=10)
    print bins, counts

    # re-sample positive samples if number of negative samples are larger than the positive ones
    if neg_count > pos_count:
        extra_indices = np.random.choice([idx for idx in range(len(Y)) if Y[idx] == +1], diff)
        X.extend([X[idx] for idx in extra_indices])
        Y.extend([+1 for _ in range(diff)])

    # re-sample negative samples if number of positive samples are more than the negative ones
    elif neg_count < pos_count:
        extra_indices = np.random.choice([idx for idx in range(len(Y)) if Y[idx] == -1], diff)
        X.extend([X[idx] for idx in extra_indices])
        Y.extend([-1 for _ in range(diff)])

    counts, bins = np.histogram(np.array(Y), bins=10)
    print bins, counts
    return X, Y


def draw_plots():
    fig, axes = plt.subplots(figsize=(20, 10), ncols=4, nrows=2)
    ax = axes.flatten()
    ax[0].set_ylabel("Normalized Reinforcement Signals")
    ax[6].set_xlabel(X_LABEL)

    i = 0
    for key, val in names.items():
        X, Y = Load_Data(mydatabase, key)
        Balance_Data(X, Y)
        Y = (Y - np.min(Y)) / (np.max(Y) - np.min(Y))
        sns.regplot(x=np.array(X), y=np.array(Y), color="g", ax=ax[i], logistic=True, y_jitter=.03, n_boot=500)
        # sns.distplot(Y, bins=20, color="g", ax=ax[i])
        ax[i].set_title(val)
        i = i+1
        # plt.title('Histogram of Final Head Position)

    # plt.savefig(X_LABEL+'_hist.jpg', format='jpg', dpi=100)
    plt.show()


def pca():
    fig, axes = plt.subplots(figsize=(20, 10), ncols=4, nrows=2)
    ax = axes.flatten()
    ax[0].set_ylabel("The Second Principal Component")
    ax[4].set_ylabel("The Second Principal Component")

    ax[4].set_xlabel("The First Principal Component")
    ax[5].set_xlabel("The First Principal Component")
    ax[6].set_xlabel("The First Principal Component")
    ax[7].set_xlabel("The First Principal Component")

    j = 0
    for key, val in names.items():
        X, Y = Load_Data(mydatabase, key)
        Balance_Data(X, Y)

        X_std = StandardScaler().fit_transform(X)
        sklearn_pca = PCA(n_components=4)
        X_sklearn = sklearn_pca.fit_transform(X_std)

        print sklearn_pca.explained_variance_, sklearn_pca.explained_variance_ratio_

        # for eigenvector in sklearn_pca.components_:
        #     print eigenvector

        pca1_pos, pca2_pos = [], []
        pca1_neg, pca2_neg = [], []

        for i in range(len(Y)):
            if Y[i] == +1:
                pca1_pos.append(X_sklearn[i, 2])
                pca2_pos.append(X_sklearn[i, 3])
            else:
                pca1_neg.append(X_sklearn[i, 2])
                pca2_neg.append(X_sklearn[i, 3])

        ax[j].scatter(pca1_pos, pca2_pos, color='r', label='Positive Reward')
        ax[j].scatter(pca1_neg, pca2_neg, color='g', label='Negative Reward')
        ax[j].set_title(val)
        ax[j].legend(loc=1)
        j = j+1
        print

    plt.show()


def plot_data():
    fig, axes = plt.subplots(figsize=(20, 10), ncols=4, nrows=2)
    ax = axes.flatten()
    ax[0].set_ylabel("The L2 of Head Trajectory")
    ax[4].set_ylabel("The L2 of Head Trajectory")

    ax[4].set_xlabel("The L2 of Change in Joints")
    ax[5].set_xlabel("The L2 of Change in Joints")
    ax[6].set_xlabel("The L2 of Change in Joints")
    ax[7].set_xlabel("The L2 of Change in Joints")

    j = 0
    for key, val in names.items():
        X, Y = Load_Data(mydatabase, key)
        Balance_Data(X, Y)

        newX =[(np.linalg.norm(elem[0:100]), np.linalg.norm(elem[100:400])) for elem in X]

        pca1_pos, pca2_pos = [], []
        pca1_neg, pca2_neg = [], []

        for i in range(len(Y)):
            if Y[i] == +1:
                pca1_pos.append(newX[i][0])
                pca2_pos.append(newX[i][1])
            else:
                pca1_neg.append(newX[i][0])
                pca2_neg.append(newX[i][1])

        ax[j].scatter(pca1_pos, pca2_pos, color='r', label='Positive Reward', alpha=0.5, s=50)
        ax[j].scatter(pca1_neg, pca2_neg, color='g', label='Negative Reward', alpha=0.5, s=50)
        ax[j].set_title(val)
        ax[j].legend(loc=1)
        # ax[j].set_xlim([-0.1, 18.0])
        j = j + 1
        print

    plt.show()


def count_duplicates():

    for key, val in names.items():
        X, Y = Load_Data(mydatabase, key)
        # Balance_Data(X, Y)

        pos_dublicates = 0
        neg_dublicates = 0
        unique_neg = 0
        unique_pos = 0
        cross_category_overlap = 0

        histogram = {}

        for i in range(len(X)):
            sample = tuple(X[i])

            if sample not in histogram:
                histogram[sample] = [0, 0]

            index = 1 if Y[i] == +1 else 0
            histogram[sample][index] += 1


        for sample, reward in histogram.items():
            if reward[0] > 0 and reward[1] > 0:
                cross_category_overlap += 1

            if reward[0] == 0 and reward[1] > 0:
                unique_pos += 1

            if reward[0] > 0 and reward[1] == 0:
                unique_neg += 1

        print val, len(histogram), unique_neg, unique_pos, cross_category_overlap, histogram.values()
        print

        # print len(X)
        # for i in range(len(X)):
        #     pos_flag = False
        #     neg_flag = False
        #     cross_flag = False
        #     for j in range(i+1, len(X)):
        #         # print i, j, Y[i], Y[j], X[i].shape, X[j].shape
        #         if Y[i] == Y[j] == +1 and np.array_equal(X[i], X[j]) and not pos_flag:
        #             pos_dublicates += 1
        #             pos_flag = True
        #         if Y[i] == Y[j] == -1 and np.array_equal(X[i], X[j]) and not neg_flag:
        #             neg_dublicates += 1
        #             neg_flag = True
        #         if Y[i] != Y[j] and np.array_equal(X[i], X[j]) and not cross_flag:
        #             cross_category_overlap += 1
        #             cross_flag = True
        #
        # print key, pos_dublicates, neg_dublicates, cross_category_overlap

def kmean_test():

    data, labels = Load_Data(mydatabase, '4')
    Balance_Data(data, labels)

    data = scale(np.array(data))

    n_samples, n_features = data.shape
    n_digits = len(np.unique(labels))

    def bench_k_means(estimator, name, data):
        t0 = time()
        estimator.fit(data)
        print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
              % (name, (time() - t0), estimator.inertia_,
                 metrics.homogeneity_score(labels, estimator.labels_),
                 metrics.completeness_score(labels, estimator.labels_),
                 metrics.v_measure_score(labels, estimator.labels_),
                 metrics.adjusted_rand_score(labels, estimator.labels_),
                 metrics.adjusted_mutual_info_score(labels, estimator.labels_),
                 metrics.silhouette_score(data, estimator.labels_,
                                          metric='euclidean',
                                          sample_size=n_samples)))

    bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
                  name="k-means++", data=data)

    bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),
                  name="random", data=data)

    # in this case the seeding of the centers is deterministic, hence we run the
    # kmeans algorithm only once with n_init=1
    pca = PCA(n_components=n_digits).fit(data)
    bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),
                  name="PCA-based",
                  data=data)
    print(82 * '_')

    # #############################################################################
    # Visualize the results on PCA-reduced data

    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02  # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'ko', markersize=8)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()

# kmean_test()
# pca()
# plot_data()
count_duplicates()