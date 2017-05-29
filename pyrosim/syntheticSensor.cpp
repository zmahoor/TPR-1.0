#ifndef _SYNTHETIC_SENSOR_CPP
#define _SYNTHETIC_SENSOR_CPP

#include "iostream"

#include "syntheticSensor.h"

#include "neuron.h"


SYNTHETIC_SENSOR::SYNTHETIC_SENSOR(int myID, int evalPeriod) {

	ID = myID;

	values = new double[evalPeriod];

	for (int t = 0 ; t < evalPeriod ; t++ ) {

		std::cin >> values[t]; 
	}

        mySensorNeuron = NULL;
}

SYNTHETIC_SENSOR::~SYNTHETIC_SENSOR(void) {

}

void SYNTHETIC_SENSOR::Connect_To_Sensor_Neuron(NEURON *sensorNeuron) {

        mySensorNeuron = sensorNeuron;
}

int  SYNTHETIC_SENSOR::Get_ID(void) {

        return ID;
}

void SYNTHETIC_SENSOR::Update_Sensor_Neurons(int t) {

        if ( mySensorNeuron ) {

                mySensorNeuron->Set( values[t] );
	}
}

void SYNTHETIC_SENSOR::Write_To_Python(int evalPeriod) {

        char outString[1000000];

        sprintf(outString,"%d %d ",ID,1);

        for ( int  t = 0 ; t < evalPeriod ; t++ ) 

                sprintf(outString,"%s %f ",outString,values[t]);

        sprintf(outString,"%s \n",outString);

        std::cout << outString;
}

#endif
