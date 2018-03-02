'''
  run_adc.py
  By: Joey-Michael Fallone

  Quick script to populate .data dirs for adc
'''

import os
import datetime

os.system("python ADC.py > '.data/" + str(datetime.datetime.now()) + ".dat'")
