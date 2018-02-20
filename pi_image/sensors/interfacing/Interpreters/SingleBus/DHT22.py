with open("../../SingleBus/.data/dht22_1.dat") as file:
	for line in file:
		pass

# take latest line
read_bytes = line.split(" ")

# from adafruit library
humidity = (int(read_bytes[0]) * 256 + int(read_bytes[1])) / 10.0
temp =     ((int(read_bytes[2]) & 0x7F) * 256 + int(read_bytes[3])) / 10.0

print("humidity: " + str(humidity))
print("temp: " + str(temp))