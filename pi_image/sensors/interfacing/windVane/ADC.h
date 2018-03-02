/*
 * ADC.h
 * By: Joey-Michael Fallone
 *
 * This simple wrapper uses os calls to read ADC values in over
 * I2C using the existing python lib for this ADC on raspberry pi
 *
*/

// constants for piping procedure
#define NON_BLOCKING 0
#define BLOCKING     1

// constants for converting readings to voltages
#define VDD      3.3     // operating voltage of the adc
#define MAX_READ 32768.0 // maximum value ADC could return
// please note that MAX_READ is the reading at VDD

class ADC {
  public:
    ADC(void);
    float readVoltage();

  private:
    float  convertReadingToVoltage(int reading);

};
