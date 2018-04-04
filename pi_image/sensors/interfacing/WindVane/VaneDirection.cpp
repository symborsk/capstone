/*
VaneDirection.cpp
Created by Dallin Toth 

Adapted code from SDL_Weather_80422.cpp extracted to only
include the wind vane direction sensor as a separated process

License information is available in the legal dir


*/
#include <time.h>
#include <stdio.h>
#include "VaneDirection.h"
#include <stdlib.h>
#include <math.h>
#include <string>
using namespace std;


#define LARGEMIN 10
#define DEFAULTDIR 0

VaneDirection::VaneDirection() {
	_adc = new ADC;

  setupDirectionArray();
}

int VaneDirection::getWindDirection()
{
  //Grab the voltage reading
	float value = _adc->readVoltage();
  
  // Default starting variables
  float min = LARGEMIN;
  int direction = DEFAULTDIR;

  //Iterate through all possible voltages and compare
  //the readings; Take smallest difference
  for(int i=0; i < directionVoltageLength; i++){
      if(fabs(value - directionVoltages[i]) < min){
        min = fabs(value - directionVoltages[i]);
        direction = i;
      }
  }
  return direction;

}

void VaneDirection::printDirection(){

  int direction = getWindDirection();
  char * curDirection = "";
  
  switch (direction){
    case 0: curDirection = "N";
            break;
    case 1: curDirection = "NE";
            break;
    case 2: curDirection = "E";
            break;
    case 3: curDirection = "SE";
            break;
    case 4: curDirection = "S";
            break;
    case 5: curDirection = "SW";
            break;
    case 6: curDirection = "W";
            break;
    case 7: curDirection = "NW";
             break;
    default: curDirection = "No reading";
  }
  printf("%s",curDirection);
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
	vane->printDirection();


}
