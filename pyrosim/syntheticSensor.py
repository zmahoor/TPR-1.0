import constants
import numpy as np
import copy

class SYNTHETIC_SENSOR:

    def __init__(self, values, sensorID=0, jointIndex=0):
        self.sensorID = sensorID
        self.jointIndex = jointIndex
        self.values = values

    def Get_Data_From_Simulator(self, simulator):
        self.values = copy.deepcopy(simulator.Get_Sensor_Data(self.sensorID, 0))

    def Get_Value(self):
        return np.mean(self.values)

    def Send_To_Simulator(self, simulator):
        simulator.Send_Synthetic_Sensor(ID=self.sensorID, jointIndex=self.jointIndex, values=self.values)
