from pyrosim import PYROSIM
import numpy as np
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle

f = open('robot.txt','r')
best = pickle.load(f)
f.close()

best.Start_Evaluate(False)
best.Compute_Fitness()
print 'fitness: ', best.fitness

