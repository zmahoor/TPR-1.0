from pyrosim import PYROSIM
import numpy as np
import random
from individualTemplate import INDIVIDUAL
from copy import deepcopy
from database import *
import time
import sys 

# INDIVIDUAL_DURATION = 30
INDIVIDUAL_NUM = 10
GENOME_SHAPE = [5, 8]
# GENOME_SHAPE =[4, 1]

color = [[1,0,0], [0,1,0], [0,0,1], [1,1,0], [1,0,1], [0,1,1], [1,1,1]]
color_index = 0
individual_index = 0

def initialize_population(pop):

    global color_index
    global individual_index


    for i in range(0, INDIVIDUAL_NUM):
        if color_index >= len(color): color_index = 0    

        pop.append(INDIVIDUAL(individual_index, GENOME_SHAPE, color[color_index]))

        color_index += 1
        individual_index += 1

def compete(pop):

    pop_len = len(pop)

    ind1 =  np.random.randint(pop_len)
    ind2 =  np.random.randint(pop_len)

    if pop_len > 1:
        while ind2 == ind1: 
            ind2 =  np.random.randint(pop_len)

    if(pop[ind1].fitness > pop[ind2].fitness):
        return (ind1, ind2)

    return (ind2, ind1)

def replace(pop, loser, winner):

    global individual_index

    pop[loser].Kill_From_Database()
    pop[loser] = deepcopy(pop[winner])

    pop[loser].id = individual_index
    pop[loser].Mutate()
    individual_index += 1

def main(argv):

    generation = 1
    population = []

    global color_index
    global individual_index

    initialize_population(population) 

    while True:

        print generation,':',
        for p in population: print '[', p.id, p.fitness, ']',
        print 

        [p.Evaluate(False, True) for p in population] 

        [p.Compute_Fitness() for p in population]

        (winner, loser) = compete(population)

        replace(population, loser, winner)

        generation += 1

        if generation == 2: break

if __name__ == "__main__":
   main(sys.argv[1:])


