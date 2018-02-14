/* 
 * SingleBus.h
 * 
 * By: Dallin Toth and Joey-Michael Fallone
 * 
 * SingleBus C++ Class Header File
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

#include <wiringPi.h>
#include <stdint.h>


// Uncomment to enable printing out nice debug messages.
//#define DHT_DEBUG

// Define where debug output will be printed.
#define DEBUG_PRINTER Serial

// Setup debug printing macros.
#ifdef DHT_DEBUG
#define DEBUG_PRINT(...) { DEBUG_PRINTER.print(__VA_ARGS__); }
#define DEBUG_PRINTLN(...) { DEBUG_PRINTER.println(__VA_ARGS__); }
#else
#define DEBUG_PRINT(...) {}
#define DEBUG_PRINTLN(...) {}
#endif

// Define types of sensors.
#define DHT11 11
#define DHT22 22
#define DHT21 21
#define AM2301 21


class SingleBus {
public:
SingleBus(uint8_t pin, uint8_t type, uint8_t count, uint8_t bytes, uint8_t delay);
void begin(void);
bool printData(void);
void sendDH11StartSignal(void);
bool read(bool force=false);
bool DH11Checksum(uint8_t * data);

private:
uint8_t *data;
uint8_t _pin, _type, _bytes, _delay;
#ifdef __AVR
// Use direct GPIO access on an 8-bit AVR so keep track of the port and bitmask
    // for the digital pin connected to the DHT.  Other platforms will use digitalRead.
    uint8_t _bit, _port;
  #endif
  uint32_t _lastreadtime, _maxcycles;
  bool _lastresult;

  uint32_t expectPulse(bool level);

};
