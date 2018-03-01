#ifndef VaneDirectionH
#define VaneDirectionH

// For 5V, use 1.0.  For 3.3V use 0.66
#define VDDPERCENTAGE 0.66
#define PowerVoltage 3.3

#include "ADC.h"


class VaneDirection
{
public:
	VaneDirection::VaneDirection();
	bool allowedThreshold(float compareValue, float value);
	float voltageToDegrees(float value, float defaultWindDirection);
	float VaneDirection::currentWindDirection();
	float VaneDirection::getCurrentWindDirection();

private:
	float _direction;
	ADC * _adc;
};

#endif
