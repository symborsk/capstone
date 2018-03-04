'''
	SDL.py
	By: Brett Wilkinson & Dallin Toth

	The following creates the json output obj for SDL data
'''

import json

# File variables
data_path = "/home/thor/capstone/pi_image/sensors/interfacing/SDL/.data/"
data_file = "station.dat"
output_path = r"/home/thor/capstone/pi_image/sensors/.out/"
output_file = r"output.json"

# JSON Output Variable
sensor_name = "Station"
read_bytes = ""
# Load the raw bytes
with open(data_path + data_file) as file:
  for line in file:
    # take latest line
        read_bytes = line.split(" ")



# From the last read line get the rain and wind speed
rain = read_bytes[3]
windSpeed = read_bytes[1]
gust = read_bytes[5]

# Build the JSON output object
output = {
			"sensor": sensor_name,
			"data": {
				"rain":rain,
                		"windSpeed":windSpeed,
				"gust":gust
			}
		}

# Write the object to a new line of the output
with open(output_path + output_file, 'a+') as file:
	file.write('\n'+json.dumps(output))
