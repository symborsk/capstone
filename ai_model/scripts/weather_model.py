import os
import tensorflow as tf
import pandas_formatting as pf
import numpy as np
import decision_forest as df
import time
import sys
import urllib.request
import urllib.error
import json

# API Key & Default REST request URL for Weather Underground API
api_key = 'ebad910686508a95'
api_url = 'http://api.wunderground.com/api'
default_query = 'hourly/q'
default_location = 'Canada/Edmonton'
response_format = '.json'
response_map = {'wind_speed':'wspd', 'relative_humidity':'humidity', 'temperature': 'temp'}
desired_unit = 'metric'

# Lists for the two types of columns
categorical_keys = ['month', 'day', 'hour']
categorical_cols = dict()
numeric_keys = pf.data_cols[2:] + [x + y for x in pf.data_cols[2:] for y in pf.suffixes]
numeric_cols = dict()

name = round(time.time())


""" Function that encompasses the weather model.

	Attributes
		n_labels: Number of label columns expected
		spring, summer, fall, winter: Lists of months corresponding to those seasons
	"""
class weather_model():
	# Number of label columns
	n_labels = 3

	# The columns that will be forecasted using the model
	forecast_cols = ['wind_speed', 'relative_humidity', 'temperature']
	seasons = ['winter' , 'w_buf', 'sprall', 's_buf', 'summer']

	# Define dictionaries based on correlated weather
	winter = [12, 1, 2]
	winter_buf = [3, 11]
	sprall = [4, 10]
	summer_buf = [5, 9]
	summer = [6, 7, 8]

	""" Model initialization function. Either loads model from JSON object or builds new model based on weather data.

		Inputs
			model_file: JSON object dictionary (loaded from file using json.loads())
			weather_data: List of pandas dataframes where weather_data[0] is the current feature & future label
			offset: Time in hours which weather_data[0] is shifted to get label values
			log_output: Boolean to indicate command line logging vs file output logging
		"""
	def __init__(self, model_file = None, weather_data = None, offset=None, log_output=False):
		if (weather_data!=None) & (offset!=None):
			# Folder to be used to store the models & logs
			self.log_dir = '../logs/{0}/'.format(name)
			self.model_dir = '../models/{0}/'.format(name)

			# Build & evaluate the model
			self.offset = offset
			self.forests, eval_input = self.build(weather_data)
			self.MAE = 	self.evaluate(eval_input.values.tolist(), log_output=log_output)

			# Initialize the default forecast weight
			self.forecast_weight = [0.5, 0.5, 0.5]
			self.run_predictions = dict()
			self.run_totals = 0

		elif model_file!=None:
			self.load(model_file)

		else:
			raise Exception('Insufficient loading information provided:\nmodel_file: {0}\nweather_data: {1}\noffset:{2}'.format(model_file, weather_data, offset))

	""" Function to build a decision forest regression model for weather prediction 

		Inputs
			dataframes: List of pandas dataframes where dataframes[0] is the current feature & future label
			split_fraction: Fraction of dataframes to be used for building vs testing

		Outputs
			model: Dictionary of DecisionForest objects
			test: Subset of initial dataframes to be used for training
		"""	
	def build(self, dataframes, split_fraction=0.8): 
		# Print initialization to command line 
		print('Building {0}h...'.format(self.offset))

		# Prepare the datasets
		weather = pf.build_dataset(dataframes, self.offset)
		train, test = pf.split_data(weather, split_fraction=split_fraction)
		data = self.split_weather(train)
		
		# Initialize the 2D forest dictionary
		model = dict([(x, dict([(y, None) for y in weather_model.forecast_cols])) for x in weather_model.seasons])
		
		# Loop over all forests to build
		for s in weather_model.seasons:
			for c in weather_model.forecast_cols:
				print("Building {0} {1} forest...".format(s, c))
				model[s][c] = df.DecisionForest(rows=pf.select(data[s], c))

		# Write the results to the file
		with open('{0}train/{1}h_build.log'.format(self.log_dir, self.offset), 'x+') as file:
			# Loop again to write all models
			for s in weather_model.seasons:
				for c in weather_model.forecast_cols:
					file.write('Model: {0} {1}\n{2}\n'.format(c, s, model[s][c].results_to_str()))

		return model, test

	""" Function to evaluate the decision frest regression model 
		
		Inputs
			rows: Pandas dataframe to be used for evaluation
			log_output: Boolean where True calls for file output logging

		Outputs
			MAE: List n_labels in length containing mean absolute error for each label
		"""
	def evaluate(self, rows, log_output=False): 
		print('Evaluating {0}h...'.format(self.offset))
		
		# Generate desired log functions
		if (log_output):
			eval_file = open('{0}eval/{1}h_breakdown.log'.format(self.log_dir, self.offset), 'x+')
			breakdown_log = eval_file.write
		else:
			breakdown_log = print
		breakdown_log('Number of labels: {1}\n'.format(self.offset, weather_model.n_labels))

		# Loop over all rows in test set & compute their absolute errors
		AE = []
		for row in rows:
			labels = row[-weather_model.n_labels:]

			expected = self.run(row[:-weather_model.n_labels], log=breakdown_log)

			row_ae = [abs(expected[i] - labels[i]) for i in range(weather_model.n_labels)]

			# Add absolute error to list
			AE += [row_ae]

			# Log results
			breakdown_log('Expected: {0}\tActual: {1}\tAbsolute Error: {2}\n'.format(expected, labels, row_ae))

		# Close the breakdown file if necessary
		if log_output:
			eval_file.close()

	   	# Calculate mean absolute error & log it
		MAE = [np.mean([E[i] for E in AE]) for i in range(weather_model.n_labels)]
		output_str = 'Weather Model {0}h:\nNumber of Forests: {5}\nSize of Evaluation Set: {4} Rows\nMAE:\tWind Speed: {1}\tRelative Humidity: {2}\t Temperature: {3}'.format(self.offset, MAE[0], MAE[1], MAE[2], len(rows), len(self.forests))
		if log_output:
			with open('{0}/eval/{1}h_forest.log'.format(self.log_dir, self.offset), 'x') as file:
				file.write(output_str)
		else:
			print(output_str)

		# Return the mean absolute error for each label
		return MAE

	""" Function to dump the model to the output folder as a JSON object
	
		"""
	def save(self): 
		# Write to model_dir file
		with open('{0}{1}h_model.json'.format(self.model_dir, self.offset), 'x+') as f:
			f.write(json.dumps(self, default=serialize, indent=2))

	""" Function to load the model object from a JSON model file

		Inputs
			model_file: absolute or relative path to a .json file containing the model
		"""
	def load(self, model_file):
		with open(model_file) as f:
			model_dict = json.loads(f.read())

		self.offset = model_dict['offset']
		self.MAE = model_dict['MAE']

		self.log_dir = model_dict['log_dir']
		self.model_dir = model_dict['model_dir']

		# Initialize the default forecast weight
		self.forecast_weight = model_dict['forecast_weight']
		self.run_predictions = model_dict['run_predictions']
		self.run_totals = model_dict['run_totals']

		# Initialize the 2D dictionary & parse all the forests
		self.forests = dict([(x, dict([(y, None) for y in weather_model.forecast_cols])) for x in weather_model.seasons])
		for s in weather_model.seasons:
			for c in weather_model.forecast_cols:
				self.forests[s][c] = DecisionForest(obj_dict=model_dict['forests'][s][c])
		
	""" Function to compute the labels for a row of input features

		UPDATE: Now updated to use the weather underground API

		Inputs:
			input_row: List of input features
			forecast: Boolean indicating whether or not to include forecast
			loc: Weather Underground HTTP request URI - must be JSON format
			log: Where the output should be written to

		Outputs:
			expected: List of label values
		"""
	def run(self, input_row, use_forecast=False, request_url='{0}/{1}/{2}/{3}{4}'.format(api_url, api_key, default_query, default_location, response_format), log=print):

		# Get the month to determine which forest to use
		month = int(input_row[1])

		if month not in range(1, 13):
			log('Error: Month not in proper range\nmonth = {0}\n'.format(month))
			return [None]
		else:
			# Move the row down the appropriate forest
			if month in weather_model.winter:
				expected = [self.forests['winter']['wind_speed'].get_expected(input_row),
							self.forests['winter']['relative_humidity'].get_expected(input_row),
							self.forests['winter']['temperature'].get_expected(input_row)]
			elif month in weather_model.winter_buf:
				expected = [self.forests['w_buf']['wind_speed'].get_expected(input_row),
							self.forests['w_buf']['relative_humidity'].get_expected(input_row),
							self.forests['w_buf']['temperature'].get_expected(input_row)]
			elif month in weather_model.sprall:
				expected = [self.forests['sprall']['wind_speed'].get_expected(input_row),
							self.forests['sprall']['relative_humidity'].get_expected(input_row),
							self.forests['sprall']['temperature'].get_expected(input_row)]
			elif month in weather_model.summer_buf:
				expected = [self.forests['s_buf']['wind_speed'].get_expected(input_row),
							self.forests['s_buf']['relative_humidity'].get_expected(input_row),
							self.forests['s_buf']['temperature'].get_expected(input_row)]
			elif month in weather_model.summer:
				expected = [self.forests['summer']['wind_speed'].get_expected(input_row),
							self.forests['summer']['relative_humidity'].get_expected(input_row),
							self.forests['summer']['temperature'].get_expected(input_row)]


		# If prompted use weighted 
		if (use_forecast):
			# Send the request & parse the response
			with urllib.request.urlopen(request_url) as response:
				parsed_response = json.loads(response.read())

			# Get the hourly forecast for the desired offset
			forecast = parsed_response['hourly_forecast'][self.offset]
			forecast_temp = forecast[response_map['temperature']][desired_unit]
			forecast_humidity = forecast[response_map['relative_humidity']]
			forecast_windspeed = forecast[response_map['wind_speed']][desired_unit]

			# Update the expected array with new forecasts
			expected[0] = (self.weight[0] * forecast_windspeed) + ((1 - self.weight[0]) * expected[0])
			expected[1] = (self.weight[1] * forecast_humidity) + ((1 - self.weight[1]) * expected[1])
			expected[2] = (self.weight[2] * forecast_temp) + ((1 - self.weight[2]) * expected[2])

		return expected

	""" Function to split input data based on the month value 
	
		Inputs
			data: Pandas dataframe
		Outputs
			4 Pandas dataframes whose union == Input data
		"""
	def split_weather(self, data): 
		winter_data = data.loc[data['month'].isin(weather_model.winter)]
		wbuf_data = data.loc[data['month'].isin(weather_model.winter_buf)]
		sprall_data = data.loc[data['month'].isin(weather_model.sprall)]
		sbuf_data = data.loc[data['month'].isin(weather_model.summer_buf)]
		summer_data = data.loc[data['month'].isin(weather_model.summer)]

		return {'winter':winter_data, 'w_buf':wbuf_data, 'sprall':sprall_data, 's_buf':sbuf_data, 'summer':summer_data}

# Function used to serialize the model
def serialize(x):
	try:
		return x.__dict__
	except AttributeError:
		try:
			return x.tolist()
		except AttributeError:
			return x

# Function to generate and save the AI models
def generate():
	# Load the data
	data = pf.load_data()

	# Build the model directories
	os.makedirs('../logs/{0}/train/'.format(name))
	os.makedirs('../logs/{0}/eval/'.format(name))
	os.makedirs('../models/{0}/'.format(name))

	# Generate & save the 5 models
	model_1h = weather_model(weather_data=data, offset=1, log_output=True)
	model_1h.save()
	model_4h = weather_model(weather_data=data, offset=4, log_output=True)
	model_4h.save()
	model_8h = weather_model(weather_data=data, offset=8, log_output=True)
	model_8h.save()
	model_12h = weather_model(weather_data=data, offset=12, log_output=True)
	model_12h.save()
	model_24h = weather_model(weather_data=data, offset=24, log_output=True)
	model_24h.save()

if __name__=='__main__':

	# UNCOMMENT THIS SECTION TO BUILD AND SAVE NEW MODELS
	"""# Build dataframes
				
			
				"""


	# UNCOMMENT THIS SECTION TO LOAD A MODEL
	

	# Continuous loop until model is loaded
	while True:
		# Prompt user for a selection
		print('\nHere are the current models stored:')
		for x in range(1, len(models)+1):
			print('{0}. {1}'.format(x, models[x]))
		# Parse user response
		try:
			sel = int(input('\nPlease make a selection ({0} - {1})\n>>> '.format(1, len(models))))
			# If its outside the choice range 
			if sel < 1 or sel > len(models):

		except ValueError:
			print("Please enter a valid response")