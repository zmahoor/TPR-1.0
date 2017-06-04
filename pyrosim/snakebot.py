from pyrosim import PYROSIM
import numpy as np
import copy
import constants as c
import math
import random
from eyes import EYES 
from brain import BRAIN

class ROBOT:

    def __init__(self):

        self.Initialize_Body()

        self.brain = BRAIN(self.num_sensors, self.num_motor_neurons,
            self.sensorsCreated)

    def Initialize_Body(self):

        self.num_joints     = 0
        self.num_objects    = 0
        self.head_ID        = 0
        self.num_sensors    = 0
        self.num_in_neurons = 0
        self.num_motor_neurons = 2
        self.sensorsCreated = {}

        self.Add_Sensors()

        print self.num_sensors, self.num_motor_neurons, self.sensorsCreated
    
    def Mutate(self):

        self.brain.Mutate()

    def Evaluate(self,sim,whatToMaximize):

        self.Get_Raw_Sensors(sim)

        if whatToMaximize == c.maximizeDistance:

            return self.raw_sensors['P'+str(self.head_ID)+'_X'][-1] 

    def Send_To_Simulator(self, sim, color, biasValues):

        jointsCreated  = {}
        objectsCreated = {}

        self.Send_Objects(sim, color)

        self.Send_Joints(sim)

        jointsCreated[0] = self.num_joints
        objectsCreated[0]= self.num_objects

        self.eyes = EYES(self.head_ID, [0,-3*c.L,2*c.R], 0.015, [1,0,0], [0,-1,0], 0.015)

        self.eyes.Create_Eyes(jointsCreated, objectsCreated)

        self.num_joints  = jointsCreated[0]
        self.num_objects = objectsCreated[0]

        self.eyes.Send_Eyes_To_Simulator(sim)

        self.Send_Sensors(sim)

        # print biasValues

        self.brain.Send_To_Simulator(sim,biasValues)

    def Send_Objects(self, sim, color):

        self.num_objects = 0
        # Green Box
        sim.Send_Box(objectID = self.num_objects , x=0, y=0, z=c.R, length=c.L,
         width=2*c.L, height=2*c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        # Purple Box
        sim.Send_Box(objectID = self.num_objects , x=0, y=2*c.L, z=c.R,length=c.L,
         width=2*c.L, height=2*c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        # Red Box
        sim.Send_Box(objectID = self.num_objects , x=0, y=-2*c.L, z=c.R,length=c.L,
         width=2*c.L, height=2*c.R, r=color[0], g=color[1], b=color[2])

        self.head_ID = self.num_objects
        self.num_objects += 1

    def Send_Joints(self, sim):

        self.num_joints = 0

        sim.Send_Joint( jointID = self.num_joints, firstObjectID = 0, secondObjectID = 2,
         n1 =1, n2 =0, n3 =0, x=0, y=-c.L, z=c.R, lo=-c.PI/2 , hi=c.PI/2)
        self.num_joints += 1

        sim.Send_Joint( jointID = self.num_joints, firstObjectID = 0, secondObjectID = 1,
         n1 =1, n2 =0, n3 =0, x=0, y=c.L, z=c.R, lo=-c.PI/2 , hi=c.PI/2)
        self.num_joints += 1

    def Add_Sensors(self):

        self.sensorsCreated = {}
        self.num_sensors = 0

        for s in range(0, 3):
            self.sensorsCreated[self.num_sensors]=c.TOC_SENSOR
            self.num_sensors += 1

        for s in range(0, 2):
            self.sensorsCreated[self.num_sensors]=c.PRO_SENSOR
            self.num_sensors += 1

        self.sensorsCreated[self.num_sensors]=c.RAY_SENSOR
        self.num_sensors += 1

        self.sensorsCreated[self.num_sensors]=c.RAY_SENSOR
        self.num_sensors += 1

        self.sensorsCreated[self.num_sensors]=c.POS_SENSOR
        self.num_sensors += 1

    def Send_Sensors(self, sim):

        sim.Send_Touch_Sensor(sensorID = 0, objectID = 0)
        sim.Send_Touch_Sensor(sensorID = 1, objectID = 1)
        sim.Send_Touch_Sensor(sensorID = 2, objectID = 2)

        sim.Send_Proprioceptive_Sensor(sensorID = 3, jointID = 0)
        sim.Send_Proprioceptive_Sensor(sensorID = 4, jointID = 1)

        sim.Send_Ray_Sensor(sensorID=5, objectID=self.num_objects-2
            , x=self.eyes.leftPupil[0], y=self.eyes.leftPupil[1], 
            z=self.eyes.leftPupil[2], r1=0, r2=-1, r3=0)

        sim.Send_Ray_Sensor(sensorID=6, objectID=self.num_objects-1
            , x=self.eyes.rightPupil[0], y=self.eyes.rightPupil[1],
             z=self.eyes.rightPupil[2], r1=0, r2=-1, r3=0)

        sim.Send_Position_Sensor(sensorID =7, objectID = self.head_ID)

    def Get_Raw_Sensors(self, sim):

        self.raw_sensors = {}

        self.raw_sensors['T0'] = copy.deepcopy(sim.Get_Sensor_Data(0, 0))
        self.raw_sensors['T1'] = copy.deepcopy(sim.Get_Sensor_Data(1, 0))
        self.raw_sensors['T2'] = copy.deepcopy(sim.Get_Sensor_Data(2, 0))

        self.raw_sensors['P0'] = copy.deepcopy(sim.Get_Sensor_Data(3, 0))
        self.raw_sensors['P1'] = copy.deepcopy(sim.Get_Sensor_Data(4, 0))

        self.raw_sensors['R0'] = copy.deepcopy(sim.Get_Sensor_Data(5, 0))

        self.raw_sensors['P'+str(self.head_ID)+'_X'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 0))
        self.raw_sensors['P'+str(self.head_ID)+'_Y'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 1))
        self.raw_sensors['P'+str(self.head_ID)+'_Z'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 2))

    def Get_Head_Trajectory(self, sim):

        self.values = []
        for ind in range(0, 3):
            self.values.append(copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, ind)))
        return self.values
