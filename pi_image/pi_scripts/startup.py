import os

# for now run as sudo?
# chmodding, we'll see what happens

while True:
	file = open("/home/thor/.interval", "r")
	interval = file.readlines()[0]
	interval = interval.strip()
	interval = int(interval)
	close(file)
	# the following is done to preverse energy, but can be changed
	# to constantly look at recheck interval file
	# That would provide faster updates to changed settings but more
	# CPU drain and I/O in operation
	time.sleep(interval)
	os.command("sh ~/pi_image/sensors/batch_read.sh")