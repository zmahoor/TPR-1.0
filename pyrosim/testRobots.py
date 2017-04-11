import numpy as np
from pyrosim import PYROSIM
import random
# from snakeRobot import ROBOT
# from bugRobot import ROBOT
from quadraped import ROBOT

import constants as c

genomeSahpe = [6, 2]
# genomeSahpe = [5,8]
color = [0, 1, 0]

# genome = np.random.random(genomeSahpe) * 2 - 1

genome = np.full(genomeSahpe, 1.0)

sim = PYROSIM(playPaused= True, playBlind=False, evalTime=c.evaluationTime)

robot = ROBOT(sim, genome, color)

sim.Start() 

sim.Wait_To_Finish()
