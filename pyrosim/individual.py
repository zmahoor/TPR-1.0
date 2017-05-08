import numpy as np
from pyrosim import PYROSIM
import random
from robot import ROBOT
import math
import pickle
import constants as c
import os

class INDIVIDUAL:

    def __init__(self, i, robotType):

        self.id = i

        self.color = [ random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
        
        self.fitness = 0

        self.sim = None

        self.robotType = robotType

        self.robot = ROBOT(robotType)

    def __getstate__(self):

        return(self.id, self.color, self.fitness, self.robotType, self.robot)

    def __setstate__(self, state):

        self.id, self.color, self.fitness, self.robotType, self.robot = state

    def Get_Head_Trajectory(self):

        self.sim.Wait_To_Finish()

        self.head_trajectory = np.array(self.robot.Get_Head_Trajectory(self.sim))

        # add the first order dervitave to the head trajectory
        self.head_trajectory = np.vstack([self.head_trajectory, 
            np.append(np.diff(self.head_trajectory[0]), [0])])

        self.head_trajectory = np.vstack([self.head_trajectory, 
            np.append(np.diff(self.head_trajectory[1]), [0])])

        self.head_trajectory = np.vstack([self.head_trajectory,
         np.append(np.diff(self.head_trajectory[2]), [0])])

    def Start_Evaluate(self, pp, pb):

        self.sim = PYROSIM(playPaused=pp , playBlind=pb, evalTime=c.evaluationTime)

        self.robot.Send_To_Simulator(self.sim, self.color)

        self.sim.Start()

    def Compute_Fitness(self, fitness_all, whatToMaximize):

        self.sim.Wait_To_Finish()

        # self.fitness = self.robot.Evaluate(self.sim, whatToMaximize)

        del self.sim

    def Mutate(self):

        self.robot.Mutate()

        self.color = [ random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

    def Print(self):

        print '[', self.id, self.fitness, ']',

    def Store(self):

        path = "../" + self.robotType

        if not os.path.exists(path):
            os.makedirs(path)

        f = open( path +'/robot_'+str(self.id)+'.dat', 'wb' )
        pickle.dump(self, f)
        f.close()




