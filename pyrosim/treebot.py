import constants as c
import copy
import math
import os
import random
import pickle
import numpy as np

from pyrosim import PYROSIM
from body import BODY
from brain import BRAIN

class ROBOT:

    def __init__(self, maxDepth, biasValues):

        self.body = BODY(int(maxDepth))

        self.brain = BRAIN( self.body.numSensors, 
            self.body.numJoints-4 if self.body.eyes else self.body.numJoints,
         self.body.sensorsCreated, biasValues)

        # print self.body.numSensors, self.body.numJoints, self.body.sensorsCreated

    def Evaluate(self,simulator,whatToMaximize):

        self.body.Get_Sensor_Data_From_Simulator(simulator)

        return self.body.Compute_Fitness(whatToMaximize)

    def Get_Head_Trajectory(self, simulator):

        self.body.Get_Sensor_Data_From_Simulator(simulator)

        return self.body.Get_Head_Trajectory(simulator)

    def Get_Raw_Sensors(self, simulator):

        self.raw_sensors={}

        self.body.Get_Sensor_Data_From_Simulator(simulator)

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

    def Send_To_Simulator(self,simulator,color,biasValues):

        self.body.Send_To_Simulator(simulator,color)

        self.brain.Send_To_Simulator(simulator,biasValues)
