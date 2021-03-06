"""
	model.py
	Created by: Brett Wilkinson

	Main program that handles menus to perform tasks like weather model building, benchmarking & prediction.
"""
import pandas_formatting as pf
import decision_forest as df
import pandas as pd
import weather_model as wm
import subprocess
import time
import json
import sys
import os

# List of tuples (cmd run flag, menu option string) for corresponding program functions & subconfigurations
options = [('-build', 'Generate a new AI model'), ('-eval', 'Load a pre-existing model to make predictions')]
build_options = [('-name', 'Change the model name'), ('-treeCount', 'Change the number of trees'), ('-batchSize', 'Change the batch size for building trees'), ('-stdThreshold', 'Change the maxmium allowed standard deviation for a leaf node'), ('-deltaThreshold', 'Change the minimum required change in standard deviation from parent to child node')]
eval_options = [('-file', 'Make predictions from local weather data in a JSON file'), ('-folder', 'Make predictions from a directory of weather data CSVs')]

# List of tuples defining the min & max ranges for parameters
parameter_range = {
	'build': {'-treeCount': (16, 256), '-batchSize': (128, 2048), '-stdThreshold':(0.5, 5), '-deltaThreshold':(0.05, 1)}
	}

# Default run variables
menu_run = True
inplace = False
file_write = False
useFile = None
input_type = 'csv'
json_obj = None
loop = False

# Default evaluation parameters
data_path = '../test_files'
model_name = 'default'
data_dir = 'example'
data_file = 'example.json'

# Default output parameters
output_path = '../test_files'
output_type = 'csv'
file_name = '{0}/{1}.{2}'.format(output_path, str(round(time.time())), output_type)

# Variables for console app
console_cmd = 'AIServerConsoleApp.exe'
pull_flag = '-GetLatestData'
push_flag = '-SendToAzureBlob'

# Variable storing currently loaded model for session
loaded_model = None

# Variable mapping sensor hub json objects to weather model features
sensor_map = {'DHT22 External': {'temperature': 'temperature', 'relative_humidity': 'humidity'}, 'Barometer': {'pressure_station': 'pressure'}, 'WindVane': {'wind_dir_10s': 'direction'}, 'Station': {'wind_speed': 'windSpeed'}}

# Main menu for the AI model CMI interface
def model_menu(argv):
	global menu_run

	# Check for any input flags
	if (len(argv)>1):
		if argv[1]=='-build':
			# Handle additional configuration flags
			if (len(argv)>2):
				build_args(argv[1:])

			# Generate the model
			wm.generate()
			
		elif argv[1]=='-eval':
			# Handle additional configuration flags
			if (len(argv)>2):
				eval_args(argv[1:])

			# Load & run the model
			evaluate()

		elif argv[1]=='-benchmark':
			# Run the benchmark function
			get_benchmark()
	else:
		# Print the menu options & get a response
		print('\nECE 492 AI Weather Model Command Line Interface\n\n' + '\n'.join(['{0}. {1}'.format(x+1, options[x][1]) for x in range(len(options))]))
		sel = menu_input(1, len(options), error_text='Please make a valid selection or press enter to exit')

		# Exit if user pressed return key
		if sel==None:
			exit()

		# Handle the selection
		if options[sel-1][0]=='-build': # Generate new model
			build_menu()
		elif options[sel-1][0]=='-eval': # Use pre-existing model
			eval_menu()

""" Function to handle user input to the interface 
	
	Inputs
		lower_bound: Int indicating the minimum possible value they can select
		upper_bound: Int indicating the maximum possible value they can select
		prompt_text: String to be displayed prompting user for input
		error_text: String to be displayed upon incorrect user input
		return_key: The string to exit/go back

	Outpus
		sel: Int indicating users selection, or None if user pressed return_key
	"""
def menu_input(lower_bound, upper_bound, prompt_text='\nPlease select an option:', error_text='Please make a valid selection or press enter to go back', return_key=''): 
	while True:
		try:
			# Parse the numeric response - do in 2 steps to provide acces to input in except statement
			sel = input('{0}\n>> '.format(prompt_text))
			sel = int(sel)

			# Check the range of the selection
			if sel < lower_bound or sel > upper_bound:
				raise ValueError
			else:
				return sel

		# Handle non-numeric or out-of-range inputs
		except ValueError:
			# Empty string indicates return ket
			if sel==return_key:
				return None
			else:
				print(error_text)

""" Function to display the build menu, handle build menu configurations & generate the models """
def build_menu(): 
	# Display the build menu
	options_str = '\n'.join(['{0}. {1}'.format(i+1, build_options[i][1]) for i in range(len(build_options))])
	extra_options = '{0}. {1}\n{2}. {3}'.format(len(build_options)+1, 'Build the model', len(build_options)+2, 'Return to main menu')
	while True:
		model_settings = 'Number of Trees: {0}\nBatch Size per Tree: {1}'.format(df.DecisionForest.n_trees, df.DecisionForest.batch_size)
		print('\nModel Generation Menu\n\nDefault Settings:\n{0}\n\n{1}\n{2}'.format(model_settings, options_str, extra_options))

		# Get user input
		sel = menu_input(1, len(build_options)+2)

		# Return to main menu if desired
		if sel==None or sel==5:
			return main_menu()

		# Handle menu selections
		if sel==1: # Set model name
			wm.name = input('Enter the desired model name:\n>> ')
			print('The model name has been changed.')
		elif sel==2: # Set the tree count
			set_treeCount()
			print('The tree count has been updated.')
		elif sel==3: # Set the batch size
			set_batchSize()
			print('The batch size has been updated.')
		elif sel==4: # Generate the models
			wm.generate()
			print('The models have been built.')

# Function to handle predictions using the model
def eval_menu():
	# Build the menu options string
	options_str = '\n'.join(['{0}. {1}'.format(i+1, eval_options[i][1]) for i in range(len(eval_options))])
	extra_options = '{0}. Load a model\n{1}. Return to main menu'.format(len(eval_options)+1, len(eval_options)+2)
	
	# Handle evaluation
	while True:
		# Display the menu options
		model_str = 'No currently loaded model' if loaded_model==None else 'Currently loaded model: {0}'.format(model_name)
		eval_str = 'Weather Data Evaluation Menu\n\n{0}\n\n{1}\n{2}'.format(model_str, options_str, extra_options)
		print(eval_str)

		# Get the users input
		sel = menu_input(1, len(eval_options)+2)

		# Handle return key
		if sel==None or sel==len(eval_options)+2:
			return main_menu()

		# Handle other selected options	
		if sel==1: # Predict from JSON file
			evaluate()
		elif sel==2: # Predict from folder of CSV's
			evaluate()
		elif sel==len(eval_options)+1: # Load a model
			load_model()

# Function to handle evaluation
def evaluate():
	global useFile
	global loaded_model
	global loop
	global json_obj

	# Check for loaded model
	if loaded_model==None:
		loaded_model = load_model()

	while True:
		# Run the pull process to get the data
		pull_proc = subprocess.Popen([console_cmd, pull_flag], stdout=subprocess.PIPE)
		out, err = pull_proc.communicate()

		while (b'False' in out):
			print('Sleeping...')
			time.sleep(10)
			pull_proc = subprocess.Popen([console_cmd, pull_flag], stdout=subprocess.PIPE)
			out, err = pull_proc.communicate()


		print('Pull\tOut: {0}\tErr: {1}'.format(out, err))

		# Get input features
		if useFile:
			input_features = get_data_file()
		else:
			input_features = get_data_dir()

		# Set output mode if not inplace
		if menu_run:
			set_output()

		# Get predictions using the model
		expected = []
		for df in input_features:
			for row in df.values.tolist():
				expected += [[(i, loaded_model[i].run(row)) for i in pf.forecast_offsets]]

		# Output the expected results
		display_results(input_features, expected)

		# Run the push process to post the data
		push_proc = subprocess.Popen([console_cmd, push_flag], stdout=subprocess.PIPE)
		out, err = push_proc.communicate()
		print('Push\tOut: {0}\tErr: {1}'.format(out, err))

		# If not looping then exit
		if loop:
			json_obj=None
		else:
			break

# Function to load the input data from CSV files stored in a specified subdirectory of test_files
def get_data_dir():
	global menu_run
	global data_dir

	# Prompt user to move data folder if necessary
	if menu_run:
		prompt = 'Please move the desired data folder into the \"test_files\" folder now. Press enter to continue...'
		input(prompt)

		# Get a list of all folders in the test_files directory
		dirs = [f for f in os.listdir('../test_files') if f.is_dir()]

		# Print the list of test folders & prompt for choice
		file_str = '\n'.join(['{0}. {1}'.format(i+1, dirs[i]) for i in range(len(dirs))])
		print(file_str)
		sel = menu_input(1, len(dirs))

		# Handle return key
		if sel==None:
			return None

		sel_dir = dirs[sel-1]
	else:
		sel_dir = data_dir

	# For CSV files pandas_formatting.load_data can load & format data appropriately
	dir_path = '../test_files/{0}/'.format(sel_dir)
	data_df = list(pf.load_data(path=dir_path))
	dataframe = pf.join_dataframes(data_df, set_index=True)
	return [dataframe]

# Function to load the input data from a single JSON file stored in test_files
def get_data_file():
	global json_obj
	global menu_run
	global data_file

	# Get json from file if not provided
	if json_obj==None:
		json_obj = {}
		# Prompt user to move data file if necessary
		if menu_run:
			prompt = 'Please move the desired data file into the \"test_files\" folder now. Press enter to continue...'
			input(prompt)

			# Get a list of all files in the test_files directory
			files = [f for f in os.listdir('../test_files') if f.endswith('.json')]
			file_str = '\n'.join(['{0}. {1}'.format(i+1, files[i]) for i in range(len(files))])
			print(file_str)
			sel = menu_input(1, len(files))

			# Handle return key
			if sel==None:
				return None

			sel_file = files[sel-1]
		else:
			sel_file=data_file

		# Read the input file
		with open('{0}/{1}'.format(data_path, sel_file), 'r+') as f:
			json_str = f.read().split('\n')
			
		# Add the strings to the json object
		for i in range(len(json_str)):
			json_obj[i] = json.loads(json_str[i])
	
	# Return the parsed version of the selected file
	return parse_data_file(json_obj)
	
# Function to parse the input data file to get the required features
def parse_data_file(parsed_response):
	result = []
	for i in parsed_response:
		curr = {}

		# Get the data & access the required info
		parsed_data = parsed_response[i]['sensors']
		for d in parsed_data:
			if d['sensor'] in sensor_map:
				for r in sensor_map[d['sensor']]:
					curr[r] = d['data'][sensor_map[d['sensor']][r]]

		# Calculate the dew point & relative humidity
		curr['dew_point'] = round(pf.dewpoint_row_formula(curr))
		curr['windchill'] = round(pf.windchill_row_formula(curr))
		curr['wind_dir_10s'] = pf.convert_wind_direction(curr['wind_dir_10s'])

		# Add the current object to the result
		result += [pd.DataFrame(curr, index=[0])]

	# Return the dataframe
	return result
		
# Set the output mode for the evaluation run
def set_output():
	global file_name
	global file_write

	prompt = '\nHow should the results be displayed?\n1. Output to a file\n2. Output to the command line'
	print(prompt)
	sel = menu_input(1, 2)

	# Handle return key
	if sel==None:
		return None

	# If file output is selected set the boolean & prompt for name
	if sel==1:
		file_write=True

		# Prompt for new name & assign if necessary
		new_name = input('The current file name is \'{0}\'. Input a new file name or press ENTER to continue.\n>> '.format(file_name))
		if new_name!='':
			file_name = '{0}/{1}.{2}'.format(output_path, new_name, output_type)

# Display the results either by writing to a file or by printing them
def display_results(input_features, expected):
	global file_write
	global json_obj
	global output_type
	global inplace
	global file_name

	if file_write:
		if json_obj==None:
			# Create the appropriate dataframe to output
			output_df = pf.create_prediction_dataframe(expected, input_features if inplace else None)

			# Output the dataframe appropriately
			if output_type=='csv':
				output_df.to_csv(path_or_buf=file_name)
			else:
				output_df.to_json(path_or_buf=file_name)
		else:
			output_dict = {}
			for i in range(len(expected)):
				# Get the JSON from expected
				curr_dict = {}

				# Loop over all forecasts & add
				for result in expected[i]:
					curr_dict['{0}h'.format(result[0])] = {'wind_speed': result[1][0], 'relative_humidity': result[1][1], 'temperature': result[1][2]}

				# Add prediction to output_dict
				json_obj[i]['Forecast'] = dict(curr_dict)

			# Write the output dict to the output file
			dump_str = '\n'.join([json.dumps(json_obj[i], default=wm.serialize) for i in range(len(json_obj))])

			# Attempt to remove file first
			try:
   				os.remove(file_name)
			except OSError:
				pass

			with open(file_name, 'x+') as f:
				f.write(dump_str)

	else:
		# Loop over all input features to display them in string format
		if json_obj==None:
			for result in expected:
				result_str = '{0}h: {1}'.format(result[0][0], result[0][1])
				for instance in result[1:]:
					result_str += '\t{0}h: {1}'.format(instance[0], instance[1])

				print(result_str)
		# Otherwise build the JSON object and print it
		else:
			output_dict = {}
			for i in range(len(expected)):
				# Get the JSON from expected
				curr_dict = {}

				# Loop over all forecasts & add
				for result in expected[i]:
					curr_dict['{0}h'.format(expected[i][0])] = {'wind_speed': expected[i][1][0], 'relative_humidity': expected[i][1][1], 'temperature': expected[i][1][2]}

				# Add prediction to output_dict
				output_dict[i] = dict(curr_dict)

			# Loop over all entries and print
			for key in output_dict:
				print(json.dumps(output_dict[key], default=wm.serialize))

# Function to handle loading the model
def load_model():
	global model_name
	global loaded_model
	global model_postfix
	global model_file

	# Initialize the loaded model dictionary
	loaded_model = dict([(x, None) for x in pf.forecast_offsets])

	# Variable for checking model files
	model_postfix = 'h_model.json'

	# Lambda functions to get offset & validate offset
	get_offset = lambda x: int(x.split('h')[0])
	validate_offset = lambda x: get_offset(x) in pf.forecast_offsets

	# Get the model name if necessary
	if menu_run:
		model_name = get_model()

		# Handle return key or load model
		if model_name==None:
			return main_menu()

	# Loop over all model json files
	for f in [x for x in os.listdir('../models/{0}'.format(model_name)) if x.endswith(model_postfix)]:
		# Load the model if it is valid
		if validate_offset(f):
			loaded_model[get_offset(f)] = wm.weather_model(model_file = '../models/{0}/{1}'.format(model_name, f))

	return loaded_model

# Function to prompt the user to select a model to load
def get_model():
	# Get all subdirectories (model name instances) from models directory
	models = [d for d in os.listdir('../models') if d.is_dir()]

	# Display the menu string
	model_str = '\n'.join(['{0}. {1}'.format(i+1, models[i]) for i in range(len(models))])
	print('Below are the models currently saved:\n{0}'.format(model_str))

	# Get a model selection
	sel = menu_input(1, len(models))

	# Handle return key
	if sel == None:
		return None

	# Return the chosen model name
	return models[sel-1]

# Function to update df.DecisionForest.n_trees based on user input
def set_treeCount(): 
	# Get the users new input
	sel = menu_input(16, 4096, prompt_text='Enter the desired tree count (16 - 4096):')

	# Handle return key
	if sel==None:
		return

	# Update tree count & return
	df.DecisionForest.n_trees = sel

# Function to update df.DecisionForest.batch_size based on user input
def set_batchSize(): 
	# Get user input
	sel = menu_input(128, 2048, prompt_text='Enter the desired batch size (128 - 2048):')

	# Handle return key
	if sel==None:
		return

	# Update the value
	df.DecisionForest.batch_size = sel

""" Function to handle any additional build arguments passed

	Inputs:
		argv: sys.argv[1:] passed from main_menu()
	"""
def build_args(argv):
	# Loop over all of the args
	while len(argv)>0:
		# Attempt to handle the argument
		try:
			# Pop the 0th element
			curr = argv.pop(0)

			# Procedure for handling argument
			# 1. Get parameter if necessary
			# 2. Validate parameter - raise ValueError if invalid
			# 3. Assign parameter
			if curr=='-treeCount':
				param = int(argv.pop(0))
				if validate_param(param, 'build', curr):
					df.DecisionForest.n_trees = param
			elif curr=='-name':
				param = argv.pop(0)
				wm.name = param
			elif curr=='-batchSize':
				param = int(argv.pop(0))
				if validate_param(param, 'build', curr):
					df.DecisionForest.batch_size = param
			elif curr=='-stdThreshold':
				param = int(argv.pop(0))
				if validate_param(param, 'build', curr):
					df.std_dev_threshold = param
			elif curr=='-deltaThreshold':
				param = int(argv.pop(0))
				if validate_param(param, 'build', curr):
					df.delta_threshold = param

		# Handle any value errors
		except ValueError:
			print('Invalid build argument passed: {0} {1}\nPlease try again with valid parameters.'.format(curr, param))
			exit()

""" Function to handle any additional eval arguments passed 

	Inputs:
		argv: sys.argv[1:] passed from main_menu()
	"""
def eval_args(argv):
	global useFile
	global json_obj
	global data_file
	global file_write
	global file_name
	global output_type
	global output_path
	global model_name
	global data_dir
	global inplace
	global loop

	# Loop over all args to handle them
	while(argv):
		# Pop the argv to handle
		curr = argv.pop(0)

		# Update accordingly
		if curr=='-file':
			param = argv.pop(0)
			if param.endswith('.json'):
				useFile = True
				data_file = param
			else:
				print('Error: Invalid data file provided.')
				exit()
		elif curr=='-folder':
			param = argv.pop(0)
			if os.path.isdir('{0}/{1}'.format(data_path, param)):
				useFile = False
				data_dir = param
			else:
				print('Error: Invalid data folder provided.')
				exit()
		elif curr=='-inplace':
			inplace = True
			file_write = True
		elif curr=='-outputFile':
			param = argv.pop(0)
			if param.endswith('.csv') or param.endswith('.json'):
				file_write = True
				file_name = '{0}/{1}'.format(output_path, param)
				output_type = param.split('.')[-1]
			else:
				print('Error: Invalid output file supplied.')
				exit()
		elif curr=='-model':
			param = argv.pop(0)
			if os.path.isdir('{0}/{1}'.format(data_path, param)):
				model_name = param
			else:
				print('Error: Invalid model name suppplied.')
				exit()
		elif curr=='-json':
			param = argv.pop(0)
			json_obj = json.loads(param)
		elif curr=='-loop':
			loop = True

""" Function to validate program input parameters with the predetermined range. 

	Inputs
		param: Input parameter int to validate
		mode: Which parameter range dictionary to use ('build' or 'eval')
		curr: Current parameter whose range is being checked (i.e. '-treeCount' or '-batchSize')

	Outputs
		boolean where True signifies valid input & False signifies invalid

	Raises ValueError when parameter is outside of the range
	"""
def validate_param(param, mode, curr):
	# Create check booleans
	lower_check = param > parameter_range[mode][curr][0]
	upper_check = param < parameter_range[mode][curr][1]
	
	# Perform range check & return
	if lower_check and upper_check:
		return True
	else:
		raise ValueError

def get_benchmark():
	global loaded_model

	# Load the model
	load_model()

	# Load the test data set
	eval_set = pf.load_data(path = '../test_files/example_folder/')

	# Get the 5 necessary offsets
	MAE = []
	for i in [1, 4, 8, 12, 24]:
		curr_set = list(eval_set)

		curr_set[0] = pf.shift_results(curr_set[0], i)

		df = pf.join_dataframes(curr_set)

		MAE += [loaded_model[i].evaluate(df.values.tolist(), log_output=True)]

	print(MAE)


# Run the main menu if program is ran
if __name__=='__main__':
	menu_run = not (sys.argv[1]=='-build' or sys.argv[1]=='-eval' or sys.argv[1]=='-benchmark')

	model_menu(sys.argv)