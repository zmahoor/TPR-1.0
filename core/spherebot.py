import sys
sys.path.append('../pyrosim')
from pyrosim import PYROSIM
import constants as c
import copy
from eyes import EYES
from brain import BRAIN

class ROBOT:

    def __init__(self):
        self.Initialize_Body()
        self.brain = BRAIN(self.num_sensors, self.num_motor_neurons,
                           self.sensorsCreated)

    def Initialize_Body(self):
        self.num_joints = 0
        self.num_objects = 0
        self.head_ID = 0
        self.num_sensors = 0
        self.num_motor_neurons = 1
        self.sensorsCreated = {}
        self.Add_Sensors()
        print self.num_sensors, self.num_motor_neurons, self.sensorsCreated
    
    def Mutate(self):
        self.brain.Mutate()

    def Send_To_Simulator(self, sim, color, biasValues):
        self.Send_Objects(sim, color)
        self.Send_Joints(sim)

        jointsCreated = {0: self.num_joints}
        objectsCreated = {0: self.num_objects}

        self.eyes = EYES(self.head_ID, [0, -c.L/4, 2*c.L], 0.015, [1, 0, 0], [0, -1, 0], 0.015)
        self.eyes.Create_Eyes(jointsCreated, objectsCreated)

        self.num_joints = jointsCreated[0]
        self.num_objects = objectsCreated[0]

        self.eyes.Send_Eyes_To_Simulator(sim)
        self.Send_Sensors(sim)
        self.brain.Send_To_Simulator(sim, biasValues)

    def Evaluate(self, sim, whatToMaximize):
        self.Get_Raw_Sensors(sim)
        if whatToMaximize == c.maximizeDistance:
            return self.raw_sensors['P'+str(self.head_ID)+'_X'][-1] 

    def Send_Objects(self, sim, color):
        self.num_objects =0
        sim.Send_Sphere(objectID=self.num_objects, x=0, y=0, z=c.L, mass=0.5,
                        radius=c.L, r=color[0], g=color[1], b=color[2])
        self.head_ID = self.num_objects
        self.num_objects +=1

        sim.Send_Cylinder(objectID=self.num_objects, x=0, y=0, z=c.L, r1=1, r2=0, r3=0,
                          length=c.L, radius=c.R/2, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        sim.Send_Sphere(objectID=self.num_objects, x=(c.L-c.R)/2, y=0, z=c.L, radius=c.R,
                        r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

    def Send_Joints(self, sim):
        self.num_joints = 0
        sim.Send_Joint(jointID=self.num_joints, firstObjectID=0, secondObjectID=1,
                       n1=0, n2=1, n3=0, x=0, y=0, z=c.L, lo=-c.PI/2, hi=c.PI/2)
        self.num_joints += 1

        sim.Send_Joint(jointID=self.num_joints, firstObjectID=1, secondObjectID=2,
                       n1=-1, n2=0, n3=0, x=(c.L-c.R), y=0, z=c.L, lo=0, hi=0)
        self.num_joints += 1

    def Get_Raw_Sensors(self, sim):
        self.raw_sensors = {'T0': copy.deepcopy(sim.Get_Sensor_Data(0, 0)),
                            'P1': copy.deepcopy(sim.Get_Sensor_Data(1, 0)),
                            'R0': copy.deepcopy(sim.Get_Sensor_Data(2, 0)),
                            'P' + str(self.head_ID) + '_X': copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 0)),
                            'P' + str(self.head_ID) + '_Y': copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 1)),
                            'P' + str(self.head_ID) + '_Z': copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 2))}

    def Get_Head_Trajectory(self, sim):
        self.values = []
        for ind in range(0, 3):
            self.values.append(copy.deepcopy(sim.Get_Sensor_Data(4, ind)))
        return self.values
    
    def Add_Sensors(self):
        self.sensorsCreated = {}
        self.num_sensors = 0

        self.sensorsCreated[self.num_sensors] = c.TOC_SENSOR
        self.num_sensors += 1

        self.sensorsCreated[self.num_sensors] = c.PRO_SENSOR
        self.num_sensors += 1

        self.sensorsCreated[self.num_sensors] = c.RAY_SENSOR
        self.num_sensors += 1

        self.sensorsCreated[self.num_sensors] = c.RAY_SENSOR
        self.num_sensors += 1

        self.sensorsCreated[self.num_sensors] = c.POS_SENSOR
        self.num_sensors += 1

    def Send_Sensors(self, sim):
        sim.Send_Touch_Sensor(sensorID=0, objectID=0)
        sim.Send_Proprioceptive_Sensor(sensorID=1, jointID=0)

        sim.Send_Ray_Sensor(sensorID=2, objectID=self.num_objects-2,
                            x=self.eyes.leftPupil[0], y=self.eyes.leftPupil[1],
                            z=self.eyes.leftPupil[2], r1=0, r2=-1, r3=0)

        sim.Send_Ray_Sensor(sensorID=3, objectID=self.num_objects-1,
                            x=self.eyes.rightPupil[0], y=self.eyes.rightPupil[1],
                            z=self.eyes.rightPupil[2], r1=0, r2=-1, r3=0)

        sim.Send_Position_Sensor(sensorID=4, objectID=0)

