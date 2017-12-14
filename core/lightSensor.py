import numpy as np
import copy

class LIGHT_SENSOR:

    def __init__(self, sensorID=0, objectIndex=0):
        self.ID = sensorID
        self.objectIndex=objectIndex

    def Get_Data_From_Simulator(self, simulator):
        self.values = copy.deepcopy(simulator.Get_Sensor_Data(self.ID, 0))

    def Get_Mean_Value(self):
        return np.mean(self.values)

    def Send_To_Simulator(self, simulator):
        simulator.Send_Light_Sensor(sensorID=self.ID, objectID=self.objectIndex)
