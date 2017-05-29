from pyrosim import PYROSIM
import numpy as np
import constants as c

class ROBOT:

    def __init__(self, commands):

        self.num_joints = 0

        self.num_objects = 0

        self.num_sensors = 0

        self.head_ID = 0

        self.genome = np.random.rand(6, 2) * 2 - 1

    def Send_To_Simulator(self, sim, color, biasValue):

        self.Send_Objects(sim, color)

        self.Send_Joints(sim)

        # self.Send_Eyes(sim, [0, -c.L/4, 2*c.L], 0.015, [1,0,0], [0,-1,0], 0.015)

        self.Send_Eyes(sim, [0, -c.L/5, 2.5*c.L], 0.015, [1,0,0], [0,-1,0], 0.015)

        # self.Send_Sensors(sim)

        # self.Send_Neurons(sim)

        # self.Send_Synapses(sim)

    def Send_Objects(self, sim, color):
        # box 
        sim.Send_Sphere(objectID = self.num_objects , x=0, y=0, z=c.L, mass=2.0,
            radius=c.L, r=color[0], g=color[1], b=color[2])
        self.num_objects +=1

        sim.Send_Sphere(objectID = self.num_objects , x=0, y=0, z=2*c.L,
            radius=c.L/2, r=color[0], g=color[1], b=color[2])

        self.head_ID = self.num_objects
        self.num_objects +=1

    def Send_Joints(self, sim):
        self.num_joints = 0
        sim.Send_Joint(jointID = self.num_joints, firstObjectID = 0, secondObjectID = 1,
         n1 =0, n2 =0 , n3 =1, x=0, y=0, lo=0, hi=0, z=2*c.L)

        self.num_joints += 1

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


   


