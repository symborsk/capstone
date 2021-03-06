#############################################################################
# startup.py
#
# By: Joey-Michael Fallone
#
# This script runs the entire sensor sweep process. It starts by launching
# the setup gui and then launches the necessary scripts and programs/drivers
# to properly operate. 
#
#
#
#############################################################################

import os
import os.path
import time

os.system("python ~/capstone/pi_image/gui/Wizard.py")
os.system("sudo sh ~/capstone/pi_image/pi_scripts/makeall.sh")
while not os.path.isfile("/home/thor/.start"):
	pass

print("setup complete")

#print("entering power saving mode")
#os.system("sudo sh ~/capstone/pi_image/pi_scripts/power_saving/power_saving.sh")

if os.path.isfile("/home/thor/.use3G.dat"):
	print("starting up 3G chip")
	os.system("sudo pon fona")
	time.sleep(15)
	os.system("sudo ifmetric ppp0 3000")
# for now run as sudo?
# chmodding, we'll see what happens
# start sdl process
os.system("sudo python ~/capstone/pi_image/image_recognition/take_baseline.py")
os.system("sudo ~/capstone/pi_image/sensors/interfacing/SDL/station &")
# initial run 
os.system("sudo sh ~/capstone/pi_image/sensors/batch_read.sh")

while True:
	file = open("/home/thor/.interval.dat", "r")
	interval = file.readlines()[0]
	interval = interval.strip()
	interval = int(interval)
	file.close()
	# the following is done to preverse energy, but can be changed
	# to constantly look at recheck interval file
	# That would provide faster updates to changed settings but more
	# CPU drain and I/O in operation
	time.sleep(interval)
	os.system("sh ~/capstone/pi_image/sensors/batch_read.sh")
	os.system("sudo pkill -9 station")
	os.system("sudo ~/capstone/pi_image/sensors/interfacing/SDL/station &")
