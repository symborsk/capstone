with open("../../SingleBus/.data/dht22_1") as file:
	for line in file:
		pass

# take latest line
read_bytes = line.split(" ")

# from adafruit library
humidity = (read_bytes[0] * 256 + read_bytes[1]) / 10.0
temp =     ((read_bytes[2] & 0x7F) * 256 + data[3]) / 10.0

print("humidity: " + humidity)
print("temp: " + temp)