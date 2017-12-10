"""
parallel hill climber plus novelty search to create diverse behaviours

"""
from pyrosim import PYROSIM
import numpy as np
import random
from copy import deepcopy
import pickle
import argparse
from timer import TIMER
import os 
import sys 

from individual import INDIVIDUAL
from population import POPULATION
sys.path.append('../bots')
from settings import *


def load_population_from_file(robotType):
    path = '../secondary_population/population_of_' + str(robotType) + '.dat'
    population = None
    try:
        with open(path, 'rb') as f:
            population = pickle.load(f)
        print ('Successful loading the population of: ', robotType)
    except:
        print ('Failed loading the population of: ', robotType)
    return population


def store_population_to_file(population, robotType):
    path = '../secondary_population'
    if not os.path.exists(path):
        os.makedirs(path)
    path += '/population_of_' + str(robotType) + '.dat'
    try:
        with open(path, 'wb') as f:
            pickle.dump(population, f)
        print ('Successful writing population of: ', robotType)
    except:
        print ('Failed writing the population of: ', robotType)


def fill_diversity_pool(robotType, tPeriod, popSize, numBest):
    endTimer = TIMER(tPeriod * 60)
    parents = load_population_from_file(robotType)
    if parents is None:
        parents = POPULATION(popSize, robotType)
    parents.Evaluate_Internal_Novelty(False, True)

    g = 1
    while not endTimer.Time_Elapsed():
        children = deepcopy(parents)
        children.Mutate()

        children.Evaluate_Internal_Novelty(False, True)
        parents.Replace_With(children)

        print g,
        parents.Print()
        g += 1
        print 

    # store top n robots into the diversity pool and kill them from this population.
    for i in range(0, numBest):
        best = parents.Find_Best()
        if parents.p[best].fitness > 0:
            print 'Killing the best: ' + str(best) + ' and replacing it with a random individual.'
            parents.p[best].Store_To_Diversity_Pool()
            parents.Kill_And_Replace( best )

    store_population_to_file( parents, robotType)
    return


def main(args):
    numBest = args.num_top_best
    popSize = args.pop_size
    tPeriod = args.evolution_period
    robotType = args.robot
    fill_diversity_pool(robotType, tPeriod, popSize, numBest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diversity pool using internal novelty.')
    parser.add_argument('--robot', '-r', type=str, default='4',
                        help='Morphology types: {1,2,3,4,spherebot,crabbot,quadruped,shinbot,snakebot}, default=1')

    parser.add_argument('--pop_size', '-p', type=int, default=20, help=
                        'Size of population, default=30.')
    
    parser.add_argument('--evolution_period', '-t', type=int, default=60, help=
                        'Experiment time in minutes, default=60.')

    parser.add_argument('--num_top_best', '-b', type=int, default=60, help=
                        'Top n robots will be stored., default=5.')
    args = parser.parse_args()
    main(args)

