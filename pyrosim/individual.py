import numpy as np
from pyrosim import PYROSIM
import random
import math
import pickle
import constants as c
import os

from snakebot import ROBOT as SB
from quadruped import ROBOT as QB
from treebot import ROBOT as TB
from starfishbot import ROBOT as SFB


class INDIVIDUAL:

    def __init__(self, i, robotType):

        self.id = i

        self.color = [ random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
        
        self.fitness = 0

        self.sim = None

        self.robotType = robotType

        if robotType == '1' or robotType == '2' or robotType == '3' or robotType == '4': 

            self.robot = TB(robotType, [1.0])

        elif robotType == 'snakebot':

            self.robot = SB(1.0)

        elif robotType == 'quadruped':

            self.robot = QB()

        elif robotType == 'starfishbot':

            self.robot = SFB(1.0)
        else: 
            print "robot not known"
            return

    def __getstate__(self):

        return(self.id, self.color, self.fitness, self.robotType, self.head_trajectory, self.robot)

    def __setstate__(self, state):

        self.id, self.color, self.fitness, self.robotType, self.head_trajectory, self.robot = state

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

    def Compute_Fitness(self, whatToMaximize):

        self.sim.Wait_To_Finish()

        # self.fitness = self.robot.Evaluate(self.sim, whatToMaximize)

        del self.sim

    def Mutate(self):

        self.robot.Mutate()

        self.color = [ random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

    def Print(self):

        print '[', self.id, self.fitness, ']',

    def Store(self):

        path = "../diversity_pool/" + self.robotType

        if not os.path.exists(path):
            os.makedirs(path)

        f = open( path +'/robot_'+str(self.id)+'.dat', 'wb' )
        pickle.dump(self, f)
        f.close()




