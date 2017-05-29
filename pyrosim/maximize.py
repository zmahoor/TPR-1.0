from afpo import AFPO

from environment import ENVIRONMENT

import sys

whatToMaximize = sys.argv[1]

# environment = ENVIRONMENT()

environment = None

maxDepth = 4

afpo = AFPO(whatToMaximize, maxDepth)

afpo.Evolve(environment)

