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

    archive = {}

    asize = 0

    def __init__(self, ps, robotType):

        self.p = {}
        self.popSize = ps

        for i in range(0, self.popSize):
            self.p[i] = INDIVIDUAL(i, robotType) 

    def Compute_External_Novelty(self):

        self.novelty = np.zeros((self.popSize, self.popSize + POPULATION.asize))

        # distance to all the other individuals
        for i in range(0, self.popSize):

            self.novelty[i][i] = float('inf')

            for j in range(i+1, self.popSize):
                vec1 = self.p[i].head_trajectory
                vec2 = self.p[j].head_trajectory
                dist = LA.norm(vec1-vec2)
                self.novelty[i][j] = self.novelty[j][i] = dist

        # distance to all the individuals in archive
        for i in range(0, self.popSize):

            for j in range(0, POPULATION.asize):
                vec1 = self.p[i].head_trajectory
                vec2 = POPULATION.archive[j].head_trajectory
                dist = LA.norm(vec1-vec2)
                self.novelty[i][self.popSize+j] = dist
    
    def Print(self):

        for i in self.p:
            self.p[i].Print()
        print

    def Sensors_Have_Changed(self, index):

        sensorDict = self.p[index].Get_Raw_Sensors()

        for sensorType in sensorDict.keys():

            sensorValues = sensorDict[sensorType]
            if np.absolute(sensorValues[-1]-sensorValues[-2]) != 0:
                return True

        return False

    def Evaluate_External_Novelty(self, pp, pb, knn=5):

        for i in self.p:
            self.p[i].Start_Evaluate(pp, pb, (c.NUM_BIAS_NEURONS+c.NUM_COMMAND_NEURONS)*[1.0])

        for i in self.p:
            self.p[i].Get_Head_Trajectory()

        self.Compute_External_Novelty()

        for i in self.p:

            if not self.Sensors_Have_Changed( i ):
                self.p[i].fitness = 0

            else:
                #find the k nearest neighbors
                idx = np.argpartition(self.novelty[i], knn)
                self.p[i].fitness = np.average(self.novelty[i][idx[:knn]])

    def Evaluate_Internal_Novelty(self, pp, pb, brange=3):

        temp = {}

        for i in self.p: 
            temp[i]=[]

        for b in np.linspace(0, 1, brange):

            for i in self.p:
                self.p[i].Start_Evaluate(pp, pb, c.NUM_BIAS_NEURONS*[1.0]+[b]\
                 if c.NUM_BIAS_NEURONS>0 else [b])

            for i in self.p:
                self.p[i].Get_Head_Trajectory()
            
            for i in self.p:
                temp[i].append(self.p[i].head_trajectory)

        for i in self.p:

            novelty = np.zeros((brange, brange))
            for j in range(0, brange):

                novelty[j][j] = float('inf')
                for k in range(j+1, brange):
                    novelty[k][j] = novelty[j][k] = LA.norm(temp[i][j] - temp[i][k])

            self.p[i].fitness = np.min(novelty)

    def Print_Archive(self):

        print "archive size: ", POPULATION.asize

    def Unique(self, i):

        for a in range(0, POPULATION.asize):
            if ( POPULATION.archive[a].head_trajectory == self.p[i].head_trajectory).all():
                return False

        return True

    def Update_Archive(self, threshold):

        for i in self.p:

            if self.p[i].fitness > threshold and self.Unique(i):

                POPULATION.archive[POPULATION.asize] = deepcopy(self.p[i])
                POPULATION.archive[POPULATION.asize].id = POPULATION.asize
                POPULATION.asize = POPULATION.asize + 1

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

    def Store_Archive(self):
        
        for i in POPULATION.archive:
            POPULATION.archive[i].Store_To_Diversity_Pool()

    def Store_All_Above_Average(self):

        avg = 0.0
        for i in self.p:
            avg += self.p[i].fitness

        avg /= float(self.popSize)

        print "average fitness: ", avg

        for i in self.p:
            if self.p[i].fitness >= avg:
                self.p[i].Store_To_Diversity_Pool()

