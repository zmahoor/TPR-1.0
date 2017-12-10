import sys
sys.path.append('../pyrosim')
from pyrosim import PYROSIM
from individual import INDIVIDUAL
from copy import deepcopy
import pickle
import constants as c
import time
import subprocess


def adjust_windows():
	script = '''tell application "System Events"
    set position of first window of application process "simulator" to {700, 1}
	end tell

	set the_title to "TPR:"
	tell application "System Events"
		repeat with p in (every process whose background only is false)
			repeat with w in every window of p
				if (name of w) contains the_title then
					tell p
						set frontmost to true
						perform action "AXRaise" of w
					end tell
				end if
			end repeat
		end repeat
	end tell'''

	proc = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	stdout_output = proc.communicate(script)[0]
	print stdout_output


f = open(sys.argv[1], 'r')
individual = pickle.load(f)
f.close()
print c.NUM_BIAS_NEURONS, c.evaluationTime
individual.Start_Evaluate(False, False, c.NUM_BIAS_NEURONS*[1.0] + [1.0])

# for command in [-1, +1]:
# 	wordVector = c.NUM_BIAS_NEURONS*[1.0] + [command]
# 	individual.Start_Evaluate(False, False, wordVector)

# time.sleep(0.01)
# adjust_windows()
# print 'fitness: ', individual.fitness

