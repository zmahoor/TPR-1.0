
from pyrosim import PYROSIM
import matplotlib.pyplot as plt
import numpy as np
from robot import ROBOT
import random
from individual import INDIVIDUAL

for i in range(0, 10):
    individual = INDIVIDUAL()
    individual.Evaluate()
    print 'Fitness: ', individual.fitness
    print




