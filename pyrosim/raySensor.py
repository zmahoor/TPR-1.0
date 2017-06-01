import constants
import numpy as np
import copy

class  RAY_SENSOR:

    def __init__(self, sensorID=0, objectIndex=0, x=0, y=0, z=0, r1=0, r2=0, r3=0):

        self.sensorID = sensorID

        self.objectIndex = objectIndex

        self.x  = x
        self.y  = y
        self.z  = z

        self.r1 = r1
        self.r2 = r2
        self.r3 = r3

    def Get_Data_From_Simulator(self, simulator):

        self.values = copy.deepcopy(simulator.Get_Sensor_Data(self.sensorID,0))

    def Get_Value(self):

        return np.mean(self.values)

    def Send_To_Simulator(self,simulator):

        simulator.Send_Ray_Sensor(sensorID = self.sensorID , objectID = self.objectIndex,\
            x = self.x , y = self.y , z = self.z , r1 = self.r1 , r2 = self.r2, r3 = self.r3)
