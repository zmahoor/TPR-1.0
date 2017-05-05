import numpy as np
import random
import math
import constants as c
from subprocess import Popen, PIPE
from robot import ROBOT 
from pyrosim import PYROSIM
import pickle
import os

class GENOME:

    def __init__(self,ID):

        self.ID = ID

        self.robot = ROBOT()

        self.age = 0

        self.Reset()

    def __getstate__(self):

        return(self.ID, self.fitness, self.age, self.robot)

    def __setstate__(self, state):

        self.ID, self.fitness, self.age, self.robot = state

    def Age(self):

        self.age = self.age + 1

    def Display(self):

        self.Send_To_Simulator(True,False,c.evaluationTime,None,color=np.array([1,1,1]))

    def Dominates(self,other):

        if ( self.fitness <= other.fitness ):

            if ( self.age <= other.age ):

                if ( (self.fitness == other.fitness) & (self.age==other.age) ):

                    i_am_younger = self.ID > other.ID

                    return i_am_younger
                else:   
                    return True
            else:
                return False
        else:
            return False 

    def Get_Dominated(self):

        return self.dominated

    def Get_Evaluated(self):

        return self.evaluated

    def Get_Fitness(self):

        return self.fitness

    def Get_From_Simulator(self,whatToMaximize):

        self.simulator.Wait_To_Finish()

        self.fitness = self.robot.Evaluate(self.simulator,whatToMaximize)

        self.robot.Get_Raw_Sensors()

        del self.simulator

        self.evaluated = True

    def More_Fit_Than(self,other):

        return self.fitness > other.fitness

    def Mutate(self):

        self.robot.Mutate()

    def Print(self):

        printString = ''

        printString = printString + '[f: '+str(self.fitness)+'] \t'

        printString = printString + '[a: '+str(self.age)+'] \t'

        print printString

    def Reset(self):

        self.evaluated = False

        self.fitness = 0.0

        self.dominated = False

    def Save(self, whatToMaximize):

        if not os.path.exists("../"+ whatToMaximize):
            
            os.makedirs("../"+ whatToMaximize)

        f = open('../'+whatToMaximize+'/robot_'+str(self.ID)+'.txt','wb')

        pickle.dump(self,f)

        f.close()

        # os.rename('tmp.txt','best.txt')
        
    def Send_To_Simulator(self,playBlind,playPaused,evaluationTime,environment,color=np.array([1,1,1])):

        self.simulator = PYROSIM(playBlind,playPaused,evaluationTime)

        self.robot.Send_To_Simulator(self.simulator,color)

        # environment.Send_To_Simulator(self.simulator,self.robot.Num_Body_Parts())

        self.simulator.Start()

    def Set_Dominated(self,dominated):

        self.dominated = dominated

    def Wait_To_Finish(self):

        self.tree.Wait_To_Finish()

