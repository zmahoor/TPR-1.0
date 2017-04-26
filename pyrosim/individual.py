import numpy as np
from pyrosim import PYROSIM
import random
from robot import ROBOT
import math
import pickle
import constants as c

class INDIVIDUAL:

    def __init__(self, i):

        self.id = i

        self.genome = np.random.random(4) * 2 - 1

        self.color = [ random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
        
        self.fitness = 0

        self.sim = None

        self.robot = ROBOT()

    def __getstate__(self):

        return(self.id, self.genome, self.color, self.fitness, self.robot)

    def __setstate__(self, state):

        self.id, self.genome, self.color, self.fitness, self.robot = state

    def Start_Evaluate(self, pp, pb):

        self.sim = PYROSIM(playPaused=pp , playBlind=pb, evalTime=c.evaluationTime)
        # robot = ROBOT(self.sim, self.genome, self.color)
        self.robot.Send_To_Simulator(self.sim, self.color)
        self.sim.Start()

    def Compute_Fitness(self, whatToMaximize):

        self.sim.Wait_To_Finish()

        # x = self.sim.Get_Sensor_Data(sensorID=4 , s=0 )
        # y = self.sim.Get_Sensor_Data(sensorID=4 , s=1 )
        # z = self.sim.Get_Sensor_Data(sensorID=4 , s=2 )

        # self.fitness = y[-1]

        # if self.fitness > 40.0:
        #     self.fitness = 40.0

        self.fitness = self.robot.Evaluate(self.sim, whatToMaximize)

    def Mutate(self):

        self.robot.Mutate()

        # geneToMutate = np.random.randint(4)
        # self.genome[geneToMutate] = random.gauss( self.genome[geneToMutate] ,
        #      math.fabs(self.genome[geneToMutate]) )

        self.color = [ random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

    def Print(self):

        print '[', self.id, self.fitness, ']',

    def Store(self):

        f = open( 'robot_'+str(self.id)+'.txt', 'wb' )
        pickle.dump(self, f)
        f.close()




