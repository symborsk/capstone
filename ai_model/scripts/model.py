import pandas_formatting as pf
import decision_forest as df
import weather_model as wm
import time
import sys

# List of tuples (cmd run flag, menu option string) for corresponding program functions & subconfigurations
options = [('-build', 'Generate a new AI model'), ('-eval', 'Load a pre-existing model to make predictions')]
build_options = [('-name', 'Change the model name'), ('-treeCount', 'Change the number of trees'), ('-batchSize', 'Change the batch size for building trees'), ('-stdThreshold', 'Change the maxmium allowed standard deviation for a leaf node'), ('-deltaThreshold', 'Change the minimum required change in standard deviation from parent to child node')]
eval_options = [('file', 'Make predictions from a file'), ('input', 'Input the weather data manually')]
eval_f_options = [('-inplace', 'Add the predictions to the file'), ('-print', 'Display the results in the console')]

# List of tuples defining the min & max ranges for parameters
parameter_range = {
	'build': {'-treeCount': (16, 256), '-batchSize': (128, 2048), '-stdThreshold':(0.5, 5), '-deltaThreshold':(0.05, 1)}
	}

# Default evaluation parameters
model_name = 'default'
data_file = '../historical_weather_data/example.csv'
use_api = False

# Default output parameters
file_write = False
file_name = str(round(time.time()))
output_type = 'json'
output_path = '../test/output/'

# Variable storing currently loaded model for session
loaded_model = None

# Main menu for the AI model CMI interface
def model_menu(argv):
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

""" Function to display the build menu, handle build menu configurations & generate the models 
	"""
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
		if sel==1: # Predict from file
			evaluate(file=True)
		elif sel==2: # Manually input data
			evaluate(manual=True)
		elif sel==3: # Load a model
			load_model()

# Function to handle evaluation
def evaluate(file=None, manual=None):
	# Get input features either manually or by file input
	if file:
		input_features = get_data_file()
	elif manual:
		input_features = get_data_manual()
	else:
		print('Error: Please use either file or manual data input')
		exit()

	# Check for loaded model
	if loaded_model==None:
		load_model()

	# Set output mode
	output = set_output()

	# Get predictions using the model
	expected = []
	for row in input_features:
		expected += [(i, loaded_model[i].run(input_features)) for i in pf.forecast_offsets]

	# Output the expected results
	display_results(expected, output)

# Function to prompt the user to 
def get_data_file():
	# Prompt the user to move their test file into the correct directory
	prompt = 'Please move the desired data file into the \"test_files\" folder now. Press enter to continue...'
	input(prompt)

	# Get a list of all JSON/CSV files in the test_files directory
	files = [f for f in os.listdir('../test_files') if f.endswith('.json') or f.endswith('.csv')]

	# Print the list of test files
	file_str = '\n'.join(['{0}. {1}'.format(i+1, files[i]) for i in range(len(files))])

# Set the output mode for the evaluation run
def set_output():
	prompt = '\nHow should the results be displayed?\n1. Output to a file\n2. Output to the command line'
	print(prompt)
	sel = menu_input(1, 2)

	# Handle return key
	if sel==None
		return None

	# If file output is selected set the boolean & prompt for name
	if sel==1:
		file_write=True

		# Prompt for new name & assign if necessary
		new_name = input('The current file name is \'{0}\'. Input a new file name or press ENTER to continue.\n>> ')
		if new_name!='':
			file_name = new_name
			prompt2 = '\nWhat format should be used?\n1. JSON\n2. CSV'
			sel2 = menu_input(1, 2)
			if sel2==2:
				output_type='csv'

		# Return the relative file path
		return '{0}/{1}.{2}'.format(output_path, file_name, output_type)

	# Return none if CLI output is chosen
	elif sel==2:
		return None

# Display the results either by writing to a file or by printing them
def display_results(expected, output):
	if output != None:
		# Build the CSV string if necessary
		if output_type=='csv':
			# Initialize CSV header
			result_str = ','.join(['{0}h_{1}'.format(x, y) for x in pf.forecast_offsets for y in pf.forecast_cols])

			# Loop over all predicted results & append to csv
			for result in expected:
				result_str += '\n{0}'.format(','.join([x[1] for x in result]))

		# Otherwise create JSON dump
		else:
			# Initialize JSON array
			result_str = '['

			# Loop and create objects for each element
			for result in expected:
				result_str += '\n\t{\n\t\t\"{0}\":{1}'.format(result[0][0], result[0][1])
				for instance in result[1:]:
					result_str += ',\n\t\t\"{0}\":{1}'.format(instance[0], instance[1])

				result_str += '\n\t},'

			# Drop the final last extra comma & close the array
			result_str = result_str[:-1]
			result_str += '\n]'

		# Write the result string to the file
		with open(output, 'x+') as f:
			f.write(result_str)
			
	else:
		# Loop over all input features to display them
		for result in expected:
			result_str = '{0}h: {1}'.format(result[0][0], result[0][1])
			for instance in result[1:]:
				result_str += '\t{0}h: {1}'.format(instance[0], instance[1])

			print(result_str)


# Function to handle loading the model
def load_model():
	# Initialize the loaded model dictionary
	loaded_model = dict([(x, None) for x in pf.forecast_offsets])

	# Variable for checking model files
	model_postfix = 'h_model.json'

	# Lambda functions to get offset & validate offset
	get_offset = lambda x: int(x.split('h')[0])
	validate_offset = lambda x: get_offset(x) in pf.forecast_offsets

	# Get the model name
	model_name = get_model()

	# Handle return key or load model
	if model_name==None:
		return main_menu()
	else:
		# Loop over all model json files
		for f in [x for x in os.listdir('../models/{0}'.format(model_name)) if x.endswith(model_postfix)]:
			# Load the model if it is valid
			if validate_offset(f):
				loaded_model[get_offset(f)] = wm.weather_model(model_file = '../models/{0}/{1}'.format(model_name, f))

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

# Run the main menu if program is ran
if __name__=='__main__':
	model_menu(sys.argv)