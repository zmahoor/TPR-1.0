import constants as c
import copy
import math
import os
import random
import pickle
import numpy as np

# from pyrosim import SIMULATOR 
from pyrosim import PYROSIM
from body import BODY
from brain import BRAIN

class ROBOT:

    def __init__(self):

        self.body = BODY()

        self.brain = BRAIN( self.body.numSensors, self.body.numJoints )

        # print self.body.numSensors, self.body.numJoints

    def Evaluate(self,simulator,whatToMaximize):

        self.body.Get_Sensor_Data_From_Simulator(simulator)

        return self.body.Compute_Fitness(whatToMaximize)

    def Get_Raw_Sensors(self):

        self.raw_sensors={'meta_data':[], 'data':[]}

        self.body.Store_Sensors(self.raw_sensors)

    def Mutate(self):

        mutType = random.randint(0,1)

        if ( mutType == 0 ):

            self.body.Mutate()
        else:
            self.brain.Mutate()

        self.body.Reset()

    def Num_Body_Parts(self):

        return self.body.numObjects

    def Print(self):

        self.body.Print()

        self.brain.Print()

    def Send_To_Simulator(self,simulator,color):

        midpoint = [self.body.root.x, self.body.root.y-c.headRadius, self.body.root.z]

        self.body.Send_To_Simulator(simulator,color)

        self.body.Make_Eyes(simulator, midpoint, 0.015, [1,0,0], [0,-1,0], 0.015)

        self.brain.Send_To_Simulator(simulator)
