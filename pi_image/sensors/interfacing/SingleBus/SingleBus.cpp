/* 
 * SingleBus.cpp
 * 
 * By: Dallin Toth and Joey-Michael Fallone
 * 
 * SingleBus C++ Class
 * 
 * This class will interface with any single-line Serial sensor interfaced 
 * over a GPIO pin on the Raspberry Pi 3.
 *
 * This code is a heavy modification of existing library code licensed under
 * the MIT license. A full copy of the MIT license is available in the legal
 * directory in the root of this project. 
 * 
 * That library code was used in compliance with the MIT license. 
 * 
 * The original library code can be found at the following link:
 *
 * https://github.com/adafruit/DHT-sensor-library
 */


#include "SingleBus.h"
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>
#define MIN_INTERVAL 2000


SingleBus::SingleBus(uint8_t pin, uint8_t type, uint8_t count, uint8_t bytes, uint8_t delay) {
  wiringPiSetup();
  data = (uint8_t*) malloc(bytes * sizeof(uint8_t));
  _pin = pin;
  _type = type;
  _bytes = bytes;
  _delay = delay;
  #ifdef __AVR
    _bit = digitalPinToBitMask(pin);
    _port = digitalPinToPort(pin);
  #endif
  _maxcycles = 1000;
  _lastresult = false;

  // but so will the subtraction.
  _lastreadtime = -MIN_INTERVAL;
}

bool SingleBus::printData() {
  if (read(true)) {
    for (int i = 0; i < _bytes; i++) {
      printf("%d ", data[i]);
    }
    printf("\n");
    return true;
  }
  else {
    return false;
  }

}


void SingleBus::sendDH11StartSignal() {
  // Go into high impedence state to let pull-up raise data line level and
  // start the reading process.
  delay(500);
  digitalWrite(_pin, HIGH);
  delay(250);

  // First set data line low for 20 milliseconds.
  pinMode(_pin, OUTPUT);
  delay(500);
  digitalWrite(_pin, LOW);
  delay(20);
}

bool SingleBus::read(bool force) {
  // Check if sensor was read less than two seconds ago and return early
  // to use last reading.
  uint32_t currenttime = millis();
  if (!force && ((currenttime - _lastreadtime) < 2000)) {
    return _lastresult; // return last correct measurement
  }
  _lastreadtime = currenttime;

  // Reset all of received data to zero.
  int i;
  for (i = 0; i < _bytes; i++) {
    data[i] = 0;
  }
  sendDH11StartSignal(); // this needs be made generic later

  pinMode(_pin, INPUT);
  uint32_t cycles[_maxcycles];
  {
    // End the start signal by setting data line high for 40 microseconds.
    // This is DH11 specific... Needs to be more general
    digitalWrite(_pin, HIGH);
    delayMicroseconds(40);

    // Now start reading the data line to get the value from the sensor
    pullUpDnControl(_pin, PUD_UP);
    delayMicroseconds(10);  // Delay a bit to let sensor pull data line low.

                // First expect a low signal for ~delay microseconds followed by a high signal
                // for ~delay microseconds again.
    if (expectPulse(LOW) == 0) {
      _lastresult = false;
      return _lastresult;
    }
    if (expectPulse(HIGH) == 0) {
      _lastresult = false;
      return _lastresult;
    }

    // variable number of bytes in sensor read in
    for (int i = 0; i < _delay; i += 2) {
      cycles[i] = expectPulse(LOW);
      cycles[i + 1] = expectPulse(HIGH);
    }
  }
    // Inspect pulses and determine which ones are 0 (high state cycle count < low
    // state cycle count), or 1 (high state cycle count > low state cycle count).
  for (int i = 0; i<40; ++i) {
    uint32_t lowCycles = cycles[2 * i];
    uint32_t highCycles = cycles[2 * i + 1];
    if ((lowCycles == 0) || (highCycles == 0)) {
      _lastresult = false;
      return _lastresult;
    }
    data[i / 8] <<= 1;
    // Now compare the low and high cycle times to see if the bit is a 0 or 1.
    if (highCycles > lowCycles) {
      // High cycles are greater than 50us low cycle count, must be a 1.
      data[i / 8] |= 1;
    }
    // Else high cycles are less than (or equal to, a weird case) the 50us low
    // cycle count so this must be a zero.  Nothing needs to be changed in the
    // stored data.
  }

  
  return DH11Checksum(data);
}

bool SingleBus::DH11Checksum(uint8_t * data) {
  
  if (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF)) {
    _lastresult = true;

    return _lastresult;
  }
  else {
    _lastresult = false;
    return _lastresult;
  }
}


uint32_t SingleBus::expectPulse(bool level) {
  uint32_t count = 0;

#ifdef __AVR
  uint8_t portState = level ? _bit : 0;
  while ((*portInputRegister(_port) & _bit) == portState) {
    if (count++ >= _maxcycles) {
      return 0; // Exceeded timeout, fail.
    }
  }
#else
  while (digitalRead(_pin) == level) {
    if (count++ >= _maxcycles) {
      return 0; // Exceeded timeout, fail.
    }
 } 

#endif

  return count;
} 

int main(int argc, char ** argv){
  int pin = atoi(argv[1]);
  SingleBus sensor = SingleBus(pin, INPUT, 3, 5, 85);
  while (sensor.printData() == false) {
    sensor.printData();
    delay(2000);
 }
return 0;
}
