
from pyrosim import PYROSIM
import matplotlib.pyplot as plt
import numpy as np
from robot import ROBOT
import random

for i in range(0, 10):
    sim = PYROSIM(playPaused=False , evalTime=200)

    robot = ROBOT(sim, random.random()*2 - 1)

    sim.Start()

    sim.Wait_To_Finish()