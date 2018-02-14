#############################################################################
# SensorSweep.py
#
# By: Joey-Michael Fallone
#
# This is the script that will run everytime the Sensor Hub is scheduled or
# manually polled to check all sensor values and relay that information 
# to the Azure IoT Hub.
#
# The script currently polls: 
# 	- image recognition
#
# usage: python3 SensorSweep.py [list of object names]
#
# Where object name is the name of the object that implements the "getData" 
# method, and the definition of the object is in the Sensor.py file
#
#############################################################################

import sys
from Sensor import *
from Connection import *

# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
sys.path.insert(0, 'azure_libs/')
from app import *
from telemetry import *

collected_data = dict()


if len(sys.argv) > 1:
	sensor_list = sys.argv
else:
	sensor_list = get_all_sensors()

	for sensor_type in sensor_list:
		if sensor_type == "SensorSweep.py":
			pass
		else:
			collected_data[sensor_type] = sensor_type.getData()

connection_string = get_connection_string()
client = initialize_client(connection_string)
telemetry = Telemetry()
telemetry.send_telemetry_data("thor-SensorHub", EVENT_SUCCESS, collected_data[ImageRec])
# this seems too good to be true... 