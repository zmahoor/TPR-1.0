# population of individuals for novelty search
from pyrosim import PYROSIM
import numpy as np
from individual import INDIVIDUAL
from sys import float_info
import pickle
from copy import deepcopy
from numpy import linalg as LA
import constants as c


class POPULATION:

    def __init__(self, ps, robotType):
        self.p = {}
        self.popSize = ps
        self.robotType = robotType

        for i in range(0, self.popSize):
            self.p[i] = INDIVIDUAL(i, robotType) 
    
    def Print(self):
        for i in self.p:
            self.p[i].Print()
        print

    def Sensors_Have_Changed(self, sensorDict):
        """
        return false if none of the sensors have changed at the last two time steps of evaluation
        else return true
        :param sensorDict: dict[array]
        :return: bool
        """
        for sensorValue in sensorDict.values():
            if np.absolute(sensorValue[-1] - sensorValue[-2]) != 0:
                return True
        return False

    def Evaluate_Internal_Novelty(self, pp, pb):
        """
        evaluate each individual in the population
        :param pp: bool
        :param pb: bool
        :return:
        """
        tempSensors = {}
        # for each individual initialize an empty list
        for i in self.p: 
            tempSensors[i] = []

        # evaluate each individual twice: once with word input -1 and once with +1
        for b in [-1, +1]:

            # start evaluating each robot under a given word
            for i in self.p:
                self.p[i].Start_Evaluate(pp, pb, c.NUM_BIAS_NEURONS*[1.0]+[b] if c.NUM_BIAS_NEURONS > 0 else [b])

            # wait for the evaluations to end
            for i in self.p:
                self.p[i].Wait_For_Me()

            # collect sensor data
            for i in self.p:
                tempSensors[i].append(self.p[i].Get_Raw_Sensors())

        # calculate the fitness for all of them
        self.Compute_Fitness(tempSensors)

    def Compute_Fitness(self, tempSensors):
        """
        compute and update the fitness of each individual within the population p
        :param tempSensors: dict[List]
        :return: none
        """
        for i in self.p:
            # raw sensors gathered for the evaluation with word -1
            neg_One_Sensors = tempSensors[i][0]

            # raw sensors gathered for the evaluation with word +1
            pos_One_Sensors = tempSensors[i][1]

            self.p[i].fitness = 0

            # if the sensors of both evaluations have changed at the last two steps
            if self.Sensors_Have_Changed(neg_One_Sensors) and self.Sensors_Have_Changed(pos_One_Sensors):
                    head_x = [key for key in neg_One_Sensors if key.endswith("_X")][0]
                    head_y = [key for key in neg_One_Sensors if key.endswith("_Y")][0]
                    head_z = [key for key in neg_One_Sensors if key.endswith("_Z")][0]

                    neg_One_Head_Traj = np.hstack((neg_One_Sensors[head_x], neg_One_Sensors[head_y],
                                                   neg_One_Sensors[head_z]))

                    head_x = [key for key in pos_One_Sensors if key.endswith("_X")][0]
                    head_y = [key for key in pos_One_Sensors if key.endswith("_Y")][0]
                    head_z = [key for key in pos_One_Sensors if key.endswith("_Z")][0]

                    pos_One_Head_Traj = np.hstack((pos_One_Sensors[head_x], pos_One_Sensors[head_y],
                                                   pos_One_Sensors[head_z]))

                    # fitness = Euclidean distance between the head trajectories
                    self.p[i].fitness = LA.norm(neg_One_Head_Traj - pos_One_Head_Traj)

    def Mutate(self):
        for i in self.p:
            self.p[i].Mutate()

    def Replace_With(self, other):
        for i in self.p:
            if self.p[i].fitness < other.p[i].fitness:
                self.p[i] = other.p[i]

    def Store_All(self):
        for i in self.p:
            self.p[i].Store_To_Diversity_Pool()

    def Find_Best(self):
        best = -float('inf')
        best_index = -1
        for i in self.p:
            if self.p[i].fitness > best:
                best = self.p[i].fitness
                best_index = i
        return best_index

    def Kill_And_Replace(self, index):
        del self.p[index]
        self.p[index] = INDIVIDUAL(index, self.robotType)

    def Store_All_Above_Average(self):
        avg = 0.0
        for i in self.p:
            avg += self.p[i].fitness
        avg /= float(self.popSize)

        print "average fitness: ", avg
        for i in self.p:
            if self.p[i].fitness >= avg:
                self.p[i].Store_To_Diversity_Pool()