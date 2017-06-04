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

robotType      = 'quadruped'

archive_thresh = 4.0

knn = 3

brange = 10

parents = POPULATION(c.popSize, robotType)

# parents.Evaluate_Internal_Novelty(False, True, brange, knn)

parents.Evaluate_External_Novelty(False, True, brange, knn)

parents.Update_Archive(archive_thresh)

for g in range(1, c.numGenerations):

    children = deepcopy(parents)

    children.Mutate()

    # children.Evaluate_Internal_Novelty(False, True, brange, knn)

    children.Evaluate_External_Novelty(False, True, brange, knn)

    # print g, 
    # children.Print()

    parents.ReplaceWith(children)

    parents.Evaluate_External_Novelty(False, True, brange, knn)

    parents.Update_Archive(archive_thresh)

    print g,
    parents.Print()
    print

    # parents.Print_Archive()

# parents.Store_All_Above_Average()
parents.Store_Archive()
