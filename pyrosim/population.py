from pyrosim import PYROSIM
import numpy as np
from individual import INDIVIDUAL
from sys import float_info
import pickle
from copy import deepcopy

class POPULATION:

    def __init__(self, ps):

        self.p = {}

        self.popSize = ps

        for i in range(0, self.popSize):
            self.p[i] = INDIVIDUAL(i) 

        self.bestOfAll = -float_info.max

    def Print(self):

        for i in self.p:
            self.p[i].Print()
        print

    def Evaluate(self, pp, pb):

        for i in self.p:
            self.p[i].Start_Evaluate(pp, pb)

        for i in self.p:
            self.p[i].Compute_Fitness()

        # self.Print()

    def Mutate(self):

        for i in self.p:
            self.p[i].Mutate()

    def ReplaceWith(self, other):

        for i in self.p:
            if (self.p[i].fitness < other.p[i].fitness):
                self.p[i] = other.p[i]

    def FindFittest(self):

        best = 0

        for i in self.p:
            if (self.p[i].fitness >= self.p[best].fitness ):
                best = i

        # if (self.p[best].fitness > self.bestOfAll):
        #     self.bestOfAll = self.p[best].fitness
        
        self.p[best].Store()

        self.p[best].Start_Evaluate(True, False)
        self.p[best].Compute_Fitness()

        # print "bestOfAll: ", self.bestOfAll
       
