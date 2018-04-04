import pandas_formatting as pf
import decision_forest as df
import weather_model as wm
import sys

# List of tuples (cmd run flag, menu option string) for corresponding program functions & subconfigurations
options = [('-build', 'Generate a new AI model'), ('-eval', 'Load a pre-existing model to make predictions')]
build_options = [('-name', 'Change the model name'), ('-treeCount', 'Change the number of trees'), ('-batchSize', 'Change the batch size for building trees')]
eval_options = [('file', 'Make predictions from a file'), ('input', 'Input the weather data manually')]
eval_f_options = [('-inplace', 'Add the predictions to the file'), ('-print', 'Display the results in the console')]

# Main menu for the AI model CMI interface
def model_menu(argv):
	# Check for any input flags
	if (len(argv)>1):
		if argv[1]=='-build':
			# TODO: Handle subconfiguration options
			wm.generate()
			
		elif argv[1]=='-eval':
			# TODO: Build 'eval' cmi mode to make predictions for a file and/or array input
			print('Work in progress...')
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
	model_settings = 'Number of Trees: {0}\nBatch Size per Tree: {1}'.format(df.DecisionForest.n_trees, df.DecisionForest.batch_size)
	options_str = '\n'.join(['{0}. {1}'.format(i+1, build_options[i][1]) for i in range(len(build_options))])
	extra_options = '{0}. {1}\n{2}. {3}'.format(len(build_options)+1, 'Build the model', len(build_options)+2, 'Return to main menu')
	while True:
		print('\nModel Generation Menu\n\nDefault Settings:\n{0}\n\n{1}\n{2}'.format(model_settings, options_str, extra_options))

		# Get user input
		sel = menu_input(1, len(build_options)+2)

		# Return to main menu if desired
		if sel==None:
			main_menu()

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
		elif sel==5: # Return to previous menu
			main_menu()

# Function to handle predictions using the model
def eval_menu():
	# Get the user to load a model
	sel_model = get_model()

	# Handle return key or load model
	if sel==None:
		main_menu()
	else:
		# Loop over all model json files
		for f in [x for x in os.listdir('../models/{0}'.format(sel_model)) if x.endswith('h_model.json')]:
			curr_model = json.load(open('../models/{0}/{1}'.format(sel_model, f)))
			

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

# Funciton to update df.DecisionForest.batch_size based on user input
def set_batchSize(): 
	# Get user input
	sel = menu_input(128, 2048, prompt_text='Enter the desired batch size (128 - 2048):')

	# Handle return key
	if sel==None:
		return

	# Update the value
	df.DecisionForest.batch_size = sel

# Run the main menu if program is ran
if __name__=='__main__':
	model_menu(sys.argv)