
from pyrosim import PYROSIM
import matplotlib.pyplot as plt
import numpy as np
from individualTemplate import INDIVIDUAL
from copy import deepcopy
import pickle
import sys

sys.path.append('../bots')

from database import DATABASE

mydatabase = DATABASE()
genomeSahpe = [5, 8]

parent = INDIVIDUAL(0, genomeSahpe)
parent.Evaluate(False, False)
parent.Compute_Fitness()

i=0
current_color = ""

while True:
    tmp = mydatabase.Fetch_New_Color()
    if tmp != "": current_color = tmp

    child = deepcopy(parent)
    child.Mutate()
    child.Set_Color(current_color)
    child.Evaluate(False, False)
    child.Compute_Fitness()

    print '[g:', i, ']', '[p:', parent.fitness , ']', '[c:', child.fitness, ']'

    if ( child.fitness > parent.fitness ):
        # child.Evaluate(False, True)
        # child.Compute_Fitness()
        parent = child
    i += 1

    




