#############################################################################
# Sensor.py
#
# By: Joey-Michael Fallone
#
# Here are the Sensor objects that will be used for SensorSweep to get data 
# from whatever sensors currently exist. The goal here is to make it easy 
# to add new sensors in the future, so there are a couple of requirements
# for all sensors:
#
# 1. The sensor must inherit from Sensor class and implement the abstract
#    method "get_data(self)"
# 2. get_data(self) should return the desired sensor reading
# 3. The name of the object should be appended to the list in the 
#    get_all_sensors() function.
#
#############################################################################

# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
import sys
sys.path.insert(0, '../image_recognition/')

from image_rec import *

class Sensor():
	@abstractmethod
	def get_data(self):
		pass

class ImageRec(Sensor):
	def get_data(self):
		return get_current_visibility_rating()

def get_all_sensors():
	sensors = list()
	sensors.append("ImageRec")