
from pyrosim import PYROSIM
import numpy as np
import constants as c

class ROBOT:

    def __init__(self, sim, wts, color):

        self.num_sensor_neurons, self.num_motor_neurons = np.shape(wts)

        self.color = color

        self.last_jointID = 0

        self.last_objectID = 0

        self.last_sensorID = 0

        self.last_synapseID = 0

        self.head_ID = 0

        self.Send_Objects(sim, color)

        self.Send_Joints(sim)

        self.Make_Eyes(sim, [0, -3*c.L, 2*c.R], 0.015, [1,0,0], [0,-1,0], 0.015)

        self.Send_Sensors(sim)

        self.Send_Neurons(sim)

        self.Send_Synapses(sim, wts)

    def Send_Objects(self, sim, color):

        # Green Box
        sim.Send_Box(objectID = self.last_objectID , x=0, y=0, z=c.R, length=c.L,
         width=2*c.L, height=2*c.R, r=0, g=1, b=0)

        self.last_objectID += 1

        # Purple Box
        sim.Send_Box(objectID = self.last_objectID , x=0, y=2*c.L, z=c.R,length=c.L,
         width=2*c.L, height=2*c.R, r=1, g=0, b=1)

        self.last_objectID += 1

        # Red Box
        sim.Send_Box(objectID = self.last_objectID , x=0, y=-2*c.L, z=c.R,length=c.L,
         width=2*c.L, height=2*c.R, r=1, g=0, b=0)

        self.head_ID = self.last_objectID

        #######################EYES#############################################
        # self.last_objectID += 1

        # sim.Send_Sphere(objectID = self.last_objectID, x=-0.02, y=-3*c.L-0.02, 
        #     z=c.R+0.02, radius=0.02, r=1, g=1, b=1)

        # self.last_objectID += 1

        # sim.Send_Sphere(objectID = self.last_objectID, x=0.02,  y=-3*c.L-0.02, 
        #     z=c.R+0.02, radius=0.02, r=1, g=1, b=1)

        # self.last_objectID += 1

        # sim.Send_Sphere(objectID = self.last_objectID, x=-0.02, y=-3*c.L-0.03, 
        #     z=c.R+0.03, radius=0.01, r=0, g=0, b=0)

        # self.last_objectID += 1

        # sim.Send_Sphere(objectID = self.last_objectID, x=0.02,  y=-3*c.L-0.03, 
        #     z=c.R+0.03, radius=0.01, r=0, g=0, b=0)

    def Send_Joints(self, sim):

        sim.Send_Joint( jointID = self.last_jointID, firstObjectID = 0, secondObjectID = 2,
         n1 =1, n2 =0, n3 =0, x=0, y=-c.L, z=c.R, lo=-c.PI/4 , hi=c.PI/4)

        self.last_jointID += 1

        sim.Send_Joint( jointID = self.last_jointID, firstObjectID = 0, secondObjectID = 1,
         n1 =1, n2 =0, n3 =0, x=0, y=c.L, z=c.R, lo=-c.PI/4 , hi=c.PI/4)

        print self.last_jointID

        # #######################EYES#############################################
        # self.last_jointID += 1

        # sim.Send_Joint(jointID = self.last_jointID , firstObjectID = 1 , secondObjectID = 3,
        #  n1 =1 , n2 =0 , n3 =0, x=-0.02, y=-3*c.L, z=c.R+0.02, lo=0 , hi=0)

        #self.last_jointID += 1

        # sim.Send_Joint(jointID = self.last_jointID , firstObjectID = 1 , secondObjectID = 4,
        #  n1 =1 , n2 =0 , n3 =0, x=0.02, y=-3*c.L, z=c.R+0.02, lo=0 , hi=0)

        # self.last_jointID += 1

        # sim.Send_Joint(jointID = self.last_jointID , firstObjectID = 3 , secondObjectID = 5,
        #  n1 =1 , n2 =0 , n3 =0, x=-0.02, y=-3*c.L-0.03, z=c.R+0.03, lo=0 , hi=0)

        # self.last_jointID += 1

        # sim.Send_Joint(jointID = self.last_jointID , firstObjectID = 4 , secondObjectID = 6,
        #  n1 =1 , n2 =0 , n3 =0, x=0.02, y=-3*c.L-0.03, z=c.R+0.03, lo=0 , hi=0)


    def Send_Sensors(self, sim):

        sim.Send_Touch_Sensor(sensorID = self.last_sensorID, objectID = 0)
        self.last_sensorID += 1

        sim.Send_Touch_Sensor(sensorID = self.last_sensorID, objectID = 1)
        self.last_sensorID += 1
        
        sim.Send_Touch_Sensor(sensorID = self.last_sensorID, objectID = 2)
        self.last_sensorID += 1

        sim.Send_Proprioceptive_Sensor(sensorID = self.last_sensorID, jointID = 0)
        self.last_sensorID += 1

        sim.Send_Proprioceptive_Sensor(sensorID = self.last_sensorID, jointID = 1)
        self.last_sensorID += 1

        sim.Send_Position_Sensor(sensorID = self.last_sensorID, objectID = 1)

    def Send_Neurons(self, sim):

        for sn in range(0, self.num_sensor_neurons):
            sim.Send_Sensor_Neuron(neuronID=sn, sensorID=sn)
            # self.last_neuronID += 1

        for mn in range(0, self.num_motor_neurons):
            sim.Send_Motor_Neuron(neuronID=mn+self.num_sensor_neurons,
             jointID=mn, tau=0.3)

    def Send_Synapses(self, sim, wts):

        for sn in range(0, self.num_sensor_neurons):
            for mn in range(0, self.num_motor_neurons):
                
                sim.Send_Synapse(sourceNeuronID = sn , targetNeuronID 
                    =mn+self.num_sensor_neurons, weight= wts[sn][mn])

    def L2_Norm(self, mylist):
        n =0.0
        for i in range(len(mylist)):
            n += mylist[i]**2 

        return(n**0.5)

    def Make_Eyes(self, sim, midpoint, distance, axis1=[1,0,0], axis2=[0,0,-1], 
        eye_radius=0.02):
        
        if distance < eye_radius/2.0:
            distance = eye_radius/2.0

        axis1 = [axis1[i] / self.L2_Norm(axis1) for i in range(len(axis1))]

        axis2 = [axis2[i] / self.L2_Norm(axis2) for i in range(len(axis2))]

        print axis1, axis2

        lefEye    =[axis1[i]* -distance + midpoint[i] for i in range(len(axis1))]

        rightEye  =[axis1[i]* distance + midpoint[i] for i in range(len(axis1))]

        leftPupil =[axis2[i]* eye_radius/1.5 + axis1[i]* -distance + midpoint[i] for i in range(0, len(axis1))]

        rightPupil=[axis2[i]* eye_radius/1.5 + axis1[i]* distance + midpoint[i] for i in range(0, len(axis1))]

        self.last_objectID += 1

        sim.Send_Sphere(objectID = self.last_objectID, 
            x= lefEye[0], y= lefEye[1], z= lefEye[2], 
            mass=0.1, radius = eye_radius, r=1, g=1, b=1)

        print self.last_objectID

        self.last_objectID += 1

        sim.Send_Sphere(objectID = self.last_objectID, 
            x= rightEye[0], y= rightEye[1], z= rightEye[2], 
            mass=0.1, radius = eye_radius, r=1, g=1, b=1)

        print self.last_objectID

        self.last_objectID += 1

        sim.Send_Sphere(objectID = self.last_objectID, 
            x= leftPupil[0], y= leftPupil[1], z= leftPupil[2], 
            mass=0.1, radius = eye_radius/1.5, r=0, g=0, b=0)

        print self.last_objectID

        self.last_objectID += 1

        sim.Send_Sphere(objectID = self.last_objectID, 
            x= rightPupil[0], y= rightPupil[1], z= rightPupil[2], 
            mass=0.1, radius = eye_radius/1.5, r=0, g=0, b=0)

        print self.last_objectID

        ###########################JOINTS#######################################
        self.last_jointID += 1

        sim.Send_Joint(jointID = self.last_jointID, firstObjectID = self.head_ID,
        secondObjectID = self.last_objectID-3,
        n1 =1, n2 =0, n3 =0, 
        x= lefEye[0], y= lefEye[1], z= lefEye[2],
        lo=0, hi=0)

        print self.last_jointID, self.last_objectID-4, self.last_objectID-3

        self.last_jointID += 1

        sim.Send_Joint(jointID = self.last_jointID, firstObjectID = self.head_ID,
        secondObjectID = self.last_objectID-2,
        n1 =1, n2 =0, n3 =0, 
        x= rightEye[0], y= rightEye[1], z= rightEye[2], 
        lo=0, hi=0)
        
        print self.last_jointID, self.last_objectID-4, self.last_objectID-2

        self.last_jointID += 1

        sim.Send_Joint(jointID = self.last_jointID, firstObjectID = self.last_objectID-3, 
        secondObjectID = self.last_objectID-1,
        n1 =1, n2 =0, n3 =0, 
        x= leftPupil[0], y= leftPupil[1], z= leftPupil[2], 
        lo=0 , hi=0)

        self.last_jointID += 1

        sim.Send_Joint(jointID = self.last_jointID, firstObjectID = self.last_objectID-2 , 
        secondObjectID = self.last_objectID,
        n1 =1, n2 =0, n3 =0, 
        x= rightPupil[0], y= rightPupil[1], z= rightPupil[2], 
        lo=0 , hi=0)


