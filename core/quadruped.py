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
        self.num_motor_neurons = 8
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

        self.eyes = EYES(self.head_ID, [0, -c.L, 3*c.R+c.L], 0.015, [1, 0, 0], [0, -1, 0], 0.015)
        self.eyes.Create_Eyes(jointsCreated, objectsCreated)
        self.num_joints = jointsCreated[0]
        self.num_objects = objectsCreated[0]
        self.eyes.Send_Eyes_To_Simulator(sim)
        self.Send_Sensors(sim)
        self.brain.Send_To_Simulator(sim,biasValues)

    def Evaluate(self, sim, whatToMaximize):
        self.Get_Raw_Sensors(sim)
        if whatToMaximize == c.maximizeDistance:
            return self.raw_sensors['P'+str(self.head_ID)+'_X'][-1]

    def Get_Raw_Sensors(self, sim):
        self.raw_sensors = {}
        for s in range(0, 4):
            self.raw_sensors['T'+str(s)] = copy.deepcopy(sim.Get_Sensor_Data(s, 0))

        for s in range(0, 8):
            self.raw_sensors['P'+str(s)] = copy.deepcopy(sim.Get_Sensor_Data(s+4, 0))

        self.raw_sensors['R0'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-3, 0))

        self.raw_sensors['P'+str(self.head_ID)+'_X'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 0))
        self.raw_sensors['P'+str(self.head_ID)+'_Y'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 1))
        self.raw_sensors['P'+str(self.head_ID)+'_Z'] = copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, 2))

    def Get_Head_Trajectory(self, sim):
        self.values = []
        for ind in range(0, 3):
            self.values.append(copy.deepcopy(sim.Get_Sensor_Data(self.num_sensors-1, ind)))
        return self.values

    def Send_Objects(self, sim, color):
        self.num_objects = 0
        # box 
        sim.Send_Box(objectID=self.num_objects, x=0, y=0, z=c.L + c.R, length=c.L, width=2*c.L,
                     height=2*c.R, r=color[0], g=color[1], b=color[2])

        self.head_ID = 0
        self.num_objects += 1

        sim.Send_Cylinder(objectID=self.num_objects, x=-c.L, y=c.L/2, z=c.L+c.R, r1=1, r2=0, r3=0,
                          length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        sim.Send_Cylinder(objectID=self.num_objects, x=-c.L, y=-c.L/2, z=c.L+c.R, r1=1, r2=0, r3=0,
                          length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        sim.Send_Cylinder(objectID=self.num_objects, x=c.L, y=c.L/2, z=c.L+c.R, r1=1, r2=0, r3=0,
                          length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        sim.Send_Cylinder(objectID=self.num_objects, x=c.L, y=-c.L/2, z=c.L+c.R, r1=1, r2=0, r3=0,
                          length=c.L, radius=c.R,  r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        # ## vertical segments
        sim.Send_Cylinder(objectID=self.num_objects, x=-(3/2*c.L+2.5*c.R), y=c.L/2, z=(c.L/2 + c.R), r1=0,
                          r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        sim.Send_Cylinder(objectID=self.num_objects, x=-(3/2*c.L+2.5*c.R), y=-c.L/2, z=(c.L/2 + c.R), r1=0,
                          r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        sim.Send_Cylinder(objectID=self.num_objects, x=(c.L+c.L/2), y=c.L/2, z=(c.L/2 + c.R), r1=0,
                          r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1

        sim.Send_Cylinder(objectID=self.num_objects, x=(c.L+c.L/2), y=0-c.L/2, z=(c.L/2 + c.R), r1=0,
                          r2=0, r3=1, length=c.L, radius=c.R, r=color[0], g=color[1], b=color[2])
        self.num_objects += 1


    def Send_Joints(self, sim):
        self.num_joints = 0
        sim.Send_Joint(jointID=self.num_joints, firstObjectID=0, secondObjectID=1,
                       n1=0, n2=-1, n3=0, x=-c.L/2, y=c.L/2, z=c.L+c.R)
        self.num_joints += 1

        sim.Send_Joint(jointID=self.num_joints, firstObjectID=0, secondObjectID=2,
                       n1=0, n2=-1, n3=0, x=-c.L/2, y=-c.L/2, z=c.L+c.R)
        self.num_joints += 1

        sim.Send_Joint(jointID=self.num_joints, firstObjectID=0, secondObjectID=3,
                       n1=0, n2=1, n3=0, x=c.L/2, y=c.L/2, z=c.L+c.R)
        self.num_joints += 1

        sim.Send_Joint(jointID=self.num_joints, firstObjectID=0, secondObjectID=4,
                       n1=0, n2=1, n3=0, x=c.L/2, y=-c.L/2, z=c.L+c.R)
        self.num_joints += 1

        ############

        sim.Send_Joint(jointID=self.num_joints, firstObjectID=1, secondObjectID=5,
                       n1=0, n2=1, n3=0, x=-3*c.L/2, y=c.L/2, z=c.L+c.R)
        self.num_joints += 1

        sim.Send_Joint(jointID=self.num_joints, firstObjectID=2, secondObjectID=6,
                       n1=0, n2=1, n3=0, x=-3*c.L/2, y=-c.L/2, z=c.L+c.R)
        self.num_joints += 1

        sim.Send_Joint(jointID=self.num_joints, firstObjectID=3, secondObjectID=7,
                       n1=1, n2=-1, n3=0, x=3*c.L/2, y=c.L/2, z=c.L+c.R)
        self.num_joints += 1

        sim.Send_Joint(jointID=self.num_joints, firstObjectID=4, secondObjectID=8,
                       n1=1, n2=-1, n3=0, x=3*c.L/2, y=-c.L/2, z=c.L+c.R)
        self.num_joints += 1

    def Add_Sensors(self):
        self.sensorsCreated = {}
        self.num_sensors = 0
        for s in range(0, 4):
            self.sensorsCreated[self.num_sensors] = c.TOC_SENSOR
            self.num_sensors += 1

        for s in range(0, 8):
            self.sensorsCreated[self.num_sensors] = c.PRO_SENSOR
            self.num_sensors += 1

        self.sensorsCreated[self.num_sensors] = c.RAY_SENSOR
        self.num_sensors += 1

        self.sensorsCreated[self.num_sensors] = c.RAY_SENSOR
        self.num_sensors += 1

        self.sensorsCreated[self.num_sensors] = c.POS_SENSOR
        self.num_sensors += 1

    def Send_Sensors(self, sim):
        for s in range(0, 4):
            sim.Send_Touch_Sensor(sensorID=s, objectID=s+5)

        for s in range(0, 8):
            sim.Send_Proprioceptive_Sensor(sensorID=s+4, jointID=s)
    
        sim.Send_Ray_Sensor(sensorID=self.num_sensors-3, objectID=self.num_objects-1,
                            x=self.eyes.leftPupil[0], y=self.eyes.leftPupil[1],
                            z=self.eyes.leftPupil[2], r1=0, r2=-1, r3=0)

        sim.Send_Ray_Sensor(sensorID=self.num_sensors-2, objectID=self.num_objects-2,
                            x=self.eyes.rightPupil[0], y=self.eyes.rightPupil[1],
                            z=self.eyes.rightPupil[2], r1=0, r2=-1, r3=0)

        sim.Send_Position_Sensor(sensorID=self.num_sensors-1, objectID=0)
