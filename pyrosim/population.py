#population of individuals for novelty search

from pyrosim import PYROSIM
import numpy as np
from individual import INDIVIDUAL
from sys import float_info
import pickle
from copy import deepcopy
from scipy.spatial import distance

class POPULATION:

    def __init__(self, ps, wtm, robotType):

        self.p = {}

        self.popSize = ps

        # self.whatToMaximize = wtm

        for i in range(0, self.popSize):
            self.p[i] = INDIVIDUAL(i, robotType) 

        self.bestOfAll = -float_info.max


    # compare all the individuals against each other and 
    def fitness_all(self):

        self.relFitness = np.zeros((self.popSize,self.popSize))

        for i in range(0, self.popSize):

            self.relFitness[i][i] = float('inf')

            for j in range(i+1, self.popSize):

                vec1 = self.p[i].head_trajectory
                vec2 = self.p[j].head_trajectory

                rows, cols= vec1.shape

                for k in range(0, rows):
                    self.relFitness[i][j] += distance.euclidean(vec1[k][:], vec2[k][:])

                self.relFitness[i][j] = self.relFitness[i][j] / float(rows)

                self.relFitness[j][i] = self.relFitness[i][j]


    def Print(self):

        for i in self.p:
            self.p[i].Print()
        print

    def Evaluate(self, pp, pb):

        for i in self.p:
            self.p[i].Start_Evaluate(pp, pb)

        for i in self.p:
            self.p[i].Get_Head_Trajectory()
        
        # for i in self.p:
        #     self.p[i].Compute_Fitness(self.whatToMaximize)
        
        self.fitness_all()

        # print self.relFitness

        for i in self.p:
            self.p[i].fitness = min(self.relFitness[i])

            # print self.p[i].fitness

        # self.Print()

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

    def FindFittest(self):

        best = 0

        for i in self.p:
            if (self.p[i].fitness >= self.p[best].fitness ):
                best = i
        
        self.p[best].Store()

        self.p[best].Start_Evaluate(True, False)
        
        self.p[best].Compute_Fitness(self.whatToMaximize)

        # print "bestOfAll: ", self.bestOfAll
       
