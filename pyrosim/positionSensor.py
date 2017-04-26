import constants
import numpy as np
import copy

class POSITION_SENSOR:

    def __init__(self, sensorID = 0 ,objectIndex = 0):

        self.sensorID = sensorID

        self.objectIndex = objectIndex

    def Get_Data_From_Simulator(self, simulator):

        self.values = []

        for ind in range(0, 3):

            print simulator.Get_Sensor_Data(self.sensorID, ind)

            self.values.append(copy.deepcopy(simulator.Get_Sensor_Data(self.sensorID, ind)))

    def Get_Mean_Z_Value(self):

        return np.mean(self.values[2,:])

    def Get_Last_Value(self):

        return self.values[2:-1]

    def Send_To_Simulator(self,simulator):

        simulator.Send_Position_Sensor(sensorID = self.sensorID , objectID = self.objectIndex)
