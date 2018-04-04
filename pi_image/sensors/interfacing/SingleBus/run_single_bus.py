'''
  run_single_bus.py 

  By: Joey-Michael Fallone & Dallin Toth

  This script runs the single bus driver in compliance with the overall
  system's batch read methodology
'''
import os
import base64

single_bus_sensors = dict()
single_bus_sensors['dht22_ext'] = 4
single_bus_sensors['dht22_bat'] = 21
custom_dir = "/home/thor/capstone/pi_image/sensors/interfacing/SingleBus/"

if __name__ == '__main__':
  #encryption using base64 solution from https://stackoverflow.com/questions/157938/hiding-a-password-in-a-python-script-insecure-obfuscation-only
  # https://stackoverflow.com/questions/13045593/using-sudo-with-python-script
  sudoPassword = str(base64.b64decode('czNuczBy'))
  # Creating the raw sensor data file that will go to the blob in Azure
  for sensor, pin in single_bus_sensors.items():
    command = custom_dir + 'SingleBus ' + str(pin) + ' > ' + custom_dir + '/.data/' + sensor + '.dat'
    os.popen('sudo -S %s'%(command), 'w').write(sudoPassword)



