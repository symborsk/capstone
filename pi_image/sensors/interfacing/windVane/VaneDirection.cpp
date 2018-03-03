/*
VaneDirection.cpp
Created by Dallin Toth 

Adapted code from SDL_Weather_80422.cpp extracted to only
include the wind vane direction sensor as a separated process

INCLUDE REFERENCES AND LICENSING INFO****


*/
#include <time.h>
#include <stdio.h>
#include "VaneDirection.h"
#include <wiringPi.h>



VaneDirection::VaneDirection() {
	_adc = new ADC();

	//Default set to North or 0 
	float _direction = 0.0;
}

bool VaneDirection::allowedThreshold(float compareValue, float value)
{
#define VARYVALUE 0.15

	if ((value > (compareValue * (1.0 - VARYVALUE))) && (value < (compareValue *(1.0 + VARYVALUE))))
	{

		return true;

	}

	return false;

}

float VaneDirection::voltageToDegrees(float value, float defaultWindDirection)
{
printf("voltage: %f\n", value);

	// Note:  The original documentation for the wind vane says 16 positions.  Typically only recieve 8 positions.  And 315 degrees was wrong.
	if (allowedThreshold(3.84 * VDDPERCENTAGE, value))
		return 0.0;

	if (allowedThreshold(1.98 * VDDPERCENTAGE, value))
		return 22.5;

	if (allowedThreshold(2.25 * VDDPERCENTAGE, value))
		return 45;

	if (allowedThreshold(0.41 * VDDPERCENTAGE, value))
		return 67.5;

	if (allowedThreshold(0.45 * VDDPERCENTAGE, value))
		return 90.0;

	if (allowedThreshold(0.32 * VDDPERCENTAGE, value))
		return 112.5;

	if (allowedThreshold(0.90 * VDDPERCENTAGE, value))
		return 135.0;

	if (allowedThreshold(0.62 * VDDPERCENTAGE, value))
		return 157.5;

	if (allowedThreshold(1.40 * VDDPERCENTAGE, value))
		return 180;

	if (allowedThreshold(1.19 * VDDPERCENTAGE, value))
		return 202.5;

	if (allowedThreshold(3.08 * VDDPERCENTAGE, value))
		return 225;

	if (allowedThreshold(2.93 * VDDPERCENTAGE, value))
		return 247.5;

	if (allowedThreshold(4.62 * VDDPERCENTAGE, value))
		return 270.0;

	if (allowedThreshold(4.04 * VDDPERCENTAGE, value))
		return 292.5;

	if (allowedThreshold(4.34 * VDDPERCENTAGE, value))  // chart in documentation wrong
		return 315.0;

	if (allowedThreshold(3.43 * VDDPERCENTAGE, value))
		return 337.5;

	//Serial.print(" FAIL WIND DIRECTION");
	return defaultWindDirection;  // return previous value if not found


}

float VaneDirection::currentWindDirection()
{
	float voltageValue;

	float Vcc = PowerVoltage;

	// Get the voltage from the vane
	voltageValue = _adc->readVoltage();

	float direction = voltageToDegrees(voltageValue, getCurrentWindDirection());

	return direction;
}

float VaneDirection::getCurrentWindDirection()
{
	return _direction;
}

int main() {
	wiringPiSetupGpio();

	VaneDirection* vane = new VaneDirection();

	printf("current direction: %f\n", vane->currentWindDirection());
}
