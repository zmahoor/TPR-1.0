import constants as c
import random
import math

class NEURON:

    def __init__(self,type,ID):

        self.type = type

        self.ID = ID

        self.tau = random.random() * 2  * c.TAU_MAX - c.TAU_MAX

    def Mutate(self):

        self.tau = random.gauss( self.tau , math.fabs(self.tau) )

        if ( self.tau > c.TAU_MAX ):

            self.tau = c.TAU_MAX

        if ( self.tau < -c.TAU_MAX ):

            self.tau = -c.TAU_MAX

    def Print(self):

        print self.ID , self.tau

    def Send_Sensor_Neuron_To_Simulator(self,simulator,sensorID):

        simulator.Send_Sensor_Neuron(neuronID=self.ID, sensorID=sensorID, sensorValueIndex=0, tau=self.tau )

    def Send_Hidden_Neuron_To_Simulator(self,simulator):

        simulator.Send_Hidden_Neuron(neuronID=self.ID, tau=self.tau )

    def Send_Motor_Neuron_To_Simulator(self,simulator,jointID):

        simulator.Send_Motor_Neuron(neuronID = self.ID, jointID = jointID , tau = self.tau )

