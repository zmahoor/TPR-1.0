# parallel hill climber plus novelty search to create diverse behaviours
from pyrosim import PYROSIM
import numpy as np
import random
from copy import deepcopy
import pickle
import argparse
from timer import TIMER

from individual import INDIVIDUAL
from population_Vn import POPULATION

storeTimer = TIMER(5 * 60)

def main(args):

    robotType = args.robot
    arch_thr  = args.arc_thr
    knn       = args.knn
    brange    = args.brange
    popSize   = args.popsize
    numGen    = args.numgen
    internal_novelty = args.internal_novelty

    parents = POPULATION(popSize, robotType)

    parents.Evaluate_Internal_Novelty(False, True)

    for g in range(1, numGen):

        children = deepcopy(parents)
        children.Mutate()

        children.Evaluate_Internal_Novelty(False, True)
        parents.ReplaceWith(children)

        if storeTimer.Time_Elapsed():

            best = self.Find_Best()
            
            if best.fitness > 0:
                self.p[best].Store_To_Diversity_Pool()
                parents.Kill_And_Replace( best )

            storeTimer.Reset()

        print g,
        parents.Print()
        print

    # parents.Store_All_Above_Average()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Diversity pool using either intenal or external diversity.')
    
    parser.add_argument('--robot', '-r', type=str, default='1',\
     help='Morphology types: {1,2,3,4,spherebot\
        ,crabbot, quadruped, shinbot, snakebot}, default=1')

    parser.add_argument('--popsize', '-p', type=int, default=30, help=\
        'Size of populaiton, default=30.')
    
    parser.add_argument('--numgen', '-n', type=int, default=100, help=\
        'Number of generations, default=100.')

    parser.add_argument('--arc_thr', '-t', type=float, default=4.0,
        help='An individual with a fitness larger than this value is inserted into the archive, default=4.0.')

    parser.add_argument('--knn', '-k', type=int, default=3,
        help='K nearest neighbor for calculating fitness in external novelty, default=3.')

    parser.add_argument('--brange', '-b', type=int, default=10,
        help='Divide [0, 1] in brange values for word to vector, default=10.')

    parser.add_argument('--internal_novelty', action='store_true',
        help='A boolean flag, default=False')

    args = parser.parse_args()

    main(args)

