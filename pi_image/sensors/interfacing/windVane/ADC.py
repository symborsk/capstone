'''
  ADC.py

  By: Joey-Michael Fallone and Dallin Toth

  Uses the existing Adafruit_ADS1x15 library to print out a 
  ADC value read to stdout

  This code is based on examples from the library referenced, 
  for which license information is provided in the legal section.
'''

# constants
GAIN = 1 # 1 is used on adc datasheet
# this value should be changed for 3.3 V operation in the future
# this value is for 4.09v operation

import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
values = adc.read_adc(0, gain=GAIN)
#print('{0:>6}'.format(*values))
print(values)


