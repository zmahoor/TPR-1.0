from pyrosim import PYROSIM
import numpy as np
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle
import sys
import constants as c

f = open(sys.argv[1],'r')
individual = pickle.load(f)
f.close()

command = 1.0
wordVector = c.NUM_BIAS_NEURONS*[1.0] + [command]
individual.Start_Evaluate(False, False, wordVector)

print 'fitness: ', individual.fitness

