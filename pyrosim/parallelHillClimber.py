# parallel hill climber plus novelty search to create diverse behaviours
from pyrosim import PYROSIM
import numpy as np
from robot import ROBOT
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle
from population import POPULATION
import constants as c
from environment import ENVIRONMENT

wtm = 'distance'

robotType = '1'

parents = POPULATION(c.popSize, wtm, robotType)
parents.Evaluate(False, True)

for g in range(1, c.numGenerations):

    children = deepcopy(parents)

    # children.Print()

    children.Mutate()
    children.Evaluate(False, True)

    parents.ReplaceWith(children)
    print g,
    parents.Print()

parents.Store_All()
# parents.FindFittest()

