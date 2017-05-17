# parallel hill climber plus novelty search to create diverse behaviours
from pyrosim import PYROSIM
import numpy as np
import random
from copy import deepcopy
import pickle

from individual import INDIVIDUAL
from robot import ROBOT
from environment import ENVIRONMENT
from population import POPULATION
import constants as c

robotType = 'starfishbot'

archive_thresh = 2.0

knn = 3

parents = POPULATION(c.popSize, robotType)

parents.Evaluate(False, True, knn)

parents.Update_Archive(archive_thresh)

for g in range(1, c.numGenerations):

    children = deepcopy(parents)

    children.Mutate()

    children.Evaluate(False, True, knn)

    # print g, 
    # children.Print()

    # parents.Update_Archive(1.0)

    parents.ReplaceWith(children)

    parents.Evaluate(False, True, knn)

    parents.Update_Archive(archive_thresh)

    print g,
    parents.Print()
    print

    # parents.Print_Archive()

parents.Store_Archive()
