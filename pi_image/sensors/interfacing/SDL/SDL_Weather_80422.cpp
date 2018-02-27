/*
  HEAVILY MODIFIED BY DALLIN AND JOEY FOR RASPBERRY PI 
  CHANGE THIS HEADER
  SDL_Weather_80422.cpp - Library for SwitchDoc Labs WeatherRack.
   SparkFun Weather Station Meters
  Argent Data Systems
  Created by SwitchDoc Labs July 27, 2014.
  Released into the public domain.
    Version 1.1 - updated constants to suppport 3.3V
    Version 1.6 - Support for ADS1015 in WeatherPiArduino Board February 7, 2015
*/


#include <time.h>
#include <stdio.h>
#include "SDL_Weather_80422.h"
#include <wiringPi.h>


bool fuzzyCompare(float compareValue, float value)
{
  #define VARYVALUE 0.15
  
   if ( (value > (compareValue * (1.0-VARYVALUE)))  && (value < (compareValue *(1.0+VARYVALUE))) )
   {
     
     return true;
     
   }
   
   return false;
  
  
  
}

float voltageToDegrees(float value, float defaultWindDirection)
{
  
  // Note:  The original documentation for the wind vane says 16 positions.  Typically only recieve 8 positions.  And 315 degrees was wrong.
  
  // For 5V, use 1.0.  For 3.3V use 0.66
#define ADJUST3OR5 0.66
#define PowerVoltage 3.3

  if (fuzzyCompare(3.84 * ADJUST3OR5 , value))
      return 0.0;

  if (fuzzyCompare(1.98 * ADJUST3OR5, value))
      return 22.5;

  if (fuzzyCompare(2.25 * ADJUST3OR5, value))
      return 45;

  if (fuzzyCompare(0.41 * ADJUST3OR5, value))
      return 67.5;

  if (fuzzyCompare(0.45 * ADJUST3OR5, value))
      return 90.0;

  if (fuzzyCompare(0.32 * ADJUST3OR5, value))
      return 112.5;

  if (fuzzyCompare(0.90 * ADJUST3OR5, value))
      return 135.0;

  if (fuzzyCompare(0.62 * ADJUST3OR5, value))
      return 157.5;

  if (fuzzyCompare(1.40 * ADJUST3OR5, value))
      return 180;

  if (fuzzyCompare(1.19 * ADJUST3OR5, value))
      return 202.5;

  if (fuzzyCompare(3.08 * ADJUST3OR5, value))
      return 225;

  if (fuzzyCompare(2.93 * ADJUST3OR5, value))
      return 247.5;

  if (fuzzyCompare(4.62 * ADJUST3OR5, value))
      return 270.0;

  if (fuzzyCompare(4.04 * ADJUST3OR5, value))
      return 292.5;

  if (fuzzyCompare(4.34 * ADJUST3OR5, value))  // chart in documentation wrong
      return 315.0;

  if (fuzzyCompare(3.43 * ADJUST3OR5, value))
      return 337.5;
      
  //Serial.print(" FAIL WIND DIRECTION");
  return defaultWindDirection;  // return previous value if not found
  
  
}



// Interrupt routines
// for mega, have to use Port B - only Port B works.
/*
Interrupt 4 - Pin 19
Interrupt 5 - Pin 18
 
*/




unsigned long lastWindTime;


void serviceInterruptAnem()
{
  printf("anem interrupt routine\n");
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


unsigned long lastRainTime;

void serviceInterruptRain()
{
  unsigned long currentTime=(unsigned long) (micros()-lastRainTime);
  printf("rain interrupt routine: curr time = %lu\n", currentTime);
  lastRainTime=micros();
  if(currentTime>500)   // debounce
  {
       SDL_Weather_80422::_currentRainCount++;
  }

  

  
  
}

long SDL_Weather_80422::_currentWindCount =0;
long SDL_Weather_80422::_currentRainCount =0;
unsigned long SDL_Weather_80422::_shortestWindTime =0;


SDL_Weather_80422::SDL_Weather_80422(int pinAnem, int pinRain)
{
  _pinAnem = pinAnem;
  _pinRain = pinRain;

  _adc = new ADC();


  _currentRainCount = 0;
  _currentWindCount = 0;
  _currentWindSpeed = 0.0;
  _currentWindDirection = 0.0;

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
  printf("finished constructor\n");

}


float SDL_Weather_80422::get_current_rain_total()
{
        printf("current rain count: %li\n", _currentRainCount);
        float rain_amount = 0.2794 * _currentRainCount/2;  // mm of rain - we get two interrupts per bucket
        _currentRainCount = 0;
	return rain_amount;
}

#define WIND_FACTOR 2.400 
float SDL_Weather_80422::current_wind_speed() // in milliseconds
{
  
   printf("inside current wind speed");
  
    // km/h * 1000 msec
    
    _currentWindCount = 0;
    delay(_sampleTime*1000);
    _currentWindSpeed = ((float)_currentWindCount/_sampleTime) * WIND_FACTOR;
  return _currentWindSpeed;
}

float SDL_Weather_80422::get_wind_gust()
{
   
   
  unsigned long latestTime;
  latestTime =_shortestWindTime;
  _shortestWindTime=0xffffffff;
  double time=latestTime/1000000.0;  // in microseconds

  return (1/(time))*WIND_FACTOR/2;

}

float SDL_Weather_80422::current_wind_direction()
{
    float voltageValue;
    
    float Vcc = PowerVoltage;

    // Get the voltage from the vane
    voltageValue = _adc->readVoltage();
   printf("insdie currentwinddir");

    float direction = voltageToDegrees(voltageValue, _currentWindDirection);
    
    return direction;
}



void SDL_Weather_80422::reset_rain_total()
{
	_currentRainCount = 0;
}

float SDL_Weather_80422::accessInternalCurrentWindDirection()
{
   return _currentWindDirection;
}

void SDL_Weather_80422::reset_wind_gust()
{
   _shortestWindTime = 0xffffffff;
}

// ongoing samples in wind

void SDL_Weather_80422::startWindSample(float sampleTime)
{
  
      _startSampleTime = micros();
     
      _sampleTime = sampleTime;
      
}
    


float SDL_Weather_80422::get_current_wind_speed_when_sampling()
{

   unsigned long compareValue;
   compareValue = _sampleTime*1000000;
  
   if (micros() - _startSampleTime >= compareValue)
    {
      // sample time exceeded, calculate currentWindSpeed
      float _timeSpan;
 //     _timeSpan = (unsigned long)(micros() - _startSampleTime);
      _timeSpan = (micros() - _startSampleTime);
 
      _currentWindSpeed = ((float)_currentWindCount/(_timeSpan)) * WIND_FACTOR*1000000;

      _currentWindCount = 0;
      
      _startSampleTime = micros();


      }
      else
      {
        //Serial.println("NOT Triggered");
        //Serial.print("time = ");
        //Serial.println(micros() - _startSampleTime);
        // if not, then return last wind speed
  
      }

  printf("inside current wind speed when sampling");
  
    return _currentWindSpeed;
}

  

 int main() {
  wiringPiSetupGpio();
  SDL_Weather_80422 *station =  new SDL_Weather_80422(16, 20);
  printf("Hello world!\n");
  //station->current_wind_speed();
 printf("current direction: %f\n", station->current_wind_direction());
  printf("Speed: %f, Rain: %f, Dir: %f\n", station->current_wind_speed(), station->get_current_rain_total(), station->current_wind_direction());
  printf("current direction: %f\n", station->current_wind_direction());
  printf("Goodbye world!\n");
}
