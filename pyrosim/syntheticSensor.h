#ifndef _SYNTHETIC_SENSOR_H
#define _SYNTHETIC_SENSOR_H

#include <ode/ode.h>

class NEURON;

class SYNTHETIC_SENSOR {

private:

	int ID;

	double *values; 

        NEURON *mySensorNeuron;

public:
	SYNTHETIC_SENSOR(int myID, int evalPeriod);

	~SYNTHETIC_SENSOR(void);

        void Connect_To_Sensor_Neuron(NEURON *sensorNeuron);

        int  Get_ID(void);

        void Update_Sensor_Neurons(int t);

	void Write_To_Python(int evalPeriod);
};

#endif
