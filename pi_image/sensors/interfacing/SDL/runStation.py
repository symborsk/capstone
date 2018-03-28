'''
  runVaneDirection.py
  By: Dallin Toth and Joey-Michael Fallone

  The following runs the rain/wind speed process inline with the batch read 
  we have set up for our process
'''
import os
import base64
import time

custom_dir = "/home/thor/capstone/pi_image/sensors/interfacing/SDL"


if __name__ == '__main__':
  #encryption using base64 solution from https://stackoverflow.com/questions/157938/hiding-a-password-in-a-python-script-insecure-obfuscation-only
  # https://stackoverflow.com/questions/13045593/using-sudo-with-python-script
  sudoPassword = str(base64.b64decode('czNuczBy'))
  # Creating the raw sensor data file that will go to the blob in Azure
  delete = "rm -rf " + custom_dir + "/.data/station.dat"
  os.system(delete)
  command = "sudo pkill -SIGUSR1 station"
    
  #p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
  os.popen("sudo -S %s"%(command), 'w').write(sudoPassword)



