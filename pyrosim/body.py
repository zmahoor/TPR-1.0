from node import NODE
from object import OBJECT
from joint import JOINT
from eyes import EYES
import constants as c
import copy
import numpy as np
import random


class BODY:

    def __init__(self, maxDepth):
        self.numObjects = 0
        self.numJoints = 0
        self.numSensors = 0
        self.root = NODE(None, 0, maxDepth, 1, 0.0, 0.0, 0, 0, 0)
        self.head_ID = 0
        self.Reset()
        self.color = np.random.random(3)

    def Compute_Fitness(self, whatToMaximize):
        if whatToMaximize == c.maximizeLight:
            return -self.Sum_Light()

        if whatToMaximize == c.maximizeMovement:
            return -self.Sum_Joint_Diff()

        if whatToMaximize == c.maximizeMovementAndHeight:
            return -(self.Sum_Joint_Diff()*self.Head_Z_Position())

        if whatToMaximize == c.maximizeHeight:
            return -self.Head_Z_Position()

        if whatToMaximize == c.maximizeDistance:
            return -self.Head_X_Position()

        else:
            print 'unknown fitness function ' + whatToMaximize
            exit(0)

    def Get_Sensor_Data_From_Simulator(self,simulator):
        self.root.Get_Sensor_Data_From_Simulator(simulator)
        self.eyes.Get_Sensor_Data_From_Simulator(simulator)

    def Get_Head_Trajectory(self, simulator):
        if self.root.object.positionSensor:
            return self.root.object.positionSensor.values

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
        self.Add_Eyes()

    def Add_Eyes(self):
        jointsCreated  = {0: self.numJoints}
        objectsCreated = {0: self.numObjects}

        midpoint = [self.root.x, self.root.y-c.headRadius, self.root.z]

        self.eyes = EYES(self.head_ID, midpoint, 0.015, [1,0,0], [0,-1,0], 0.015)
        self.eyes.Create_Eyes(jointsCreated, objectsCreated)
        self.eyes.Add_Sensors(self.sensorsCreated)

        # print jointsCreated, objectsCreated, sensorsCreated

        self.numSensors = len(self.sensorsCreated)
        self.numJoints  = jointsCreated[0]
        self.numObjects = objectsCreated[0]

    def Store_Sensors(self, raw_sensors):
        self.root.Store_Sensors(raw_sensors)
        self.eyes.Store_Sensors(raw_sensors)

    def Send_To_Simulator(self,simulator,color):
        self.root.Send_Objects_To_Simulator(simulator, color)
        self.root.Send_Joints_To_Simulator(simulator)
        self.eyes.Send_Eyes_To_Simulator(simulator)

    def Sum_Light(self):
        return self.root.Sum_Light()
        sumOfLight = 0

        if self.lightSensor:
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
        if self.propSensor:
            sumOfJointDiff = self.propSensor.Get_Diff_Value()

        for c in range(0, self.numChildren):
            sumOfJointDiff = sumOfJointDiff + self.children[c].Sum_Joint_Diff()

        print "sumOfJointDiff: ", sumOfJointDiff
        return sumOfJointDiff

# --------------- Private methods -------------------------

    def Add_Joints(self):
        jointsCreated = {0: 0}
        self.root.Add_Joints(None,None,jointsCreated)
        self.numJoints = jointsCreated[0]

    def Add_Objects(self):
        objectsCreated = {0: 0}
        self.root.Add_Objects(None,objectsCreated)
        self.numObjects = objectsCreated[0]

    def Add_Sensors(self):
        self.sensorsCreated = {}
        self.root.Add_Sensors(self.sensorsCreated)
        self.numSensors = len(self.sensorsCreated)

    def Assign_IDs(self):
        ID = {0: 0}
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
            self.root.Move(0, 0, -lowestPoint[0] + c.headRadius)
        else:
            self.root.Move(0, 0, -lowestPoint[0] + c.radius)

    def Sum_Light(self):
        return self.root.Sum_Light()

    def Add_Head(self):
        self.root.object.current = self.root
        self.root.object.child = self.root.children[0]
        self.root.object.parent = None
        self.root.children[0].joint.r = self.root.children[1]
        self.root.children[1].joint.r = self.root.children[0]
