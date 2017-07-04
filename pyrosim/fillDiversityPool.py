# parallel hill climber plus novelty search to create diverse behaviours
from pyrosim import PYROSIM
import numpy as np
import random
from copy import deepcopy
import pickle
import argparse

from individual import INDIVIDUAL
from population import POPULATION

def main(args):

    robotType = args.robot
    arch_thr  = args.arc_thr
    knn       = args.knn
    brange    = args.brange
    popSize   = args.popsize
    numGen    = args.numgen
    internal_novelty = args.internal_novelty

    parents = POPULATION(popSize, robotType)

    if internal_novelty:
        parents.Evaluate_Internal_Novelty(False, True, brange)

    else:
        parents.Evaluate_External_Novelty(False, True, knn)
        parents.Update_Archive(arch_thr)

    for g in range(1, numGen):

        children = deepcopy(parents)
        children.Mutate()

        if internal_novelty:

            children.Evaluate_Internal_Novelty(False, True, brange)
            parents.ReplaceWith(children)

        else:
            children.Evaluate_External_Novelty(False, True, knn)
            parents.ReplaceWith(children)
            parents.Evaluate_External_Novelty(False, True, knn)
            parents.Update_Archive(arch_thr)

        print g,
        parents.Print()
        print

        if not internal_novelty:
            parents.Print_Archive()

    if internal_novelty:
        parents.Store_All_Above_Average()

    else:
        parents.Store_Archive()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Diversity pool using either intenal or external diversity.')
    
    parser.add_argument('--robot', '-r', type = str, default='1', help='Morphology types: {1,2,3,4,spherebot\
        ,crabbot, quadruped, shinbot, snakebot}, default=1')

    parser.add_argument('--popsize', '-p', type = int, default=30, help=\
        'Size of populaiton, default=30.')
    
    parser.add_argument('--numgen', '-n', type = int, default=100, help=\
        'Number of generations, default=100.')

    parser.add_argument('--arc_thr', '-t', type = float, default=4.0,
        help='An individual with a fitness larger than this value is inserted into the archive, default=4.0.')

    parser.add_argument('--knn', '-k', type=int, default=3,
        help='K nearest neighbor for calculating fitness in external novelty, default=3.')

    parser.add_argument('--brange', '-b', type=int, default=10,
        help='Divide [0, 1] in brange values for word to vector, default=10.')

    parser.add_argument('--internal_novelty', action='store_true',
        help='A boolean flag, default=False')

    args = parser.parse_args()

    main(args)

