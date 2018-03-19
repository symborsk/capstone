/*
  SDL_Weather_80422.h

  The following is a *very* heavily modified version of the library 
  for this sensor (originally written for Arduino) modified to run 
  on the raspberry pi 3 and to match our own personal usage. 

  By: Joey-Michael Fallone and Dallin Toth

  Original header: 
  SDL_Weather_80422.h - Library for Weather Sensor
  Designed for:  SwitchDoc Labs WeatherRack www.switchdoc.com
  Argent Data Systems
  SparkFun Weather Station Meters
  Created by SwitchDoc Labs July 27, 2014.
  Released into the public domain.
    Version 1.1 - updated constants to suppport 3.3V
    Version 1.6 - Support for ADS1015 in WeatherPiArduino Board February 7, 2015
*/
#ifndef SDL_Weather_80422_h
#define SDL_Weather_80422_h

// constant file path for data storage
char * file_path = 
  "/home/thor/capstone/pi_image/sensors/interfacing/SDL/.data/station.dat"


void serviceInterruptAnem();
void serviceInterruptRain();

class SDL_Weather_80422
{
  public:
    SDL_Weather_80422(int pinAnem, int pinRain);
  
    float getCurrentRainTotal();
    float getCurrentWindSpeed();
    float getWindGust();
    void resestRainTotal();
    void resetWindGust();

    static unsigned long _shortestWindTime;
    static long _currentRainCount;
    static long _currentWindCount;

  
  private:

    int _pinAnem;
    int _pinRain;    
    float _sampleTime;

   
   
    unsigned long _startSampleTime;

    float _currentWindSpeed;
   
    
    void startWindSample(float sampleTime);
    float getSampingWindSpeed();
};

#endif

