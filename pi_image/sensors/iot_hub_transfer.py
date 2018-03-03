import base64
import hmac
import hashlib
import time
import requests
import urllib
import time
import sys
import json
import os

# File variables
output_path = "/home/thor/capstone/pi_image/sensors/interfacing/SingleBus/.out/"
output_file = "output.json"

# JSON Object Variables
hub_name = "thor"
timestamp = int(time.time())

# Number of sensors in the hub
# TODO: Update to be a dynamic value based on config
sensor_count = 1 

# Location variables
# TODO: Update to dynamic location from 3G/GPS board
lat, lon = 53.5273, -113.5295

# IoT Hub Connection Variables
# TODO: Look into somehow providing this dynamically
connectionString = 'HostName=pcl-dev-bgwilkinson-ioth.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=+3mmzTBcle0MEROiQX6myvrSlCeM7GrUA4xdNeD7NVs='
deviceId = 'sensor_hub'

""" Class taken from https:\\github.com\khilscher\IoTHubPiHackathon\SenseHat_IoTHub_Lab_Key.py on Feb 20, 2018 """
class IoTHub:
    
    API_VERSION = '2016-02-03'
    TOKEN_VALID_SECS = 10
    TOKEN_FORMAT = 'SharedAccessSignature sig=%s&se=%s&skn=%s&sr=%s'
    
    def __init__(self, connectionString=None):
        if connectionString != None:
            iotHost, keyName, keyValue = [sub[sub.index('=') + 1:] for sub in connectionString.split(";")]
            self.iotHost = iotHost
            self.keyName = keyName
            self.keyValue = keyValue

    def _buildExpiryOn(self):
        return '%d' % (time.time() + self.TOKEN_VALID_SECS)
    
    def _buildIoTHubSasToken(self, deviceId):
        resourceUri = '%s/devices/%s' % (self.iotHost, deviceId)
        targetUri = resourceUri.lower()
        expiryTime = self._buildExpiryOn()
        toSign = '%s\n%s' % (targetUri, expiryTime)
        key = base64.b64decode(self.keyValue.encode('utf-8'))

        if sys.version_info[0] < 3:
            signature = urllib.quote(
                base64.b64encode(
                    hmac.HMAC(key, toSign.encode('utf-8'), hashlib.sha256).digest()
                )
            ).replace('/', '%2F')
        else:
            signature = urllib.parse.quote(
                base64.b64encode(
                    hmac.HMAC(key, toSign.encode('utf-8'), hashlib.sha256).digest()
                )
            ).replace('/', '%2F')

        return self.TOKEN_FORMAT % (signature, expiryTime, self.keyName, targetUri)
    
    def registerDevice(self, deviceId):
        sasToken = self._buildIoTHubSasToken(deviceId)
        url = 'https://%s/devices/%s?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        body = '{deviceId: "%s"}' % deviceId
        r = requests.put(url, headers={'Content-Type': 'application/json', 'Authorization': sasToken}, data=body)
        return r.text, r.status_code

    def receiveC2DMsg(self, deviceId):
        sasToken = self._buildIoTHubSasToken(deviceId)
        url = 'https://%s/devices/%s/messages/devicebound?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        r = requests.get(url, headers={'Authorization': sasToken})
        return r.text, r.status_code, r.headers

    def ackC2DMsg(self, deviceId, eTag):
        sasToken = self._buildIoTHubSasToken(deviceId)
        url = 'https://%s/devices/%s/messages/devicebound/%s?api-version=%s' % (self.iotHost, deviceId, eTag, self.API_VERSION)
        r = requests.delete(url, headers={'Authorization': sasToken})
        return r.text, r.status_code, r.headers

    def sendD2CMsg(self, deviceId, message):
        sasToken = self._buildIoTHubSasToken(deviceId)
        url = 'https://%s/devices/%s/messages/events?api-version=%s' % (self.iotHost, deviceId, self.API_VERSION)
        r = requests.post(url, headers={'Authorization': sasToken}, data=message)
        return r.text, r.status_code



""" Function that loads JSON output files & returns a single JSON string for the hub

	Inputs
		path: Folder path where output JSON files are stored
		files: List of JSON filenames to be loaded
	Outputs
		JSON string for the sensor hub message
	"""
def get_output(path=output_path, output=output_file, count=sensor_count):
	# Load all of the JSON objects then truncate the file
	sensors = []
	with open(path + output, 'r+') as f:
		# The 0th element is blank since all sensor programs lead with newline
		contents = f.read().split('\n')[1:]
		f.truncate(0)

	# Load all of the JSON objects from the file
	for c in contents:
		sensors += [json.loads(c)]

	# Build the JSON object that will be transmitted
	output = {
				"device_name": hub_name,
				"timestamp": timestamp,
				"location": {
					"lat": lat,
					"lon": lon
				},
				"sensors": sensors
			}

	# Return the output in JSON string format
	return json.dumps(output, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

if __name__=='__main__':
	# Initialize the connection
	IoTHubConn = IoTHub(connectionString)

	try:
		# Receive any messages from the IoT Hub
		response = IoTHubConn.receiveC2DMsg(deviceId)

		# TODO: Handle messages from IoT Hub

		# Send data to the IoT Hub
		body = get_output()
		response = IoTHubConn.sendD2CMsg(deviceId, body)
	except OSError as err:
		print('Error: ' + str(err))