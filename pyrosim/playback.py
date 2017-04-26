from pyrosim import PYROSIM
import numpy as np
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle
import sys

wtm = 'movement_height'

f = open('robot_'+sys.argv[1]+'.txt','r')
best = pickle.load(f)
f.close()

best.Start_Evaluate(True, False)
best.Compute_Fitness(wtm)
print 'fitness: ', best.fitness

