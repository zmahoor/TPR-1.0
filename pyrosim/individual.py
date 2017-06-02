import numpy as np
from pyrosim import PYROSIM
import random
import math
import pickle
import constants as c
import os

from snakebot import ROBOT as SNB
from quadruped import ROBOT as QB
from shinbot import ROBOT as SHB
from treebot import ROBOT as TB
from starfishbot import ROBOT as SFB
from crabbot import ROBOT as CB
from spherebot import ROBOT as SPB

class INDIVIDUAL:

    def __init__(self, i, robotType):

        self.id = i

        self.color = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
        
        self.fitness = 0

        self.sim = None

        self.robotType = robotType

        self.head_trajectory = None

        if robotType == '1' or robotType == '2' or robotType == '3' or robotType == '4': 

            self.robot = TB(robotType, [1.0])

        elif robotType == 'snakebot':

            self.robot = SNB([1.0])

        elif robotType == 'quadruped':

            self.robot = QB([1.0])

        elif robotType == 'shinbot':

            self.robot = SHB([1.0])

        elif robotType == 'starfishbot':

            self.robot = SFB([1.0])

        elif robotType == 'spherebot':

            self.robot = SPB([1.0])

        elif robotType == 'crabbot':

            self.robot = CB([1.0])

        else: 
            print "robot not known"
            return

    def __getstate__(self):

        return(self.id, self.color, self.fitness, self.robotType, self.head_trajectory, self.robot)

    def __setstate__(self, state):

        self.id, self.color, self.fitness, self.robotType, self.head_trajectory, self.robot = state

    def Set_ID(self, id):

        self.id = id

    def Set_Color(self, color):

        if color == 'red':
            self.color = [1, 0, 0]

        elif color == 'green':
            self.color = [0, 1, 0]

        elif color == 'blue':
            self.color = [0, 0, 1]

        elif color == 'yellow':
            self.color = [1 ,1, 0]

        elif color == 'purple' or color =='magenta':
            self.color = [1, 0, 1]

        elif color == 'white':
            self.color = [1, 1, 1 ]

        elif color == 'cyan':
            self.color = [0, 1, 1]

        elif color == 'black':
            self.color = [0, 0, 0]

        elif color == 'orange':
            self.color = [1, 153.0/255.0, 0 ]

        # else: self.color = [0.5, 0.5, 0.5]

    def Get_Raw_Sensors(self):

        return self.robot.raw_sensors

    def Get_Head_Trajectory(self):

        self.sim.Wait_To_Finish()

        self.head_trajectory = np.array(self.robot.Get_Head_Trajectory(self.sim))

        # add the first order dervitave to the head trajectory
        # self.head_trajectory = np.vstack([self.head_trajectory, 
        #     np.append(np.diff(self.head_trajectory[0]), [0])])

        # self.head_trajectory = np.vstack([self.head_trajectory, 
        #     np.append(np.diff(self.head_trajectory[1]), [0])])

        # self.head_trajectory = np.vstack([self.head_trajectory,
        #  np.append(np.diff(self.head_trajectory[2]), [0])])

        del self.sim

    def Start_Evaluate(self, pp, pb, command):

        self.sim = PYROSIM(playPaused=pp , playBlind=pb, evalTime=c.evaluationTime)

        self.robot.Send_To_Simulator(self.sim, self.color, command)

        self.sim.Start()

    def Wait_For_Me(self):

        self.sim.Wait_To_Finish()

        self.robot.Get_Raw_Sensors(self.sim)
        
        del self.sim

    def Compute_Fitness(self, whatToMaximize):

        self.sim.Wait_To_Finish()

        # self.fitness = self.robot.Evaluate(self.sim, whatToMaximize)

        del self.sim

    def Mutate(self):

        self.robot.Mutate()

        self.color = [ random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

    def Print(self):

        print '[', self.id, self.fitness, ']',

    def Store_Sensors(self):

        pass

    def Store_To_Diversity_Pool(self):

        path = "../diversity_pool/" + self.robotType

        if not os.path.exists(path):
            os.makedirs(path)

        f = open( path +'/robot_'+str(self.id)+'.dat', 'wb' )
        pickle.dump(self, f)
        f.close()




