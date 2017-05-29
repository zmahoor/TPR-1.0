import numpy as np
from pyrosim import PYROSIM
import random
# from simpleRobot import ROBOT
from bugRobot import ROBOT
import math
import pickle
import constants as c

class INDIVIDUAL:

    def __init__(self, i, robotType, color=[0.5, 0.5, 0.5], command=0.0):

        self.id = i

        self.color = color
        
        self.fitness = 0

<<<<<<< HEAD
        self.command = command
=======
        self.robotType = robotType
>>>>>>> d4ab1aae9e75b1f7d309162fa8a0487f8b1850c4

        self.sim = None

    def __getstate__(self):

        return(self.id, self.genomeSahpe, self.genome, self.command, self.color, self.fitness)

    def __setstate__(self, state):

        self.id, self.genomeSahpe, self.genome, self.command, self.color, self.fitness = state

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

        # else: self.color = [0.5, 0.5, 0.5]

    def Evaluate(self, pp, pb):

        self.sim = PYROSIM(playPaused=pp, playBlind=pb, evalTime=c.evaluationTime)

        robot = ROBOT(self.sim, self.genome, self.color, self.command)

        self.sim.Start() 

        # self.sim.Wait_To_Finish()

    def Wait_For_Me(self):

        self.sim.Wait_To_Finish()
        
        del self.sim

    def Compute_Fitness(self):

        self.fitness = np.sum(self.genome)
        # self.fitness = np.random.random() * 2 - 1
        del self.sim

    def Mutate(self):

        self.robot.Mutate()

    def Print(self):

        print '[', self.id, self.fitness, ']',

<<<<<<< HEAD
    def store_Robot_To_File(self):
        brainPath = '../controllers/r_' + str(self.id) + '.txt'

        with open(brainPath,'wb') as f:
            pickle.dump(  self , f )
            f.close()

=======
>>>>>>> d4ab1aae9e75b1f7d309162fa8a0487f8b1850c4



