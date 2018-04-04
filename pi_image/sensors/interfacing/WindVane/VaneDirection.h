/*
	VaneDirection.h

	By: Dallin Toth

	This is the header file for the windvane object found in 
	VaneDirection.cpp
*/




#ifndef VaneDirection_H
#define VaneDirection_H

// For 5V, use 1.0.  For 3.3V use 0.66
#define VDDPERCENTAGE 0.66
#define PowerVoltage 3.3

#include "ADC.h"

#define NORTH     0
#define NORTHEAST 1
#define EAST      2
#define SOUTHEAST 3
#define SOUTH     4
#define SOUTHWEST 5
#define WEST      6
#define NORTHWEST 7

#define directionVoltageLength 8
float directionVoltages[8];

#define nV  2.047897;
#define neV 1.212122;
#define eV  0.246332;
#define seV 0.48783;
#define sV  0.755713;
#define swV 1.652014;
#define wV  2.457376;
#define nwV 2.308328;




class VaneDirection
{
public:
	VaneDirection();
  void setupDirectionArray(); 
	int getWindDirection();
  void printDirection();
private:
	float _direction;
	ADC * _adc;
};

#endif
