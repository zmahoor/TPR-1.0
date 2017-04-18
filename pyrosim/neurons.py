import constants as c
from neuron import NEURON
import random

class NEURONS: 

        def __init__(self,numSensorNeurons,numMotorNeurons):

		self.numSensorNeurons = numSensorNeurons

		self.numMotorNeurons = numMotorNeurons

		self.Create_Sensor_Neurons()

		self.Create_Hidden_Neurons()

		self.Create_Motor_Neurons()

	def Mutate(self):

		mutType = random.randint(0,2)

		if ( mutType == 0 ):

			self.Mutate_Sensor_Neurons()

		elif ( mutType == 1 ):

			self.Mutate_Hidden_Neurons()
		else:
			self.Mutate_Motor_Neurons()

	def Print(self):

                for s in self.sensorNeurons:

                        self.sensorNeurons[s].Print()

		for h in self.hiddenNeurons:

			self.hiddenNeurons[h].Print()

		for m in self.motorNeurons:

			self.motorNeurons[m].Print()

	def Send_To_Simulator(self,simulator):

                for s in range(0,self.numSensorNeurons):

			self.sensorNeurons[s].Send_Sensor_Neuron_To_Simulator(simulator,s)

                for h in range(0,c.NUM_HIDDEN_NEURONS):

			self.hiddenNeurons[h].Send_Hidden_Neuron_To_Simulator(simulator)

                for m in range(0,self.numMotorNeurons):

			self.motorNeurons[m].Send_Motor_Neuron_To_Simulator(simulator,m)

# -------------------- Private functions ---------------------

	def Create_Sensor_Neurons(self):

		self.sensorNeurons = {}

                for s in range(0,self.numSensorNeurons):

                        self.sensorNeurons[s] = NEURON(c.SENSOR_NEURON,s)

	def Create_Hidden_Neurons(self):

		self.hiddenNeurons = {}

                for h in range(0,c.NUM_HIDDEN_NEURONS):

                        self.hiddenNeurons[h] = NEURON(c.HIDDEN_NEURON,self.numSensorNeurons + h)

	def Create_Motor_Neurons(self):

                self.motorNeurons = {}

                for m in range(0,self.numMotorNeurons):

                        self.motorNeurons[m] = NEURON(c.MOTOR_NEURON,self.numSensorNeurons + c.NUM_HIDDEN_NEURONS + m)

	def Mutate_Sensor_Neurons(self):

		s = random.randint(0,self.numSensorNeurons-1)

		self.sensorNeurons[s].Mutate()

        def Mutate_Hidden_Neurons(self):

                h = random.randint(0,c.NUM_HIDDEN_NEURONS-1)

                self.hiddenNeurons[h].Mutate()

        def Mutate_Motor_Neurons(self):

                m = random.randint(0,self.numMotorNeurons-1)

                self.motorNeurons[m].Mutate()

