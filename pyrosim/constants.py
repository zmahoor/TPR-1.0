L = 0.1

R = L/5

PI = 3.14159

headRadius = 2 * R

eyeRadius = 0.015

popSize = 5

numEnvs = 2

# ------------- Things to maximize -----------------

maximizeTouch = 'touch'

maximizeProprioception = 'proprioception'

maximizeHeight = 'height'

maximizeDistance = 'distance'

maximizeLight = 'light'

maximizeRed = 'red'

maximizeGreen = 'green'

maximizeBlue = 'blue'

maximizeWhite = 'white'

maximizeVestibular = 'vestibular'

maximizeMovement = 'movement'

maximizePushing = 'pushing'

maximizeMovementAndHeight = 'movement_height'

maximizeDistanceAndHeight = 'distance_height'

maximizeTouch = 'touch'

# ------------- Other parameters -------------------

evaluationTime = 600

# maxDepth = 2

maxChildren = 2

length = 0.5 / 4.0

radius = 0.05 / 4.0

numGenerations = 10

# ------------------ Robot parameters --------------

JOINT_ANGLE_MAX = -3.14159/8.0

JOINT_ANGLE_MUTATION_MAGNITUDE = 3.14159/8.0

# ----------- Neural network parameters ------------

SENSOR_NEURON = 0

HIDDEN_NEURON = 1

MOTOR_NEURON = 2

BIAS_NEURON = 3

POS_SENSOR = 4
PRO_SENSOR = 5
RAY_SENSOR = 6
TOC_SENSOR = 7
LIT_SENSOR = 8

NUM_HIDDEN_NEURONS = 3

TAU_MAX = 1.0
