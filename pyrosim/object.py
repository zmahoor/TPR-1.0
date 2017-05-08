import constants as c
import math
from touchSensor import TOUCH_SENSOR
from lightSensor import LIGHT_SENSOR
from positionSensor import POSITION_SENSOR

class OBJECT: 

    def __init__(self,parentNode,childNode,ID,currentNode=None):

        self.ID = ID
        
        self.parent = parentNode

        self.child = childNode

        self.lightSensor = None

        self.touchSensor = None

        self.positionSensor = None

        self.current = currentNode
        
    def Add_Sensors(self,sensorsCreated):

        if self.ID == 0: 

            self.positionSensor = POSITION_SENSOR(sensorID = sensorsCreated[0] , objectIndex = self.ID)

            sensorsCreated[0] = sensorsCreated[0] + 1


        self.touchSensor = TOUCH_SENSOR( sensorID = sensorsCreated[0] , objectIndex = self.ID)

        sensorsCreated[0] = sensorsCreated[0] + 1

        # self.lightSensor = LIGHT_SENSOR( sensorID = sensorsCreated[0] , objectIndex = self.ID)

        # sensorsCreated[0] = sensorsCreated[0] + 1


    def Store_Sensors(self, raw_sensors):

        if self.positionSensor:

            raw_sensors["P"+str(self.ID)+"_X"] = self.positionSensor.values[0]
            raw_sensors["P"+str(self.ID)+"_Y"] = self.positionSensor.values[1]
            raw_sensors["P"+str(self.ID)+"_Z"] = self.positionSensor.values[2]

        if self.lightSensor:

            raw_sensors["L"+str(self.ID)] = self.lightSensor.values

        if self.touchSensor:

            raw_sensors["T"+str(self.ID)] = self.touchSensor.values

    def Get_Light_Sensor_Value(self):

        if ( self.lightSensor ):

            return self.lightSensor.Get_Mean_Value()
        else:
            return 0

    def Get_Position_Sensor_Value(self):

        if (self.positionSensor):

            return self.positionSensor.Get_Mean_Z_Value()
        else:
            return 0

    def Get_Sensor_Data_From_Simulator(self,simulator):

        if ( self.lightSensor ):

            self.lightSensor.Get_Data_From_Simulator(simulator)

        if ( self.touchSensor ):

            self.touchSensor.Get_Data_From_Simulator(simulator)

        if(self.positionSensor):

            self.positionSensor.Get_Data_From_Simulator(simulator)

    def Print(self):

        outputString = ''

        outputString = outputString + str(self.ID)

        return outputString

    def Send_To_Simulator(self,simulator,color):

        if self.parent == None: 

            x = self.current.x
            y = self.current.y 
            z = self.current.z

            simulator.Send_Sphere(objectID = self.ID, x=x, y=y, z=z, mass = 0.05,
                radius = c.headRadius, r=color[0], g=color[1], b=color[2])

        else:

            x = (self.parent.x + self.child.x) / 2.0
            y = (self.parent.y + self.child.y) / 2.0
            z = (self.parent.z + self.child.z) / 2.0

            r1 = self.child.x - self.parent.x
            r2 = self.child.y - self.parent.y
            r3 = self.child.z - self.parent.z

            xDiff = self.child.x - self.parent.x
            yDiff = self.child.y - self.parent.y
            zDiff = self.child.z - self.parent.z

            length = math.sqrt( math.pow(xDiff,2.0) + math.pow(yDiff,2.0) + pow(zDiff,2.0) )

            simulator.Send_Cylinder(objectID=self.ID, x=x, y=y, z=z, r1=r1, r2=r2, r3=r3, length=length, radius=c.radius, r=color[0], g=color[1], b=color[2])

        if ( self.lightSensor ):

            self.lightSensor.Send_To_Simulator(simulator) 

        if ( self.touchSensor ):

            self.touchSensor.Send_To_Simulator(simulator)

        if ( self.positionSensor ):

            self.positionSensor.Send_To_Simulator(simulator)
