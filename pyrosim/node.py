import constants
import math
import random
import pyrosim
import numpy as np
from object import OBJECT
from joint import JOINT

class NODE:

    def __init__(self, parent, myDepth, maxDepth, numChildren, myAngle1, myAngle2, x, y, z):

        self.myDepth = myDepth
        self.numChildren = numChildren
        self.object = None
        self.joint = None
        self.myAngle1 = myAngle1
        self.myAngle2 = myAngle2
        self.x = x
        self.y = y
        self.z = z
        self.children = {}

        if self.myDepth < maxDepth:
            self.Create_Children(maxDepth)
        else:
            self.numChildren = 0

    def Add_Joints(self,parent,grandParent,jointsCreated):
        if self.myDepth == 0:
            # firstNode = self.children[0]
            # secondNode = self.children[1]
            # nodeContainingJointPosition = self
            # q = self.children[0]
            # p = self
            # r = self.children[1]
            # self.joint = JOINT(firstNode,secondNode,nodeContainingJointPosition,q,p,r,jointsCreated[0])
            # jointsCreated[0]+=1
            pass

        elif ( self.myDepth == 1 ):
            # self.joint = None
            firstNode = parent
            secondNode = self
            nodeContainingJointPosition = parent
            q = self
            p = parent
            r = parent
            self.joint = JOINT(firstNode, secondNode, nodeContainingJointPosition, q, p, r, jointsCreated[0])
            jointsCreated[0] += 1
        else:

            firstNode = parent
            secondNode = self
            nodeContainingJointPosition = parent
            q = self
            p = parent
            r = grandParent
            self.joint = JOINT(firstNode, secondNode, nodeContainingJointPosition, q, p, r, jointsCreated[0])

            jointsCreated[0] += 1

        for c in self.children:
            self.children[c].Add_Joints(self,parent, jointsCreated)

    def Add_Objects(self,parent, objectsCreated):
        if self.myDepth == 0:
            # self.object = None
            self.object = OBJECT(None, self.children[0], objectsCreated[0], self)
            objectsCreated[0] += 1

        else:
            self.object = OBJECT(parent,self, objectsCreated[0])
            objectsCreated[0] += 1

        for c in self.children:
            self.children[c].Add_Objects(self, objectsCreated)

    def Add_Sensors(self, sensorsCreated):
        if self.object:
            self.object.Add_Sensors(sensorsCreated)

        if (self.joint) :
            self.joint.Add_Sensors(sensorsCreated)

        for c in self.children:
            self.children[c].Add_Sensors(sensorsCreated)

    def Assign_IDs(self, ID):
        self.ID = ID[0]
        ID[0] += 1
        for c in range(0, self.numChildren):
            self.children[c].Assign_IDs(ID)

    def Create_Children(self, maxDepth):
        for c in range(0,self.numChildren):
            hisAngle1 = self.myAngle1 + random.random()*2.0*3.14159 - 3.14159
            hisAngle2 = self.myAngle2 + random.random()*2.0*3.14159 - 3.14159
            hisX = self.x + constants.length * math.cos(hisAngle1) * math.sin(hisAngle2)
            hisY = self.y + constants.length * math.sin(hisAngle1) * math.sin(hisAngle2)
            hisZ = self.z + constants.length * math.cos(hisAngle2)
            self.children[c] = NODE(self, self.myDepth+1, maxDepth, constants.maxChildren, hisAngle1, hisAngle2,
                                    hisX, hisY, hisZ)

    def Find_Lowest_Point(self, lowestPoint, lowestDepth):
        if self.z < lowestPoint[0]:
            lowestPoint[0] = self.z
            lowestDepth[0] = self.myDepth

        for c in range(0,self.numChildren):
            self.children[c].Find_Lowest_Point(lowestPoint, lowestDepth)

    def Find_Highest_Point(self, highestPoint):
        if self.ID >= 0:
            if self.finalZ > highestPoint[0]:
                highestPoint[0] = self.finalZ

        for c in range(0,self.numChildren):
            self.children[c].Find_Highest_Point(highestPoint)

    def Flip(self):
        self.x = -self.x
        for c in range(0,self.numChildren):
            self.children[c].Flip()

    def Get_Sensor_Data_From_Simulator(self, simulator):
        if ( self.object ):
            self.object.Get_Sensor_Data_From_Simulator(simulator)

        if(self.joint):
            self.joint.Get_Sensor_Data_From_Simulator(simulator)

        for c in range(0,self.numChildren):
            self.children[c].Get_Sensor_Data_From_Simulator(simulator)

    def Store_Sensors(self, raw_sensors):
        if ( self.object ):
            self.object.Store_Sensors(raw_sensors)

        if ( self.joint):
            self.joint.Store_Sensors(raw_sensors)

        for c in range(0,self.numChildren):
            self.children[c].Store_Sensors(raw_sensors)

    def Make_Parent_Of(self, other):
        other.Recalculate_Depth(self.myDepth+1)
        self.children[self.numChildren] = other
        self.numChildren = self.numChildren + 1

    def Move(self, x, y, z):
        self.x = self.x + x
        self.y = self.y + y
        self.z = self.z + z
        for c in range(0,self.numChildren):
            self.children[c].Move(x, y, z)

    def Mutate(self, mutationProbability):
        if random.random() < mutationProbability:
            self.Mutate_Angles()

        for c in range(0,self.numChildren):
            self.children[c].Mutate(mutationProbability)

    def Mutate_Angles(self):
        angle1Change = random.random()*0.1 - 0.05
        angle2Change = random.random()*0.1 - 0.05

        self.Update_Angles(angle1Change,angle2Change)
        for c in self.children:
            self.children[c].Update_Positions(self.x,self.y,self.z)

    def Mutate_Length(self):
        self.x = self.x + random.random()*0.1 - 0.05
        self.y = self.y + random.random()*0.1 - 0.05
        self.z = self.z + random.random()*0.1 - 0.05

    def Number_Of_Nodes(self):
        numNodes = 1
        for c in range(0,self.numChildren):
            numNodes = numNodes + self.children[c].Number_Of_Nodes()

        return numNodes
    
    def Print(self):
        outputString = ''
        for i in range(0, self.myDepth):
            outputString = outputString + '   '

        if self.object:
            outputString = outputString + self.object.Print() 
        else:
            outputString = outputString + 'N'
        print outputString

        for c in range(0, self.numChildren):
            self.children[c].Print()

    def Recalculate_Depth(self, myDepth):
        self.myDepth = myDepth

        for c in range(0, self.numChildren):
            self.children[c].Recalculate_Depth( self.myDepth + 1 )

    def Send_Joints_To_Simulator(self,simulator):

        if self.joint:
            self.joint.Send_To_Simulator(simulator)

        for c in self.children:
            self.children[c].Send_Joints_To_Simulator(simulator)

    def Send_Objects_To_Simulator(self, simulator, color):
        if self.object:
            self.object.Send_To_Simulator(simulator, color)

        for c in self.children:
            self.children[c].Send_Objects_To_Simulator(simulator, color)

    def Size(self):
        size = 1
        for c in self.children:
            size = size + self.children[c].Size()
        return size

    def Sum_Touch(self):
        sumOfTouch = 0
        if self.object:
            sumOfTouch = self.object.Get_Touch_Sensor_Value()

        for c in self.children:
            sumOfTouch = sumOfTouch+self.children[c].Sum_Touch()

        return sumOfTouch

    def Sum_Light(self):
        sumOfLight = 0
        if self.object:
            sumOfLight = self.object.Get_Light_Sensor_Value()

        for c in self.children:
            sumOfLight = sumOfLight + self.children[c].Sum_Light()

        return sumOfLight

    def Sum_Joint_Diff(self):

        sumOfJointDiff = 0
        if self.joint:
            sumOfJointDiff = self.joint.Get_Proprioceptive_Sensor_Value()

        for c in self.children:
            sumOfJointDiff = sumOfJointDiff + self.children[c].Sum_Joint_Diff()

        return sumOfJointDiff

    def Update_Angles(self, angle1Change, angle2Change):
        self.myAngle1 = self.myAngle1 + angle1Change
        self.myAngle2 = self.myAngle2 + angle2Change

        for c in self.children:
            self.children[c].Update_Angles(angle1Change, angle2Change)

    def Update_Positions(self, parentX, parentY, parentZ):
        self.x = parentX + constants.length * math.cos(self.myAngle1) * math.sin(self.myAngle2)
        self.y = parentY + constants.length * math.sin(self.myAngle1) * math.sin(self.myAngle2)
        self.z = parentZ + constants.length * math.cos(self.myAngle2)

        for c in range(0,self.numChildren):
            self.children[c].Update_Positions(self.x,self.y,self.z)
