#population of individuals for novelty search
from pyrosim import PYROSIM
import numpy as np
from individual import INDIVIDUAL
from sys import float_info
import pickle
from copy import deepcopy
from numpy import linalg as LA

class POPULATION:

    archive = {}

    asize = 0

    def __init__(self, ps, robotType):

        self.p = {}

        self.popSize = ps

        for i in range(0, self.popSize):
            self.p[i] = INDIVIDUAL(i, robotType) 

    def Compute_Novelty_Matrix(self):

        self.novelty = np.zeros((self.popSize,self.popSize + POPULATION.asize))

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

    def Evaluate(self, pp, pb, knn=5):

        for i in self.p:
            self.p[i].Start_Evaluate(pp, pb, 1.0)

        for i in self.p:
            self.p[i].Get_Head_Trajectory()
        
        self.Compute_Novelty_Matrix()

        for i in self.p:
            #find the k nearest neighbors
            idx = np.argpartition(self.novelty[i], knn)
            self.p[i].fitness = np.average(self.novelty[i][idx[:knn]])

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
            self.p[i].Store()

    def Store_Archive(self):
        
        for i in POPULATION.archive:
            POPULATION.archive[i].Store()
