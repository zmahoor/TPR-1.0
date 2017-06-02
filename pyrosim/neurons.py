import constants as c
from neuron import NEURON
import random

class NEURONS: 

    def __init__(self,numSensorNeurons,numMotorNeurons, sensorsList, biasValues):

        self.numSensorNeurons = numSensorNeurons

        self.numMotorNeurons = numMotorNeurons

        self.numBiasNeurons = len(biasValues)

        self.sensorsList = sensorsList

        self.Create_Bias_Neurons()

        self.Create_Sensor_Neurons()

        self.Create_Hidden_Neurons()

        self.Create_Motor_Neurons()

    def Mutate(self):

        mutType = random.randint(1,2)

        # if ( mutType == 0 ):

        #   self.Mutate_Sensor_Neurons()

        if ( mutType == 1 ):

            self.Mutate_Hidden_Neurons()
        else:
            self.Mutate_Motor_Neurons()

    def Print(self):

        for b in self.biasNeurons:

            self.biasNeurons[b].Print()

        for s in self.sensorNeurons:

            self.sensorNeurons[s].Print()

        for h in self.hiddenNeurons:

            self.hiddenNeurons[h].Print()

        for m in self.motorNeurons:

            self.motorNeurons[m].Print()

    def Send_To_Simulator(self,simulator, biasValues):

        for b in range(0, self.numBiasNeurons):
            
            self.biasNeurons[b].Send_Bias_Neuron_To_Simulator(simulator, biasValues[b])

        for s in range(0,self.numSensorNeurons):

            self.sensorNeurons[s].Send_Sensor_Neuron_To_Simulator(simulator)

        for h in range(0,c.NUM_HIDDEN_NEURONS):

            self.hiddenNeurons[h].Send_Hidden_Neuron_To_Simulator(simulator)

        for m in range(0,self.numMotorNeurons):

            self.motorNeurons[m].Send_Motor_Neuron_To_Simulator(simulator,m)


# -------------------- Private functions ---------------------

    def Create_Bias_Neurons(self):

        self.biasNeurons = {}

        for b in range(0, self.numBiasNeurons):

            self.biasNeurons[b] = NEURON(c.BIAS_NEURON, b)

    def Create_Sensor_Neurons(self):

        rayAdded = False

        self.sensorNeurons = {}

        ind=0
        for s in range(0,self.numSensorNeurons):

            if(self.sensorsList[s] == c.POS_SENSOR):

                self.sensorNeurons[ind] = NEURON(c.SENSOR_NEURON,self.numBiasNeurons+ind,s,0)
                ind += 1
                self.sensorNeurons[ind] = NEURON(c.SENSOR_NEURON,self.numBiasNeurons+ind,s,1)
                ind += 1
                self.sensorNeurons[ind] = NEURON(c.SENSOR_NEURON,self.numBiasNeurons+ind,s,2)

            elif(self.sensorsList[s] == c.PRO_SENSOR or self.sensorsList[s] == c.TOC_SENSOR 
                or self.sensorsList[s] == c.LIT_SENSOR):
                self.sensorNeurons[ind] = NEURON(c.SENSOR_NEURON,self.numBiasNeurons+ind,s)
                ind += 1

            # elif(self.sensorsList[s] == c.RAY_SENSOR and not rayAdded):
            #     rayAdded = True
            #     self.sensorNeurons[ind] = NEURON(c.SENSOR_NEURON,self.numBiasNeurons+ind,s)
            #     ind += 1

        self.numSensorNeurons = len(self.sensorNeurons)

        # for s in self.sensorNeurons:

        #     print self.sensorNeurons[s].ID, self.sensorNeurons[s].sensorID, self.sensorNeurons[s].valueIndex

    def Create_Hidden_Neurons(self):

        self.hiddenNeurons = {}

        for h in range(0,c.NUM_HIDDEN_NEURONS):

            self.hiddenNeurons[h] = NEURON(c.HIDDEN_NEURON, 
                self.numBiasNeurons+self.numSensorNeurons + h)

    def Create_Motor_Neurons(self):

        self.motorNeurons = {}

        for m in range(0,self.numMotorNeurons):

            self.motorNeurons[m] = NEURON(c.MOTOR_NEURON, 
                self.numBiasNeurons+ self.numSensorNeurons + c.NUM_HIDDEN_NEURONS + m)

        # print len(self.motorNeurons)
    # def Mutate_Sensor_Neurons(self):

    #   s = random.randint(0,self.numSensorNeurons-1)

    #   self.sensorNeurons[s].Mutate()

    def Mutate_Hidden_Neurons(self):

        h = random.randint(0,c.NUM_HIDDEN_NEURONS-1)

        self.hiddenNeurons[h].Mutate()

    def Mutate_Motor_Neurons(self):

        m = random.randint(0,self.numMotorNeurons-1)

        self.motorNeurons[m].Mutate()

