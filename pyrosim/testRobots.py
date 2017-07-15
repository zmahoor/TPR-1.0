import numpy as np
from pyrosim import PYROSIM
import random

from snakebot import ROBOT as SNB
from quadruped import ROBOT as QB
from shinbot import ROBOT as SHB
from treebot import ROBOT as TB
from starfishbot import ROBOT as SFB
from crabbot import ROBOT as CB
from spherebot import ROBOT as SPB

import constants as c

color = np.random.random(3)

sim = PYROSIM(playPaused= True, playBlind=False, evalTime=200)

robot = CB()
# robot = QB()
# robot = SHB()
# robot = TB(2)
# robot = SPB()
# robot = SFB()
# robot = SNB()

robot.Send_To_Simulator(sim, color, (c.NUM_BIAS_NEURONS+c.NUM_COMMAND_NEURONS)*[1.0])
sim.Start()
sim.Wait_To_Finish()

# robot.Get_Raw_Sensors(sim)
# print robot.raw_sensors

# fitness = robot.Evaluate(sim, 'movement')
# robot.Store_Sensors(1)
del sim
# print fitness
