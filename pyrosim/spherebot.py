from pyrosim import PYROSIM
import numpy as np
import constants as c
import copy
import random
import math

class ROBOT:

    def __init__(self, commands):

        self.num_joints = 0

        self.num_objects = 0

        self.num_sensors = 0

        self.head_ID = 0

        self.genome = np.random.rand(7, 1) * 2 - 1

    def Evaluate(self,sim,whatToMaximize):

        self.Get_Raw_Sensors(sim)

        if whatToMaximize == c.maximizeDistance:

            return self.raw_sensors['P'+str(self.head_ID)+'_X'][-1] 

    def Mutate(self):

        self.genomeSahpe = self.genome.shape

        geneToMutate = np.random.randint(self.genomeSahpe[0] * self.genomeSahpe[1])

        ind1 = geneToMutate / self.genomeSahpe[1]
        ind2 = geneToMutate % self.genomeSahpe[1]

        self.genome[ind1][ind2] = random.gauss( self.genome[ind1][ind2] ,
             math.fabs(self.genome[ind1][ind2]) )

        if self.genome[ind1][ind2] > 1.0:
            self.genome[ind1][ind2] = 1

        if self.genome[ind1][ind2] < -1.0:
            self.genome[ind1][ind2] = -1

    def Send_To_Simulator(self, sim, color, biasValue):

        self.Send_Objects(sim, color)

        self.Send_Joints(sim)

        self.Send_Eyes(sim, [0, -c.L/4, 2*c.L], 0.015, [1,0,0], [0,-1,0], 0.015)

        self.Send_Sensors(sim)

        self.Send_Neurons(sim, biasValue[0])

        self.Send_Synapses(sim)

    def Send_Objects(self, sim, color):

        self.num_objects =0

        sim.Send_Sphere(objectID = self.num_objects , x=0, y=0, z=c.L, mass=0.5,
            radius=c.L, r=color[0], g=color[1], b=color[2])
        self.num_objects +=1

        sim.Send_Cylinder(objectID = self.num_objects, x=0, y=0, z=c.L, r1=1, r2=0, r3=0,
         length=c.L, radius=c.R/2, r=color[0], g=color[1], b=color[2])
        
        self.head_ID = self.num_objects

        self.num_objects += 1

        sim.Send_Sphere(objectID = self.num_objects, x=(c.L-c.R)/2, y=0, z=c.L, radius=c.R,
         r=color[0], g=color[1], b=color[2])

        self.num_objects += 1


    def Send_Joints(self, sim):

        self.num_joints=0

        sim.Send_Joint(jointID = self.num_joints, firstObjectID=0, secondObjectID=1,
         n1 =0, n2 =1 , n3 =0, x=0, y=0, z=c.L, lo=-c.PI/2 , hi=c.PI/2)

        self.num_joints += 1

        sim.Send_Joint(jointID = self.num_joints, firstObjectID=1, secondObjectID=2,
         n1=-1, n2 =0 , n3 =0, x=(c.L-c.R), y=0, z=c.L, lo=0 , hi=0)

        self.num_joints += 1


    def Get_Raw_Sensors(self, sim):

        self.raw_sensors = {}

        self.raw_sensors['T0'] = copy.deepcopy(sim.Get_Sensor_Data(0, 0))

        self.raw_sensors['P1'] = copy.deepcopy(sim.Get_Sensor_Data(1, 0))

        self.raw_sensors['P'+str(self.head_ID)+'_X'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 0))

        self.raw_sensors['P'+str(self.head_ID)+'_Y'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 1))

        self.raw_sensors['P'+str(self.head_ID)+'_Z'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 2))

    def Get_Head_Trajectory(self, sim):

        self.values = []

        for ind in range(0, 3):

            self.values.append(copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, ind)))

        return self.values

    def Send_Sensors(self, sim):

        self.num_sensors = 0

        sim.Send_Touch_Sensor(sensorID=self.num_sensors, objectID = 0)
        self.num_sensors += 1

        sim.Send_Proprioceptive_Sensor(sensorID=self.num_sensors, jointID =0)
        self.num_sensors += 1
        
        sim.Send_Position_Sensor(sensorID=self.num_sensors, objectID = 0)
        self.num_sensors += 1

        # print self.num_sensors

    def Send_Neurons(self, sim, bValue):

        self.num_in_neurons = 0
        self.num_motor_neurons = 0

        sim.Send_Sensor_Neuron(neuronID=self.num_in_neurons, sensorID=0)
        self.num_in_neurons += 1

        # sim.Send_Sensor_Neuron(neuronID=self.num_in_neurons, sensorID=1)
        # self.num_in_neurons += 1

        # sim.Send_Sensor_Neuron(neuronID=self.num_in_neurons, sensorID=2)
        # self.num_in_neurons += 1

        sim.Send_Sensor_Neuron(neuronID=self.num_in_neurons, sensorID=self.num_sensors-1, sensorValueIndex = 0)
        self.num_in_neurons += 1

        sim.Send_Sensor_Neuron(neuronID=self.num_in_neurons, sensorID=self.num_sensors-1, sensorValueIndex = 1)
        self.num_in_neurons += 1

        sim.Send_Sensor_Neuron(neuronID=self.num_in_neurons, sensorID=self.num_sensors-1, sensorValueIndex = 2)
        self.num_in_neurons += 1

        sim.Send_Bias_Neuron(neuronID = self.num_in_neurons, biasValue=bValue)
        self.num_in_neurons += 1

        sim.Send_Motor_Neuron(neuronID=self.num_in_neurons, jointID=0, tau=0.3)
        self.num_motor_neurons += 1

    def Send_Synapses(self, sim):

        # print self.num_in_neurons, self.num_motor_neurons

        for sn in range(0, self.num_in_neurons):

            for mn in range(0, self.num_motor_neurons):

                sim.Send_Synapse(sourceNeuronID = sn ,targetNeuronID=mn+self.num_in_neurons, 
                    weight= self.genome[sn][mn])

    def Send_Eyes(self, sim, midpoint, distance, axis1=[1,0,0], axis2=[0,0,-1], 
        eye_radius=0.02):
        
        if distance < eye_radius/2.0:
            distance = eye_radius/2.0

        axis1 = [axis1[i] / np.linalg.norm(axis1) for i in range(len(axis1))]

        axis2 = [axis2[i] / np.linalg.norm(axis2) for i in range(len(axis2))]

        # print axis1, axis2

        lefEye    =[axis1[i]* -distance + midpoint[i] for i in range(len(axis1))]

        rightEye  =[axis1[i]* distance + midpoint[i] for i in range(len(axis1))]

        leftPupil =[axis2[i]* eye_radius/1.5 + axis1[i]* -distance + midpoint[i] for i in range(0, len(axis1))]

        rightPupil=[axis2[i]* eye_radius/1.5 + axis1[i]* distance + midpoint[i] for i in range(0, len(axis1))]

        sim.Send_Sphere(objectID = self.num_objects, 
            x= lefEye[0], y= lefEye[1], z= lefEye[2], 
            mass=0.01, radius = eye_radius, r=1, g=1, b=1)

        # print self.num_objects

        self.num_objects += 1

        sim.Send_Sphere(objectID = self.num_objects, 
            x= rightEye[0], y= rightEye[1], z= rightEye[2], 
            mass=0.01, radius = eye_radius, r=1, g=1, b=1)

        # print self.num_objects

        self.num_objects += 1

        sim.Send_Sphere(objectID = self.num_objects, 
            x= leftPupil[0], y= leftPupil[1], z= leftPupil[2], 
            mass=0.01, radius = eye_radius/1.5, r=0, g=0, b=0)

        # print self.num_objects

        self.num_objects += 1

        sim.Send_Sphere(objectID = self.num_objects, 
            x= rightPupil[0], y= rightPupil[1], z= rightPupil[2], 
            mass=0.01, radius = eye_radius/1.5, r=0, g=0, b=0)

        # print self.num_objects

        ###########################JOINTS#######################################

        sim.Send_Joint(jointID = self.num_joints, firstObjectID = self.head_ID,
        secondObjectID = self.num_objects-3,
        n1 =1, n2 =0, n3 =0, 
        x= lefEye[0], y= lefEye[1], z= lefEye[2],
        lo=0, hi=0)

        # print self.num_joints, self.num_objects-4, self.num_objects-3

        self.num_joints += 1

        sim.Send_Joint(jointID = self.num_joints, firstObjectID = self.head_ID,
        secondObjectID = self.num_objects-2,
        n1 =1, n2 =0, n3 =0, 
        x= rightEye[0], y= rightEye[1], z= rightEye[2], 
        lo=0, hi=0)
        
        # print self.num_joints, self.num_objects-4, self.num_objects-2

        self.num_joints += 1

        sim.Send_Joint(jointID = self.num_joints, firstObjectID = self.num_objects-3, 
        secondObjectID = self.num_objects-1,
        n1 =1, n2 =0, n3 =0, 
        x= leftPupil[0], y= leftPupil[1], z= leftPupil[2], 
        lo=0 , hi=0)

        self.num_joints += 1

        sim.Send_Joint(jointID = self.num_joints, firstObjectID = self.num_objects-2 , 
        secondObjectID = self.num_objects,
        n1 =1, n2 =0, n3 =0, 
        x= rightPupil[0], y= rightPupil[1], z= rightPupil[2], 
        lo=0 , hi=0)

        self.num_joints += 1


   


