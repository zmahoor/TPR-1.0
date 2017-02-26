
from pyrosim import PYROSIM
import numpy as np
from robot import ROBOT
import random
from individual import INDIVIDUAL
from copy import deepcopy
from population import POPULATION
from database import *
from threading import Timer
import time


g = 0
commtxt = ""
INDIVIDUAL_DURATION = 3 * 60
prevTime = time.time()


parents = POPULATION(5)
parents.Evaluate(True)
mydatabse = DATABASE()

while True:
    
    g += 1
    # if g == 100: break

    currTime = time.time()
    interval =  (currTime - prevTime)

    if interval >= INDIVIDUAL_DURATION: 

        prevTime = currTime
        commtxt = mydatabse.Fetch_A_Command(2)
        print commtxt


    children = deepcopy(parents)
    children.Mutate()
    children.Evaluate(True)

    parents.ReplaceWith(children)
    print g,
    parents.Print()
    parents.FindFittest()

    

