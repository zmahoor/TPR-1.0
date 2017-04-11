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

        self.head_ID = 0

        self.Send_Objects(sim, color)

        # self.Send_Joints(sim)

        # self.Make_Eyes(sim, [0, 0, 3*c.R+c.L], 0.015, [1,0,0], [0,-1,0], 0.015)

        # self.Send_Sensors(sim)

        # self.Send_Neurons(sim)

        # self.Send_Synapses(sim, wts)

    def Send_Objects(self, sim, color):
        # box 
        sim.Send_Box(objectID = self.last_objectID , x=0, y=0, z=c.L + c.R, length=c.L, width=2*c.L,
         height=2*c.R, r=color[0], g=color[1], b=color[2])

        self.head_ID = 0
        
        self.last_objectID += 1

        # # red
        sim.Send_Cylinder(objectID = self.last_objectID, x=-c.L, y=c.L/2, z=c.L + c.R, r1=1 , r2=0, r3=0,
         length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        
        self.last_objectID += 1

        # green
        sim.Send_Cylinder(objectID=self.last_objectID, x=-c.L, y=-c.L/2, z=c.L + c.R, r1=1 , r2=0, r3=0,
         length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

        self.last_objectID += 1

        # # # blue
        sim.Send_Cylinder(objectID=self.last_objectID, x=c.L, y=c.L/2, z=c.L + c.R, r1=1 , r2=0, r3=0,
         length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        
        self.last_objectID += 1

        # # #purple
        sim.Send_Cylinder(objectID=self.last_objectID, x=c.L, y=-c.L/2, z=c.L + c.R, r1=1 , r2=0, r3=0,
         length=c.L, radius=c.R,  r=color[0], g=color[1], b=color[2])

        self.last_objectID += 1

        # ## vertical segments
        #red
        sim.Send_Cylinder(objectID=self.last_objectID, x=-(3/2*c.L+c.R), y=c.L/2, z=(c.L/2 + c.R), r1=0,
         r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

        # self.last_objectID += 1

        # # green
        # sim.Send_Cylinder(objectID=self.last_objectID, x=(c.L+c.L/2), y=0, z=(c.L/2 + c.R), r1=0,
        #  r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])

        # self.last_objectID += 1

        # #blue
        # sim.Send_Cylinder(objectID=self.last_objectID, x=0, y=-(c.L/2 + c.L), z=(c.L/2 + c.R), r1=0,
        #  r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        
        # self.last_objectID += 1

        # # purple
        # sim.Send_Cylinder(objectID=self.last_objectID, x=-(c.L+c.L/2), y=0, z=(c.L/2 + c.R), r1=0,
        #  r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
