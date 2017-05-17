import numpy as np
from pyrosim import PYROSIM
import random

from snakebot import ROBOT as SB
from quadruped import ROBOT as QB
from treebot import ROBOT as TB
from starfishbot import ROBOT as SFB

from environment import ENVIRONMENT

import constants as c

color = np.random.random(3)

biasValues = [1.0, -1.0]
# genome = np.random.random(genomeSahpe) * 2 - 1
# genome = np.full(genomeSahpe, 1.0)

sim = PYROSIM(playPaused= True, playBlind=False, evalTime=200)

# robot = TB(1, biasValues)
# robot = SB(1.0)
robot = SFB(1.0)
robot.Send_To_Simulator(sim, color, 1.0)
# robot.Send_To_Simulator(sim, color, biasValues)

# environment = ENVIRONMENT()
# print "parts: ", robot.Num_Body_Parts()
# environment.Send_To_Simulator(sim, robot.Num_Body_Parts())

sim.Start()
sim.Wait_To_Finish()
# fitness = robot.Evaluate(sim, 'movement')
# robot.Store_Sensors(1)
del sim
# print fitness
