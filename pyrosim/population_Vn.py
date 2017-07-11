#population of individuals for novelty search
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

        for sensorType in sensorDict.keys():

            sensorValues = sensorDict[sensorType]
            if np.absolute(sensorValues[-1]-sensorValues[-2]) != 0:
                return True

        return False

    def Evaluate_Internal_Novelty(self, pp, pb):

        tempSensors = {}

        for i in self.p: 
            tempSensors[i]=[]

        for b in [-1, +1]:

            for i in self.p:
                self.p[i].Start_Evaluate(pp, pb, c.NUM_BIAS_NEURONS*[1.0]+[b]\
                 if c.NUM_BIAS_NEURONS>0 else [b])

            for i in self.p:
                self.p[i].Wait_For_Me()
            
            for i in self.p:
                tempSensors[i].append(self.p[i].Get_Raw_Sensors())

        self.Compute_Fitness(tempSensors)

    def Compute_Fitness(self, tempSensors ):

        for i in self.p:

            neg_One_Sensors = tempSensors[i][0]
            pos_One_Sensors = tempSensors[i][1]

            self.p[i].fitness = 0

            if self.Sensors_Have_Changed( neg_One_Sensors ):
                if self.Sensors_Have_Changed( pos_One_Sensors ):

                    neg_One_Head_Traj = np.hstack((neg_One_Sensors['P0_X'],\
                         neg_One_Sensors['P0_Y'], neg_One_Sensors['P0_Z'] ))

                    pos_One_Head_Traj = np.hstack((pos_One_Sensors['P0_X'],\
                         pos_One_Sensors['P0_Y'], pos_One_Sensors['P0_Z'] ))

                    self.p[i].fitness = LA.norm(neg_One_Head_Traj - pos_One_Head_Traj)

    def Mutate(self):

        for i in self.p:
            self.p[i].Mutate()

    def ReplaceWith(self, other):

        for i in self.p:
            if (self.p[i].fitness < other.p[i].fitness):
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

