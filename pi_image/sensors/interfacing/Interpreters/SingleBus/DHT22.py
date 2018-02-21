import json

# File variables
data_path = "/home/thor/capstone/pi_image/sensors/interfacing/SingleBus/.data/"
data_file = "dht22_1.dat"
output_path = r"/home/thor/capstone/pi_image/sensors/interfacing/SingleBus/.out/"
output_file = r"output.json"

# JSON Output Variable
sensor_name = "DHT22"

# Load the raw bytes
with open(data_path + data_file) as file:
	for line in file:
		pass

# take latest line
read_bytes = line.split(" ")

# from adafruit library
humidity = (int(read_bytes[0]) * 256 + int(read_bytes[1])) / 10.0
temp =     ((int(read_bytes[2]) & 0x7F) * 256 + int(read_bytes[3])) / 10.0

# Build the JSON output object
output = {
			"sensor": sensor_name,
			"data": {
				"humidity":humidity,
				"temperature":temp
			}
		}

# Write the object to a new line of the output
with open(output_path + output_file, 'a+') as file:
	file.write('\n'+json.dumps(output))
