/*
  HEAVILY MODIFIED BY DALLIN AND JOEY FOR RASPBERRY PI
  FIX THIS HEADER
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

#include "ADC.h"


class SDL_Weather_80422
{
  public:
    SDL_Weather_80422(int pinAnem, int pinRain);
  
    float get_current_rain_total();
    float current_wind_speed();
    float current_wind_direction();
    float get_wind_gust();
    void reset_rain_total();
    void reset_wind_gust();
  
  
  
  

    static unsigned long _shortestWindTime;
    static long _currentRainCount;
    static long _currentWindCount;
    

     
    float accessInternalCurrentWindDirection();

  friend void serviceInterruptAnem();
  friend void serviceInterruptRain(); 
  
  private:

    int _pinAnem;
    int _pinRain;    
    float _sampleTime;

    ADC * _adc;
   
    unsigned long _startSampleTime;

    float _currentWindSpeed;
    float _currentWindDirection;
    
    void startWindSample(float sampleTime);
    float get_current_wind_speed_when_sampling();
};

#endif

