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
#include <stdlib.h>
#include <math.h>

VaneDirection::VaneDirection() {
	_adc = new ADC();

	//Default set to North or 0 
	float _direction = 0.0;
}

int VaneDirection::getWindDirection()
{
  
	float value = _adc->readVoltage();
  
  setupDirectionArray();
  
  float min = 10;
  int direction = 0;

  
  for(int i=0; i < directionVoltageLength; i++){
      if(fabs(value - directionVoltages[i]) < min){
        min = fabs(value - directionVoltages[i]);
        direction = i;
      }
  }
  return direction;

}


void VaneDirection::setupDirectionArray(){
  // Initialize array with directional values in volts
  directionVoltages[NORTH] =     nV;
  directionVoltages[NORTHEAST] = neV;
  directionVoltages[EAST] =      eV;
  directionVoltages[SOUTHEAST] = seV;
  directionVoltages[SOUTH] =     sV;
  directionVoltages[SOUTHWEST] = swV;
  directionVoltages[WEST] =      wV;
  directionVoltages[NORTHWEST] = nwV;

}



int main() {
	VaneDirection* vane = new VaneDirection();

	printf("current direction: %d\n", vane->getWindDirection());
}
