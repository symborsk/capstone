/*
  SDL_Weather_80422.cpp

  The following is a *very* heavily modified version of the library 
  for this sensor (originally written for Arduino) modified to run 
  on the raspberry pi 3 and to match our own personal usage. 

  By: Joey-Michael Fallone and Dallin Toth

  Original Header: 
  SDL_Weather_80422.cpp - Library for SwitchDoc Labs WeatherRack.
   SparkFun Weather Station Meters
  Argent Data Systems
  Created by SwitchDoc Labs July 27, 2014.
  Released into the public domain.
    Version 1.1 - updated constants to suppport 3.3V
    Version 1.6 - Support for ADS1015 in WeatherPiArduino Board February 7, 2015
*/
#include <signal.h>

#include <stdio.h>
#include <signal.h>
// global var for sig handler 
int printRequested = 0;

void printSignalHandler(int signal) 
{
  if (signal == SIGUSR1)
  {
    printRequested = 1;
  }
}

#include <time.h>
#include "SDL_Weather_80422.h"
#include <wiringPi.h>

#define WIND_FACTOR 2.400 

unsigned long lastWindTime;
unsigned long lastRainTime;

long SDL_Weather_80422::_currentWindCount = 0;
long SDL_Weather_80422::_currentRainCount = 0;
unsigned long SDL_Weather_80422::_shortestWindTime = 0;

SDL_Weather_80422::SDL_Weather_80422(int pinAnem, int pinRain)
{
  _pinAnem = pinAnem;
  _pinRain = pinRain;

  _currentRainCount = 0;
  _currentWindCount = 0;
  _currentWindSpeed = 0.0;
  
  lastWindTime = 0;
  _shortestWindTime = 0xffffffff;
  
  _sampleTime = 5.0;
  
  _startSampleTime = micros();
   
   // set up interrupts
  pinMode(pinAnem, INPUT);	   // pinAnem is input to which a switch is connected
  digitalWrite(pinAnem, HIGH);   // Configure internal pull-up resistor
  pinMode(pinRain, INPUT);	   // pinRain is input to which a switch is connected
  digitalWrite(pinRain, HIGH);   // Configure internal pull-up resistor
  
  // Attach the intterupt to the pin
  wiringPiISR(pinAnem, INT_EDGE_RISING, &serviceInterruptAnem);
  wiringPiISR(pinRain, INT_EDGE_RISING, &serviceInterruptRain);

}

void serviceInterruptAnem()
{
  unsigned long currentTime= (unsigned long)(micros()-lastWindTime);

  lastWindTime=micros();
  if(currentTime>1000)   // debounce
  {
     SDL_Weather_80422::_currentWindCount++;
    if(currentTime<SDL_Weather_80422::_shortestWindTime)
    {
     SDL_Weather_80422::_shortestWindTime=currentTime;
    }
 
  }
 

  
}


void serviceInterruptRain()
{
  unsigned long currentTime=(unsigned long) (micros()-lastRainTime);
  lastRainTime=micros();
  if(currentTime>500)   // debounce
  {
       SDL_Weather_80422::_currentRainCount++;
  }

  
}


float SDL_Weather_80422::getCurrentRainTotal()
{
        float rain_amount = 1.5 * _currentRainCount;  // mm of rain - based on our own calibration
        _currentRainCount = 0;
	return rain_amount;
}

float SDL_Weather_80422::getCurrentWindSpeed() // in milliseconds
{
  
    // km/h * 1000 msec
    
    _currentWindCount = 0;
    delay(_sampleTime*1000);
    _currentWindSpeed = ((float)_currentWindCount/_sampleTime) * WIND_FACTOR;
  return _currentWindSpeed;
}

float SDL_Weather_80422::getWindGust()
{
   
   
  unsigned long latestTime;
  latestTime =_shortestWindTime;
  _shortestWindTime=0xffffffff;
  double time=latestTime/1000000.0;  // in microseconds

  return (1/(time))*WIND_FACTOR;

}

void SDL_Weather_80422::resestRainTotal()
{
	_currentRainCount = 0;
}

void SDL_Weather_80422::resetWindGust()
{
   _shortestWindTime = 0xffffffff;
}

void SDL_Weather_80422::startWindSample(float sampleTime)
{
  
      _startSampleTime = micros();
     
      _sampleTime = sampleTime;
      
}

float SDL_Weather_80422::getSampingWindSpeed()
{

   unsigned long compareValue;
   compareValue = _sampleTime*1000000;
  
   if (micros() - _startSampleTime >= compareValue)
    {
      // sample time exceeded, calculate currentWindSpeed
      float _timeSpan;
      // _timeSpan = (unsigned long)(micros() - _startSampleTime);
      _timeSpan = (micros() - _startSampleTime);
 
      _currentWindSpeed = ((float)_currentWindCount/(_timeSpan)) * WIND_FACTOR*1000000;

      _currentWindCount = 0;
      
      _startSampleTime = micros();

    }
  
  
    return _currentWindSpeed;
}

 int main() 
 {
  wiringPiSetupGpio();
  SDL_Weather_80422 *station =  new SDL_Weather_80422(16, 20);

  if (signal(SIGUSR1, printSignalHandler) == SIG_ERR) {
    printf("Error occurred setting up SIGUSR1 signal handler\n");
  }

  while (1) 
  {
    if (printRequested) {
      FILE * output = fopen(file_path, "a+");
      fprintf(output, "Speed: %f Rain: %f Gust: %f", station->getCurrentWindSpeed(), station->getCurrentRainTotal(), station->getWindGust());
      printRequested = 0;
      fclose(output);
    }
  }
}
