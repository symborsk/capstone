import os
import base64

custom_dir = "/home/thor/capstone/pi_image/sensors/interfacing/Barometer/"

if __name__ == '__main__':
  # Creating the raw sensor data file that will go to the blob in Azure
    command = 'python ' + custom_dir + 'Barometer.py > ' + custom_dir + '/.data/Barometer.dat'
    os.popen((command), 'w')



