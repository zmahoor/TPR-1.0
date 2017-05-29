from pyrosim import PYROSIM
import numpy as np
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle
import sys

wtm = 'height'

f = open(sys.argv[1],'r')
best = pickle.load(f)
f.close()

print 'fitness: ', best.fitness

# best.Send_To_Simulator(False,True,600,None,color=np.array([1,1,1]))
# best.Get_From_Simulator(wtm)
# print best.robot.command
# best.robot.command = 0

best.Start_Evaluate(True, False, [0.5])
best.Compute_Fitness(wtm)
# print best.robot.command

