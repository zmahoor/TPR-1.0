import random
import math
import numpy as np

class SYNAPSE:

    def __init__(self,sourceNeuron,targetNeuron):

        self.sourceNeuron = sourceNeuron

        self.targetNeuron = targetNeuron

        self.weight = np.random.rand() * 2 - 1

    def Mutate(self):

        self.weight = random.gauss( self.weight , math.fabs(self.weight) )

    def Print(self):

        print self.weight

    def Send_To_Simulator(self,simulator):

        simulator.Send_Synapse(sourceNeuronID = self.sourceNeuron , targetNeuronID = self.targetNeuron , weight = self.weight )

