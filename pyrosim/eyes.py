import constants as c
import math
import numpy as np

from touchSensor import TOUCH_SENSOR
from lightSensor import LIGHT_SENSOR
from positionSensor import POSITION_SENSOR
from raySensor import RAY_SENSOR

class EYES: 

    def __init__(self, head_ID, midpoint, distance, axis1=[1,0,0], axis2=[0,0,-1], 
        eye_radius=0.02):

        self.midpoint = midpoint

        self.distance = distance

        self.axis1 = axis1

        self.axis2 = axis2

        self.eye_radius = eye_radius

        self.head_ID = head_ID

        self.left_raySensor = None

        self.right_raySensor = None

    def Create_Eyes(self, jointsCreated, objectsCreated):

        self.leftEye_ID    = objectsCreated[0]
        self.rightEye_ID   = objectsCreated[0]+1
        self.leftPupil_ID  = objectsCreated[0]+2
        self.rightPupil_ID = objectsCreated[0]+3

        self.numJoints = jointsCreated[0]

        jointsCreated[0]  += 4
        objectsCreated[0] += 4

        if self.distance < self.eye_radius/2.0:
            self.distance = self.eye_radius/2.0

        _axis1 = [self.axis1[i]/np.linalg.norm(self.axis1) for i in range(len(self.axis1))]

        _axis2 = [self.axis2[i]/np.linalg.norm(self.axis2) for i in range(len(self.axis2))]

        # print _axis1, _axis2

        self.lefEye    =[_axis1[i]* -self.distance + self.midpoint[i] for i in range(len(_axis1))]

        self.rightEye  =[_axis1[i]* self.distance + self.midpoint[i] for i in range(len(_axis1))]

        self.leftPupil =[_axis2[i]* self.eye_radius/1.5 + _axis1[i]* -self.distance\
         + self.midpoint[i] for i in range(0, len(_axis1))]

        self.rightPupil=[_axis2[i]* self.eye_radius/1.5 + _axis1[i]* self.distance\
         + self.midpoint[i] for i in range(0, len(_axis1))]

    def Add_Sensors(self,sensorsCreated):

        sensorInd = len(sensorsCreated)

        self.left_raySensor = RAY_SENSOR( sensorID = sensorInd, 
            objectIndex = self.leftPupil_ID, x= self.leftPupil[0],
             y=self.leftPupil[1], z=self.leftPupil[2], r1=0, r2=-1, r3=0)

        sensorsCreated[sensorInd] = c.RAY_SENSOR

        sensorInd = len(sensorsCreated)

        self.right_raySensor = RAY_SENSOR( sensorID = sensorInd,
         objectIndex = self.rightPupil_ID, x=self.rightPupil[0],
         y=self.rightPupil[1], z=self.rightPupil[2], r1=0, r2=-1, r3=0)

        sensorsCreated[sensorInd] = c.RAY_SENSOR

    def Get_Sensor_Data_From_Simulator(self, simulator):

        if self.left_raySensor:

            self.left_raySensor.Get_Data_From_Simulator(simulator)

    def Store_Sensors(self, raw_sensors):

        if self.left_raySensor:

            raw_sensors["R"+str(self.leftPupil_ID)] = self.left_raySensor.values[0]

        if self.right_raySensor:

            raw_sensors["R"+str(self.rightPupil_ID)] = self.left_raySensor.values[0]

    def Send_Eyes_To_Simulator(self, sim):

        joint_ID = self.numJoints

        sim.Send_Sphere(objectID = self.leftEye_ID, 
            x= self.lefEye[0], y= self.lefEye[1], z= self.lefEye[2], 
            mass=0.05, radius = self.eye_radius, r=1, g=1, b=1)

        sim.Send_Sphere(objectID = self.rightEye_ID, 
            x= self.rightEye[0], y= self.rightEye[1], z= self.rightEye[2], 
            mass=0.05, radius = self.eye_radius, r=1, g=1, b=1)

        sim.Send_Sphere(objectID = self.leftPupil_ID, 
            x= self.leftPupil[0], y= self.leftPupil[1], z= self.leftPupil[2], 
            mass=0.05, radius = self.eye_radius/1.5, r=0, g=0, b=0)

        sim.Send_Sphere(objectID = self.rightPupil_ID, 
            x= self.rightPupil[0], y= self.rightPupil[1], z= self.rightPupil[2], 
            mass=0.05, radius = self.eye_radius/1.5, r=0, g=0, b=0)
 
        ###########################JOINTS#######################################

        sim.Send_Joint(jointID = self.numJoints, firstObjectID = self.head_ID,
        secondObjectID = self.leftEye_ID,
        n1 =1, n2 =0, n3 =0, 
        x= self.lefEye[0], y= self.lefEye[1], z= self.lefEye[2],
        lo=0, hi=0)

        self.numJoints += 1

        sim.Send_Joint(jointID = self.numJoints, firstObjectID = self.head_ID,
        secondObjectID = self.rightEye_ID,
        n1 =1, n2 =0, n3 =0, 
        x= self.rightEye[0], y= self.rightEye[1], z= self.rightEye[2], 
        lo=0, hi=0)
        
        self.numJoints += 1

        sim.Send_Joint(jointID = self.numJoints, firstObjectID = self.leftEye_ID, 
        secondObjectID = self.leftPupil_ID,
        n1 =1, n2 =0, n3 =0, 
        x= self.leftPupil[0], y= self.leftPupil[1], z= self.leftPupil[2], 
        lo=0 , hi=0)

        self.numJoints += 1

        sim.Send_Joint(jointID = self.numJoints, firstObjectID = self.rightEye_ID, 
        secondObjectID = self.rightPupil_ID,
        n1 =1, n2 =0, n3 =0, 
        x= self.rightPupil[0], y= self.rightPupil[1], z= self.rightPupil[2], 
        lo=0 , hi=0)

        if ( self.left_raySensor ):

            self.left_raySensor.Send_To_Simulator(sim) 

        if ( self.right_raySensor ):

            self.right_raySensor.Send_To_Simulator(sim)