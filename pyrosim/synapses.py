import constants as c
import numpy as np
import random
import math
from synapse import SYNAPSE

class SYNAPSES: 

    def __init__(self,numSensorNeurons,numMotorNeurons):

        self.numSensorNeurons = numSensorNeurons

        self.numMotorNeurons = numMotorNeurons

        self.numBiasNeurons = c.NUM_BIAS_NEURONS + c.NUM_COMMAND_NEURONS

        self.Create_BH()

        self.Create_SH()

        self.Create_HH()

        self.Create_HM()

    def Mutate(self):

        mutType = random.randint(0,3)

        if ( mutType == 0 ):

            self.Mutate_SH()

        elif ( mutType == 1 ):

            self.Mutate_HH()

        elif(mutType == 2):

            self.Mutate_HM()

        else:
            self.Mutate_BH()

    def Print(self):

        self.Print_BH()

        self.Print_SH()

        self.Print_HH()

        self.Print_HM()

    def Send_To_Simulator(self,simulator):

        self.Send_BH(simulator)

        self.Send_SH(simulator)

        self.Send_HH(simulator)

        self.Send_HM(simulator)


# -------------------- Private functions ---------------------
    
    def Create_BH(self):

        self.bh = {}

        for b in range(0,self.numBiasNeurons):

            for h in range(0,c.NUM_HIDDEN_NEURONS):

                sourceNeuron = b

                targetNeuron = self.numSensorNeurons + h

                self.bh[b,h] = SYNAPSE(sourceNeuron,targetNeuron)


    def Create_SH(self):

        self.sh = {}

        for s in range(0,self.numSensorNeurons):

            for h in range(0,c.NUM_HIDDEN_NEURONS):

                sourceNeuron = s

                targetNeuron = self.numSensorNeurons + h

                self.sh[s,h] = SYNAPSE(sourceNeuron,targetNeuron)

    def Create_HH(self):

        self.hh = {}

        for h1 in range(0,c.NUM_HIDDEN_NEURONS):

            for h2 in range(0,c.NUM_HIDDEN_NEURONS):

                sourceNeuron = self.numSensorNeurons + h1

                targetNeuron = self.numSensorNeurons + h2

                self.hh[h1,h2] = SYNAPSE(sourceNeuron,targetNeuron)

    def Create_HM(self):

        self.hm = {}

        for h in range(0,c.NUM_HIDDEN_NEURONS):

            for m in range(0,self.numMotorNeurons):

                sourceNeuron = self.numSensorNeurons + h

                targetNeuron = self.numSensorNeurons + c.NUM_HIDDEN_NEURONS + m 

                self.hm[h,m] = SYNAPSE(sourceNeuron,targetNeuron)

    def Mutate_SH(self):

        s = random.randint(0, self.numSensorNeurons - 1 )

        h = random.randint(0, c.NUM_HIDDEN_NEURONS - 1 )

        self.sh[s,h].Mutate()

    def Mutate_HH(self):

        h1 = random.randint(0, c.NUM_HIDDEN_NEURONS - 1 )

        h2 = random.randint(0, c.NUM_HIDDEN_NEURONS - 1 )

        self.hh[h1,h2].Mutate()

    def Mutate_HM(self):

        h = random.randint(0, c.NUM_HIDDEN_NEURONS - 1 )

        m = random.randint(0, self.numMotorNeurons - 1 )

        self.hm[h,m].Mutate()

    def Mutate_BH(self):

        b = random.randint(0, self.numBiasNeurons - 1 )

        h = random.randint(0, c.NUM_HIDDEN_NEURONS - 1 )

        self.sh[b,h].Mutate()

    def Print_BH(self):

        for b,h in self.bh:

            self.bh[b,h].Print()

    def Print_SH(self):

        for s,h in self.sh:

            self.sh[s,h].Print()

    def Print_HH(self):

        for h1,h2 in self.hh:

            self.hh[h1,h2].Print()

    def Print_HM(self):

        for h,m in self.hm:

            self.hm[h,m].Print()

    def Send_SH(self,simulator):

        for s in range(0,self.numSensorNeurons):

            for h in range(0,c.NUM_HIDDEN_NEURONS):

                self.sh[s,h].Send_To_Simulator(simulator)

    def Send_HH(self,simulator):

        for h1 in range(0,c.NUM_HIDDEN_NEURONS):

            for h2 in range(0,c.NUM_HIDDEN_NEURONS):

                self.hh[h1,h2].Send_To_Simulator(simulator)

    def Send_HM(self,simulator):

        for h in range(0,c.NUM_HIDDEN_NEURONS):

            for m in range(0,self.numMotorNeurons):

                self.hm[h,m].Send_To_Simulator(simulator)

    def Send_BH(self, simulator):

        for b in range(0,self.numBiasNeurons):

            for h in range(0,c.NUM_HIDDEN_NEURONS):

                self.bh[b,h].Send_To_Simulator(simulator)


