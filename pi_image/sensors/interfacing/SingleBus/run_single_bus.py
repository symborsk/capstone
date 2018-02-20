'''
	We need to have a list of single bus pins here (populated
	by the setup wizard)
'''
import os

single_bus_sensors = dict()
single_bus_sensors["dht22_1"] = 7

if __name__ == '__main__':
	# https://stackoverflow.com/questions/13045593/using-sudo-with-python-script
	sudoPassword = 's3ns0r' # encrypt this lol

	for sensor, pin in single_bus_sensors.items():
		command = './SingleBus ' + str(pin) + ' > .data/' + sensor + '.dat'
		p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

