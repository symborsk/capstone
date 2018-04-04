'''
	Barometer.py
	By: Brett Wilkinson & Dallin Toth

	The following creates the json output obj for barometer data
'''

import json

# File variables
data_path = "/home/thor/capstone/pi_image/sensors/interfacing/Barometer/.data/"
data_file = "Barometer.dat"
output_path = r"/home/thor/capstone/pi_image/sensors/.out/"
output_file = r"output.json"

# JSON Output Variable
sensor_name = "Barometer"
read_bytes = ""
# Load the raw bytes
with open(data_path + data_file) as file:
  for line in file:
    # take latest line
        read_bytes = line.split(" ")




# From the last read line get the pressure
pressure = float(read_bytes[0])

# Build the JSON output object
output = {
			"sensor": sensor_name,
			"data": {
				"pressure":pressure
			}
		}

# Write the object to a new line of the output
with open(output_path + output_file, 'a+') as file:
	file.write('\n'+json.dumps(output))
