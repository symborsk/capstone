import sys
import json
import numpy as np
import pandas as pd
import re
import ipaddress
from pathlib import Path

# Import the ai_model files used to load & run model
from ....ai_model.scripts import decision_forest as df 
from ....ai_model.scripts import weather_model as model
from ....ai_model.scripts import pandas_formatting as pf

# Define the array of possible allowed argument inputs for the program
main_args = [ "-datafile", # The only required parameter. A file path to a .json or .csv file must be supplied immediately after
	"-destination", # Optional parameter to pipe the output to either a file path or web url/ip address. If not supplied, results are printed to command line
	"-append", # Optional flag to append the model results to the input data row
	"-verbose" #Optional flag to trigger verbose command line logging
]

# Default variables corresponding to flags
datafile = None
destination = None
append = False
verbose = False

# Regex to match the argument supplied with destination against accepted formats: IP address, web url, JSON/CSV output file
destination_regex = '\A([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|(https:\/\/)?(www\.)?\S*\.\S*|[a-zA-Z0-9 \-\:\\\/\.]*\.(\.json|\.JSON|\.csv|\.CSV))\Z'

""" Main function to run the ai_model. 

	Inputs:
		argv: Array of supplied program arguments, either main_args elements or values corresponding to main_args elements
	"""
def main(argv):
	# Parse the command line arguments arguments
	parse_args(argv)

""" Function to parse the arguments passed when the function is called from the command line 

	Inputs:
		argv: List of passed string command arguments - either elements of main_args or parameters for main_args
		"""
def parse_args(argv):
	# Attempt to parse the datafile argument
	try:
		# Get the index of the datafile argument, then remove it & pop the supplied datafile
		datafile_index = argv.index(main_args[0])
		argv.remove(argv[datafile_index])
		datafile = argv.pop(datafile_index)

		# Check for appropriate datafile filetype & that the file exists
		if !(datafile.endswith('.json') or datafile.endswith('.csv')):
			print("Error: incorrect filetype supplied. Please provide a CSV or JSON file.")
			exit()
		elif (!Path(datafile).is_file()):
			print("Error: supplied datafile not found or does not exist. Please try again.")
			exit()
	# No -datafile argument passed. Print an error message and exit
	except ValueError:
		print("Error: datafile argument not supplied. Please provide a file containing input features.")
		exit()

	# Parse any other supplied arguments
	for i in range(len(argv)):
		curr = argv[i]

		# Check through main_args list
		if curr==main_args[1]:
			# Parse the destination argument supplied
			destination = argv.pop(i+1)
	
			# Double check regex match - exit if necessary
			regex_match = re.search(regex, destination).group(0) == destination
			if !(regex_match):
				print("Error: incorrect destination argument supplied. Please supply a proper ip address, web url or JSON/CSV file path.")
				exit()

		elif curr==main_args[2]:
			append=True
		elif curr==main_args[3]:
			verbose=True


# Run main script if necessary
if __name__=='__main__':
	main(sys.arvg)