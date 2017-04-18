import constants as c
import numpy as np
import random
import math
from neurons import NEURONS
from synapses import SYNAPSES

class BRAIN:

    def __init__(self,numSensors,numJoints):

        self.neurons = NEURONS(numSensors,numJoints)

        self.synapses = SYNAPSES(numSensors,numJoints)

    def Mutate(self):

        mutType = random.randint(0,1)

        if ( mutType == 0 ):

            self.neurons.Mutate()
        else:
            self.synapses.Mutate()

    
    def Send_To_Simulator(self,simulator):

        self.neurons.Send_To_Simulator(simulator)

        self.synapses.Send_To_Simulator(simulator)

# ----------------- Private methods -----------------------

    def Print(self):

        self.synapses.Print()
