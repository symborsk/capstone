/* DHT library
MIT license
written by Adafruit Industries
*/
#ifndef SINGLEBUS_H
#define SINGLEBUS_H

#include "wiringPi.h"


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
   SingleBus(uint8_t pinNum, uint8_t type, uint8_t count=6, uint8_t bytes, uint8_t delay);
   void begin(void);
   void printData(void);
   void sendDH11StartSignal(void);
   void DH11Checksum(void);
   boolean read(bool force=false);

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

class InterruptLock {
  public:
   InterruptLock() {
    noInterrupts();
   }
   ~InterruptLock() {
    interrupts();
   }

};

#endif
