from afpo import AFPO

from environment import ENVIRONMENT

import sys

whatToMaximize = sys.argv[1]

# environment = ENVIRONMENT()

environment = None

afpo = AFPO(whatToMaximize)

afpo.Evolve(environment)

