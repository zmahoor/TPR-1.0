import constants as c
import random
import math

class NEURON:

    def __init__(self,type,ID,sensorID=0,valueIndex=0):

        self.type = type

        self.ID = ID

        self.sensorID = sensorID

        self.valueIndex = valueIndex

        self.tau = random.random() * 2  * c.TAU_MAX - c.TAU_MAX

    def Mutate(self):
        
        if(self.type == c.SENSOR_NEURON or self.type == c.BIAS_NEURON):

            return

        self.tau = random.gauss( self.tau , math.fabs(self.tau) )

        if ( self.tau > c.TAU_MAX ):

            self.tau = c.TAU_MAX

        if ( self.tau < -c.TAU_MAX ):

            self.tau = -c.TAU_MAX

    def Print(self):

        print self.ID , self.tau

    def Send_Bias_Neuron_To_Simulator(self, simulator, value):

        simulator.Send_Bias_Neuron(neuronID = self.ID, biasValue=value)

    def Send_Sensor_Neuron_To_Simulator(self,simulator):

        simulator.Send_Sensor_Neuron(neuronID=self.ID, sensorID=self.sensorID, 
            sensorValueIndex=self.valueIndex, tau=self.tau )

    def Send_Hidden_Neuron_To_Simulator(self,simulator):

        simulator.Send_Hidden_Neuron(neuronID=self.ID, tau=self.tau )

    def Send_Motor_Neuron_To_Simulator(self,simulator,jointID):

        simulator.Send_Motor_Neuron(neuronID = self.ID, jointID = jointID , tau = self.tau )


