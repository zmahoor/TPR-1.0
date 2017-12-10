import constants as c
import numpy as np
from proprioceptiveSensor import PROPRIOCEPTIVE_SENSOR


class JOINT: 

    def __init__(self, firstNode, secondNode, nodeWithMyPosition, q, p, r, ID):
        self.firstNode = firstNode
        self.secondNode = secondNode
        self.nodeWithMyPosition = nodeWithMyPosition
        self.q = q
        self.p = p
        self.r = r
        self.ID = ID
        self.propSensor = None

    def Add_Sensors(self, sensorsCreated):
        sensorInd = len(sensorsCreated)
        self.propSensor = PROPRIOCEPTIVE_SENSOR(sensorID=sensorInd, jointIndex=self.ID)
        sensorsCreated[sensorInd] = c.TOC_SENSOR

    def Store_Sensors(self, raw_sensors):
        if self.propSensor:
            raw_sensors["P"+str(self.ID)] = self.propSensor.values

    def Get_Proprioceptive_Sensor_Value(self):
        if self.propSensor:
            return self.propSensor.Get_Diff_Value()
        else:
            return 0

    def Get_Sensor_Data_From_Simulator(self, simulator):
        if self.propSensor:
            self.propSensor.Get_Data_From_Simulator(simulator)

    def Print(self):
        outputString = ''
        outputString = outputString + str(self.ID)
        return outputString

    def Send_To_Simulator(self, simulator):
        firstObjectID = self.firstNode.object.ID
        secondObjectID = self.secondNode.object.ID

        x = self.nodeWithMyPosition.x
        y = self.nodeWithMyPosition.y
        z = self.nodeWithMyPosition.z
        n = self.Compute_Joint_Normal()
        lo = -c.JOINT_ANGLE_MAX
        hi = +c.JOINT_ANGLE_MAX
        simulator.Send_Joint(jointID=self.ID, firstObjectID=firstObjectID, secondObjectID=secondObjectID,
                             x=x, y=y, z=z, n1=n[0], n2=n[1], n3=n[2], lo=lo, hi=hi)

        if self.propSensor:
            self.propSensor.Send_To_Simulator(simulator) 

# -------------------------- Private methods ----------------------------------

    def Compute_Joint_Normal(self):

        P = np.zeros(3)
        P[0] = self.p.x
        P[1] = self.p.y
        P[2] = self.p.z

        Q = np.zeros(3)
        Q[0] = self.q.x
        Q[1] = self.q.y
        Q[2] = self.q.z

        R = np.zeros(3)
        R[0] = self.r.x
        R[1] = self.r.y
        R[2] = self.r.z

        a = Q - P
        b = R - P

        return np.cross(a,b)
