
from pyrosim import PYROSIM
import numpy as np
from robot import ROBOT
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle
from population import POPULATION

parents = POPULATION(20)
parents.Evaluate(False, True)

for g in range(1, 50):

    children = deepcopy(parents)

    # children.Print()

    children.Mutate()
    children.Evaluate(False, True)

    parents.ReplaceWith(children)
    print g,
    parents.Print()

parents.FindFittest()

