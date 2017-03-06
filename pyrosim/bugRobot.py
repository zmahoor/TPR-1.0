
from pyrosim import PYROSIM
import numpy as np
import constants as c

class ROBOT:

    def __init__(self, sim, wts, color):

        self.num_sensor_neurons, self.num_motor_neurons = np.shape(wts)
        self.color = color

        self.Send_Objects(sim, color)
        self.Send_Joints(sim)
        self.Send_Sensors(sim)
        self.Send_Neurons(sim)
        self.Send_Synapses(sim, wts)

    def Send_Objects(self, sim, color):
        # box 
        sim.Send_Box(objectID = 0 , x=0, y=0, z=c.L + c.R, length=c.L, width=c.L,
         height=2*c.R, r=color[0], g=color[1], b=color[2])
        
        # # red
        sim.Send_Cylinder( objectID=1, x=0, y=c.L, z=c.L + c.R, r1=0 , r2=1, r3=0,
         length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        
        # green
        sim.Send_Cylinder( objectID=2, x=c.L, y=0, z=c.L + c.R, r1=1 , r2=0, r3=0,
         length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

        # # blue
        sim.Send_Cylinder( objectID=3, x=0, y=-c.L, z=c.L + c.R, r1=0 , r2=-1, r3=0,
         length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

        # #purple
        sim.Send_Cylinder( objectID=4, x=-c.L, y=0, z=c.L + c.R, r1=-1 , r2=0, r3=0,
         length=c.L, radius=c.R,  r=color[0], g=color[1], b=color[2])

        ## vertical segments
        #red
        sim.Send_Cylinder( objectID=5, x=0, y=c.L/2 + c.L, z=(c.L/2 + c.R), r1=0,
         r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

        # green
        sim.Send_Cylinder( objectID=6, x=(c.L+c.L/2), y=0, z=(c.L/2 + c.R), r1=0,
         r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

        #blue
        sim.Send_Cylinder( objectID=7, x=0, y=-(c.L/2 + c.L), z=(c.L/2 + c.R), r1=0,
         r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

        # purple
        sim.Send_Cylinder( objectID=8, x=-(c.L+c.L/2), y=0, z=(c.L/2 + c.R), r1=0,
         r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

    def Send_Joints(self, sim):

        # red
        sim.Send_Joint( jointID = 0 , firstObjectID = 0 , secondObjectID = 1,
         n1 =-1 , n2 =0 , n3 =0, x=0, y=c.L/2, z=c.L+c.R)
        sim.Send_Joint( jointID = 1 , firstObjectID = 1 , secondObjectID = 5,
         n1 =-1 , n2 =0 , n3 =0, x=0, y=c.L+c.L/2, z=c.L+c.R)

        # green
        sim.Send_Joint( jointID = 2 , firstObjectID = 0 , secondObjectID = 2,
         n1 =0 , n2 =1 , n3 =0, x=c.L/2, y=0, z=c.L+c.R)
        sim.Send_Joint( jointID = 3 , firstObjectID = 2 , secondObjectID = 6,
         n1 =0 , n2 =1 , n3 =0, x=(c.L+c.L/2), y=0, z=c.L+c.R)
        
        # # blue
        sim.Send_Joint( jointID = 4 , firstObjectID = 0 , secondObjectID = 3,
         n1 =1 , n2 =0 , n3 =0, x=0, y=-c.L/2, z=c.L+c.R)
        sim.Send_Joint( jointID = 5 , firstObjectID = 3 , secondObjectID = 7,
         n1 =1 , n2 =0 , n3 =0, x=0, y=-(c.L+c.L/2), z= c.L+c.R)
        
        # # purple
        sim.Send_Joint( jointID = 6 , firstObjectID = 0 , secondObjectID = 4,
         n1 =0 , n2 =-1 , n3 =0, x=-c.L/2, y=0, z=c.L+c.R)
        sim.Send_Joint( jointID = 7 , firstObjectID = 4 , secondObjectID = 8,
         n1 =0 , n2 =-1 , n3 =0, x=-(c.L+c.L/2), y=0, z=c.L+c.R)

    def Send_Sensors(self, sim):

        for s in range(0, 4):
            sim.Send_Touch_Sensor(sensorID = s, objectID = s+5)

        sim.Send_Position_Sensor(sensorID = 4, objectID = 0)

    def Send_Neurons(self, sim):

        for sn in range(0, self.num_sensor_neurons):
            sim.Send_Sensor_Neuron(neuronID=sn, sensorID=sn)

        for mn in range(0, self.num_motor_neurons):
            sim.Send_Motor_Neuron(neuronID=mn+self.num_sensor_neurons,
             jointID=mn, tau=0.3)

    def Send_Synapses(self, sim, wts):

        for sn in range(0, self.num_sensor_neurons):
            for mn in range(0, self.num_motor_neurons):
                
                sim.Send_Synapse(sourceNeuronID = sn , targetNeuronID 
                    =mn+self.num_sensor_neurons, weight= wts[sn][mn])



