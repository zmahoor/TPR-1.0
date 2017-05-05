from pyrosim import PYROSIM
import numpy as np
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle
import sys

wtm = 'distance'

f = open(sys.argv[1]+'.txt','r')
best = pickle.load(f)
f.close()

print 'fitness: ', best.fitness

best.Send_To_Simulator(False,True,600,None,color=np.array([1,1,1]))
best.Get_From_Simulator(wtm)

print 'fitness: ', best.fitness

# best.Start_Evaluate(True, False)
# best.Compute_Fitness(wtm)

