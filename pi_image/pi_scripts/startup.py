import os
import time

os.command("python ~/capstone/pi_image/gui/Wizard.py")
# for now run as sudo?
# chmodding, we'll see what happens
# start sdl process
os.command("sudo ~/capstone/pi_image/sensors/interfacing/SDL/station &");
# initial run 
os.command("sh ~/pi_image/sensors/batch_read.sh")

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
	os.command("sh ~/pi_image/sensors/batch_read.sh")
