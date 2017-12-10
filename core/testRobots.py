import sys
sys.path.append('../pyrosim')
import numpy as np
import constants as c
from pyrosim import PYROSIM
from crabbot import ROBOT as CB
from crabplusbot import ROBOT as CPB
from frogbot import ROBOT as FB
from humanoid import ROBOT as HB
from quadruped import ROBOT as QB
from quadrupedplus import ROBOT as QPB
from shinbot import ROBOT as SHB
from snakebot import ROBOT as SNB
from snakeplusbot import ROBOT as SNPB
from spherebot import ROBOT as SPB
from starfishbot import ROBOT as SFB
from treebot import ROBOT as TB

color = np.random.random(3)

sim = PYROSIM(playPaused=True, playBlind=False, evalTime=200)

# robot = QPB()
# robot = CPB()
# robot  = FB()
# robot = HB()
# robot = SNPB()
# robot = CB()
# robot = QB()
# robot = SHB()
# robot = TB(2)
# robot = SPB()
robot = SFB()
# robot = SNB()

robot.Send_To_Simulator(sim, color, (c.NUM_BIAS_NEURONS+c.NUM_COMMAND_NEURONS)*[1.0])
sim.Start()
sim.Wait_To_Finish()

print type(sim.dataFromPython)
print sim.dataFromPython.shape

# robot.Get_Raw_Sensors(sim)
# print robot.raw_sensors

# fitness = robot.Evaluate(sim, 'movement')
# robot.Store_Sensors(1)
# del sim
# print fitness
