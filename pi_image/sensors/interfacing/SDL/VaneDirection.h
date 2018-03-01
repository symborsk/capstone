<<<<<<< HEAD
#ifndef VaneDirection_H
#define VaneDirection_H
=======
#ifndef VaneDirectionH
#define VaneDirectionH
>>>>>>> 1ce4412cc52d814b96025c49a8becc6611653393

// For 5V, use 1.0.  For 3.3V use 0.66
#define VDDPERCENTAGE 0.66
#define PowerVoltage 3.3

#include "ADC.h"


class VaneDirection
{
public:
<<<<<<< HEAD
	VaneDirection();
	bool allowedThreshold(float compareValue, float value);
	float voltageToDegrees(float value, float defaultWindDirection);
	float currentWindDirection();
	float getCurrentWindDirection();
=======
	VaneDirection::VaneDirection();
	bool allowedThreshold(float compareValue, float value);
	float voltageToDegrees(float value, float defaultWindDirection);
	float VaneDirection::currentWindDirection();
	float VaneDirection::getCurrentWindDirection();
>>>>>>> 1ce4412cc52d814b96025c49a8becc6611653393

private:
	float _direction;
	ADC * _adc;
};

#endif
