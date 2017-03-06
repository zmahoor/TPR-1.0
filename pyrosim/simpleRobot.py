
from pyrosim import PYROSIM
import numpy as np

class ROBOT:

    def __init__(self, sim, wts, color):

        # print color
        
        sim.Send_Cylinder( objectID=0, x=0, y=0 , z=0.6, length=1.0, radius=0.1,
            r=color[0], g=color[1], b=color[1])

        sim.Send_Cylinder( objectID=1, x=0 , y=0.5 , z=1.1 , r1=0 , r2=1, r3=0,
         length=1.0 , radius=0.1, r=color[0], g=color[1], b=color[1])

        sim.Send_Joint( jointID = 0 , firstObjectID = 0 , secondObjectID = 1,
         n1 = -1 , n2 = 0 , n3 = 0, x=0, y=0, z= 1.1, lo=-3.14159/2 , hi=3.14159/2)

        sim.Send_Touch_Sensor( sensorID = 0 , objectID = 0 )
        sim.Send_Touch_Sensor( sensorID = 1 , objectID = 1 )
        sim.Send_Proprioceptive_Sensor(sensorID = 2, jointID = 0)
        sim.Send_Ray_Sensor(sensorID = 3 , objectID = 1 , x = 0 , y = 1.1 , z = 1.1 , r1 = 0 , r2 = 1, r3 = 0)
        sim.Send_Position_Sensor(sensorID = 4, objectID = 1)

        for sn in range(0, 4):
            sim.Send_Sensor_Neuron(neuronID=sn, sensorID=sn)

        sim.Send_Motor_Neuron(neuronID=4, jointID=0 )

        for sn in range(0, 4):
            for mn in range(0, 1):
                sim.Send_Synapse(sourceNeuronID = sn , targetNeuronID = 4, weight= wts[sn][mn])



