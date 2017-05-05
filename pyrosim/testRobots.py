import numpy as np
from pyrosim import PYROSIM
import random
# from snakeRobot import ROBOT
# from bugRobot import ROBOT
# from quadraped import ROBOT

from robot import ROBOT

from environment import ENVIRONMENT

import constants as c

# genomeSahpe = [7, 2]
# genomeSahpe = [6,8]
# color = [0, 1, 0]

color = np.random.random(3)

# genome = np.random.random(genomeSahpe) * 2 - 1

# genome = np.full(genomeSahpe, 1.0)

sim = PYROSIM(playPaused= True, playBlind=False, evalTime=200)

# robot = ROBOT(sim, genome, color, command = 0.0)

robot = ROBOT()
robot.Send_To_Simulator(sim, color)

# environment = ENVIRONMENT()
# print "parts: ", robot.Num_Body_Parts()
# environment.Send_To_Simulator(sim, robot.Num_Body_Parts())

sim.Start()
sim.Wait_To_Finish()
fitness = robot.Evaluate(sim, 'movement')
robot.Store_Sensors(1)

# print fitness
