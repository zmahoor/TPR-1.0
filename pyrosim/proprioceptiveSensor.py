import constants
import numpy as np
import copy


class PROPRIOCEPTIVE_SENSOR:

    def __init__(self, sensorID=0, jointIndex=0):
        self.sensorID = sensorID
        self.jointIndex = jointIndex

    def Get_Data_From_Simulator(self, simulator):
        self.values = copy.deepcopy(simulator.Get_Sensor_Data(self.sensorID, 0))

    def Get_Value(self):
        return np.mean(self.values)

    def Get_Diff_Value(self):
        return np.sum(np.absolute(np.diff(self.values)))

    def Send_To_Simulator(self,simulator):
        simulator.Send_Proprioceptive_Sensor(sensorID=self.sensorID, jointID=self.jointIndex)
