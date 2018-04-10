'''
    iot_hub_transfer.py
    By: Brett Wilkinson and Dallin Toth

    Parsing & sensor hub settings capabilities added by Joey-Michael Fallone
    
    This python script generates the JSON objects of our sensor data 
    and transmits them up to the Azure server. 
'''


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

from collections import namedtuple

# File variables
output_path = "/home/thor/capstone/pi_image/sensors/.out/"
output_file = "output.json"

# JSON Object Variables
hub_name = "sensor_hub"
timestamp = int(time.time())

# battery temp
with open ("/home/thor/.bat_temp.dat") as bat_file:
    bat_temp = bat_file.readline().strip("\n")
os.system("rm -rf ~/.bat_temp.dat")

# Number of sensors in the hub
# TODO: Update to be a dynamic value based on config
sensor_count = 1 

# Location variables
# TODO: Update to dynamic location from 3G/GPS board
lat, lon = 53.5273, -113.5295

# IoT Hub Connection Variables
# TODO: Look into somehow providing this dynamically
# original
with open('/home/thor/.connection_string.dat') as data_file:
    connectionString = data_file.readline().strip("\n")

print(connectionString)
 

# connectionString = 'HostName=pcl-dev-bgwilkinson-ioth.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=+3mmzTBcle0MEROiQX6myvrSlCeM7GrUA4xdNeD7NVs='
# shared
#connectionString = 'HostName=pcl-dev-bgwilkinson-ioth.azure-devices.net;SharedAccessKeyName=device;SharedAccessKey=+2js7mRuUIJnGowjujF8X3Mm76NLq5OttGlefC4BxDA='

#connectionString = 'HostName=pcl-dev-bgwilkinson-ioth.azure-devices.net;DeviceId=sensor_hub;SharedAccessKey=6t45Ha2yrNXKs3wE9twIfe4RK6lriH1hlJFwYic78Kk='
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
    print("getting output")
    with open("/home/thor/.interval.dat") as interval_file:
        polling_frequency = interval_file.readline()
        polling_frequency = float(polling_frequency)/60
    # Load all of the JSON objects then truncate the file
    with open("/home/thor/.email.dat", "r") as email_file:
        email = email_file.readline().strip("\n")

    if os.path.isfile("/home/thor/.use3G.dat"):
        use_3g = "true"
    else:
        use_3g = "false"

    sensors = []
    with open(path + output, 'r+') as f:
        # The 0th element is blank since all sensor programs lead with newline
        contents = f.read().split('\n')[1:]
        f.truncate(0)

    # Load all of the JSON objects from the file
    for c in contents:
        print(c)
        sensors += [json.loads(c)]

    # Build the JSON object that will be transmitted
    output = {
                "device_name": hub_name,
                "timestamp": timestamp,
        "polling_frequency": polling_frequency,
        "battery_temp_ro": float(bat_temp),
        "email_address":  email,
        "use_3G": use_3g,
                "location": {
                    "lat": lat,
                    "lon": lon
                },
                "sensors": sensors
            }

    # Return the output in JSON string format
    return json.dumps(output, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

""" Function that takes received JSON data (for sensor hub settings) and 
    takes appropriate action based on them

    Inputs
        message: The JSON string received by the client
    Outputs
        x: The obj created by interpreting the JSON string (message)

    Partially based on:
    https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
"""
def parse_message(message):
    message = message[0]
    x = json.loads(message, 
            object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return x

""" Function that takes received obj and parses out changes to settings

    Inputs
        settings: The object containing new settings
"""
def update_settings(settings):
    print(dir(settings))
    try:
        seconds = int(settings.polling_frequency) * 60
        with open("/home/thor/.interval.dat", "w+") as file:
            file.write(str(seconds))
        email = str(settings.email_address)
        with open("/home/thor/.email.dat") as file:
            file.write(email)
        if settings.use_3G == "true":
            f = open("/home/thor/.use3G.dat")
        else:
            os.system("sudo rm -rf /home/thor/.use3G.dat")
    except:
        print("no polling freq?")

if __name__=='__main__':
    # Initialize the connection
    IoTHubConn = IoTHub(connectionString)
    print(connectionString)


    try:
        # Receive any messages from the IoT Hub
        response = IoTHubConn.receiveC2DMsg(deviceId)
        print(str(response))
        try:
            responseObj =  parse_message(response)
            #sanitize the etag 
            etag = response[2]['ETag']
            etag = etag.replace('"', '').strip()        
            ackRespo = IoTHubConn.ackC2DMsg(deviceId, etag)
            print(str(ackRespo))
            update_settings(responseObj)
        except:
            pass
        # Send data to the IoT Hub
        body = get_output()
        print(body)
        response = IoTHubConn.sendD2CMsg(deviceId, body)
    except OSError as err:
        print('Error: ' + str(err))
