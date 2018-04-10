'''
	DHT22.py
	By: Brett Wilkinson, Dallin Toth & Joey-Michael Fallone

	The following creates the json output obj for DHT22 data
'''

import json

# File variables
data_path = "/home/thor/capstone/pi_image/sensors/interfacing/SingleBus/.data/"
ext_file = "dht22_ext.dat"
bat_file = "dht22_bat.dat"
output_path = r"/home/thor/capstone/pi_image/sensors/.out/"
output_file = r"output.json"

# JSON Output Variable
ext_name  = "DHT22 External"
ext_bytes = ""
# Load the raw bytes
with open(data_path + ext_file) as file:
  for line in file:
    # take latest line
    ext_bytes = line.split(" ")

with open(data_path + bat_file) as file:
   for line in file:
     # take latest line
     bat_bytes = line.split(" ")


# from adafruit library
ext_humidity = (int(ext_bytes[0]) * 256 + int(ext_bytes[1])) / 10.0
ext_temp =     ((int(ext_bytes[2]) & 0x7F) * 256 + int(ext_bytes[3])) / 10.0
bat_humidity = (int(bat_bytes[0]) * 256 + int(bat_bytes[1])) / 10.0
bat_temp =     ((int(bat_bytes[2]) & 0x7F) * 256 + int(bat_bytes[3])) / 10.0

# Build the JSON output object
ext_output = {
			"sensor": ext_name,
			"data": {
				"humidity":ext_humidity,
				"temperature":ext_temp
			}
		}
with open('/home/thor/.bat_temp', 'w+') as bat_file:
	bat_file.write(str(bat_temp))

# bat_output = {
# 			"sensor": bat_name,
# 			"data": {
# 				"humidity":bat_humidity,
# 				"temperature":bat_temp
# 			}
# 		}


# Write the object to a new line of the output
with open(output_path + output_file, 'a+') as file:
	file.write('\n'+json.dumps(ext_output)+'\n')
