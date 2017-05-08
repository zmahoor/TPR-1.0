from node import NODE
from object import OBJECT
from joint import JOINT
import constants as c
import copy
import numpy as np
import random


class BODY:

    def __init__(self):

        self.numObjects = 0

        self.numJoints = 0

        self.numSensors = 0

        self.root = NODE(None,0,c.maxDepth,1,0.0,0.0,0,0,0)

        self.head_ID = 0

        self.Reset()

        self.color = np.random.random(3)

    def Compute_Fitness(self,whatToMaximize):

        if ( whatToMaximize == c.maximizeLight ):

            return -self.Sum_Light()

        if(whatToMaximize == c.maximizeMovement):

            return -self.Sum_Joint_Diff()

        if(whatToMaximize == c.maximizeMovementAndHeight):

            return -(self.Sum_Joint_Diff() * self.Head_Z_Position())

        if(whatToMaximize == c.maximizeDistanceAndHeight):

            return -(self.Head_X_Position() * self.Head_Z_Position())

        if(whatToMaximize == c.maximizeHeight):

            return -self.Head_Z_Position()

        if(whatToMaximize == c.maximizeDistance):

            return -self.Head_X_Position()

        else:
            print 'unknown fitness function ' + whatToMaximize

            exit(0)

    def Get_Sensor_Data_From_Simulator(self,simulator):

        self.root.Get_Sensor_Data_From_Simulator(simulator)

    def Mutate(self):

        numberOfNodes = self.root.children[0].Size()

        probabilityOfNodeMutation = 1.0 / numberOfNodes
 
        self.root.children[0].Mutate(probabilityOfNodeMutation)

    def Print(self):

        self.root.Print()

    def Reset(self):

        self.Create_Mirror_Image()

        self.Assign_IDs()

        self.Add_Objects()

        self.Add_Joints()

        self.Add_Head()

        self.Add_Sensors()

        self.Move_Up()

    def Store_Sensors(self, raw_sensors):

        self.root.Store_Sensors(raw_sensors)

    def Send_To_Simulator(self,simulator,color):

        self.root.Send_Objects_To_Simulator(simulator, color)

        self.root.Send_Joints_To_Simulator(simulator)

    def Sum_Light(self):

        return self.root.Sum_Light()

        sumOfLight = 0

        if ( self.lightSensor ):

            sumOfLight = self.lightSensor.Get_Value()

        for c in range(0,self.numChildren):

            sumOfLight = sumOfLight + self.children[c].Sum_Light()

        print "sumLight: ", sumOfLight

        return sumOfLight

    def Head_Z_Position(self):

        # headZLocation = self.root.object.positionSensor.values[2]

        # count = 0.0

        # for l in headZLocation:

        #     if l >= 3* c.headRadius and l <= (c.maxDepth * c.length + c.headRadius):

        #         count += 1.0

        # return count/len(headZLocation)

        return self.root.object.positionSensor.Get_Mean_Z_Value()

    def Head_X_Position(self):

        return self.root.object.positionSensor.Get_Last_X_Value()

    def Sum_Joint_Diff(self):

        return self.root.Sum_Joint_Diff()

        sumOfJointDiff = 0

        if(self.propSensor):

            sumOfJointDiff = self.propSensor.Get_Diff_Value()

        for c in range(0,self.numChildren):

            sumOfJointDiff = sumOfJointDiff + self.children[c].Sum_Joint_Diff()

        print "sumOfJointDiff: ", sumOfJointDiff

        return sumOfJointDiff

# --------------- Private methods -------------------------

    def Add_Joints(self):

        jointsCreated = {}

        jointsCreated[0] = 0

        self.root.Add_Joints(None,None,jointsCreated)

        self.numJoints = jointsCreated[0]

    def Add_Objects(self):

        objectsCreated = {}

        objectsCreated[0] = 0

        self.root.Add_Objects(None,objectsCreated)

        self.numObjects = objectsCreated[0]

    def Add_Sensors(self):

        sensorsCreated = {}

        sensorsCreated[0] = 0

        self.root.Add_Sensors(sensorsCreated)

        self.numSensors = sensorsCreated[0]

    def Assign_IDs(self):

        ID = {}

        ID[0] = 0

        self.root.Assign_IDs(ID)

    def Create_Mirror_Image(self):

        self.root.children[1] = copy.deepcopy( self.root.children[0] )

        self.root.numChildren = 2

        self.root.children[1].Flip()

    def Move_Up(self):

        lowestPoint = [1000.0]

        lowestDepth = [-1]

        self.root.Find_Lowest_Point(lowestPoint, lowestDepth)

        # the lowest part is the head
        if lowestDepth[0] == 0:
            self.root.Move( 0 , 0, -lowestPoint[0] + c.headRadius )
        else:
            self.root.Move( 0 , 0, -lowestPoint[0] + c.radius )

    def Sum_Light(self):

        return self.root.Sum_Light()

    def Add_Head(self):

        self.root.object.current = self.root

        self.root.object.child   = self.root.children[0]

        self.root.object.parent  = None

        self.root.children[0].joint.r = self.root.children[1]

        self.root.children[1].joint.r = self.root.children[0]

    def L2_Norm(self, mylist):
        n =0.0
        for i in range(len(mylist)):
            n += mylist[i]**2 

        return(n**0.5)

    def Make_Eyes(self, sim, midpoint, distance, axis1=[1,0,0], axis2=[0,0,-1], 
        eye_radius=0.02):

        joint_ID = self.numJoints

        object_ID = self.numObjects
        
        if distance < eye_radius/2.0:
            distance = eye_radius/2.0

        axis1 = [axis1[i] / self.L2_Norm(axis1) for i in range(len(axis1))]

        axis2 = [axis2[i] / self.L2_Norm(axis2) for i in range(len(axis2))]

        # print axis1, axis2

        lefEye    =[axis1[i]* -distance + midpoint[i] for i in range(len(axis1))]

        rightEye  =[axis1[i]* distance + midpoint[i] for i in range(len(axis1))]

        leftPupil =[axis2[i]* eye_radius/1.5 + axis1[i]* -distance + midpoint[i] for i in range(0, len(axis1))]

        rightPupil=[axis2[i]* eye_radius/1.5 + axis1[i]* distance + midpoint[i] for i in range(0, len(axis1))]

        sim.Send_Sphere(objectID = object_ID, 
            x= lefEye[0], y= lefEye[1], z= lefEye[2], 
            mass=0.05, radius = eye_radius, r=1, g=1, b=1)

        # print object_ID

        object_ID += 1

        sim.Send_Sphere(objectID = object_ID, 
            x= rightEye[0], y= rightEye[1], z= rightEye[2], 
            mass=0.05, radius = eye_radius, r=1, g=1, b=1)

        # print object_ID

        object_ID += 1

        sim.Send_Sphere(objectID = object_ID, 
            x= leftPupil[0], y= leftPupil[1], z= leftPupil[2], 
            mass=0.05, radius = eye_radius/1.5, r=0, g=0, b=0)

        # sim.Send_Ray_Sensor(sensorID= self.numSensors, objectID=object_ID, 
        #     x= leftPupil[0], y= leftPupil[1], z= leftPupil[2], r1=0,r2=-1,r3=0)

        object_ID += 1

        # self.numSensors += 1

        sim.Send_Sphere(objectID = object_ID, 
            x= rightPupil[0], y= rightPupil[1], z= rightPupil[2], 
            mass=0.05, radius = eye_radius/1.5, r=0, g=0, b=0)

        # sim.Send_Ray_Sensor(sensorID= self.numSensors, objectID=object_ID, 
        #     x= rightPupil[0], y= rightPupil[1], z= rightPupil[2], r1=0,r2=-1,r3=0)
 
        # self.numSensors += 1

        # print self.numSensors

        ###########################JOINTS#######################################

        sim.Send_Joint(jointID = joint_ID, firstObjectID = self.head_ID,
        secondObjectID = object_ID-3,
        n1 =1, n2 =0, n3 =0, 
        x= lefEye[0], y= lefEye[1], z= lefEye[2],
        lo=0, hi=0)

        # print joint_ID, object_ID-4, object_ID-3

        joint_ID += 1

        sim.Send_Joint(jointID = joint_ID, firstObjectID = self.head_ID,
        secondObjectID = object_ID-2,
        n1 =1, n2 =0, n3 =0, 
        x= rightEye[0], y= rightEye[1], z= rightEye[2], 
        lo=0, hi=0)
        
        # print joint_ID, object_ID-4, object_ID-2

        joint_ID += 1

        sim.Send_Joint(jointID = joint_ID, firstObjectID = object_ID-3, 
        secondObjectID = object_ID-1,
        n1 =1, n2 =0, n3 =0, 
        x= leftPupil[0], y= leftPupil[1], z= leftPupil[2], 
        lo=0 , hi=0)

        # print joint_ID, object_ID-3, object_ID-1

        joint_ID += 1

        sim.Send_Joint(jointID = joint_ID, firstObjectID = object_ID-2 , 
        secondObjectID = object_ID,
        n1 =1, n2 =0, n3 =0, 
        x= rightPupil[0], y= rightPupil[1], z= rightPupil[2], 
        lo=0 , hi=0)

        # print joint_ID, object_ID-2, object_ID




