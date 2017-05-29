import time
import numpy as np

class TIMER:

        def __init__(self,countdownDuration):

		self.countdownDuration = countdownDuration

		self.Reset()

	def Reset(self):

        	currentTime = time.time()

        	self.targetTime = currentTime + self.countdownDuration

	def Time_Elapsed(self):

        	currentTime = time.time()

        	return currentTime >= self.targetTime

	def Time_Remaining(self):

        	currentTime = time.time()

        	timeRemaining = self.targetTime - currentTime

        	secondsRemaining = int( np.floor( timeRemaining ) )

        	return secondsRemaining
