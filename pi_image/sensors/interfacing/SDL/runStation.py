'''
  We need to have a list of single bus pins here (populated
  by the setup wizard)
'''
import os
import base64

custom_dir = "/home/thor/capstone/pi_image/sensors/interfacing/SDL"


if __name__ == '__main__':
  #encryption using base64 solution from https://stackoverflow.com/questions/157938/hiding-a-password-in-a-python-script-insecure-obfuscation-only
  # https://stackoverflow.com/questions/13045593/using-sudo-with-python-script
  sudoPassword = base64.b64decode('czNuczBy')
  # Creating the raw sensor data file that will go to the blob in Azure
  command = custom_dir + '/Station ' + ' > ' + custom_dir + '/.data/station.dat'
  p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
  os.popen("sudo -S %s"%(command), 'w').write(sudoPassword)



