
from pyrosim import PYROSIM
import numpy as np
from nrobot import ROBOT
import random
from individual import INDIVIDUAL
from copy import deepcopy
import pickle
from population import POPULATION

parents = POPULATION(5)
parents.Evaluate(True)

for g in range(1, 500):

    children = deepcopy(parents)
    children.Mutate()
    children.Evaluate(True)

    parents.ReplaceWith(children)
    print g,
    parents.Print()

parents.FindFittest()

