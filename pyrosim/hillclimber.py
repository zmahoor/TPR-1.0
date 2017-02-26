
from pyrosim import PYROSIM
import matplotlib.pyplot as plt
import numpy as np
from robot import ROBOT
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle

parent = INDIVIDUAL(0)
parent.Start_Evaluate(False)
parent.Compute_Fitness()

for i in range(0, 100):
    child = deepcopy( parent )
    child.Mutate()
    child.Start_Evaluate(True)
    child.Compute_Fitness()

    print '[g:', i+1, ']', '[pw:', parent.genome ,']','[p:' , parent.fitness , ']', '[c:', child.fitness, ']'

    if ( child.fitness > parent.fitness ):
        child.Start_Evaluate(True)
        child.Compute_Fitness()

        parent = child

        f = open('robot.p','w')
        pickle.dump(parent , f )
        f.close()




