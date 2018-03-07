import os
import tensorflow as tf
import pandas_formatting as pf
import numpy as np
import decision_forest as df
import time
import sys
import json

# Lists for the two types of columns
categorical_keys = ['month', 'day', 'hour']
categorical_cols = dict()
numeric_keys = pf.data_cols[2:] + [x + y for x in pf.data_cols[2:] for y in pf.suffixes]
numeric_cols = dict()

# Mapping of boundaries to be used for the categorical data
categorical_boundaries = {'month':[x for x in range(2, 13)], 'day':[x for x in range(2, 32)], 'hour':[x for x in range(0, 23, 4)]}

# Runtime of the program & folder creation
runtime = round(time.time())
os.makedirs('../logs/{0}/train/'.format(runtime))
os.makedirs('../logs/{0}/eval/'.format(runtime))
os.makedirs('../models/{0}/'.format(runtime))


""" Function that encompasses the weather model.

	Attributes
		n_labels: Number of label columns expected
		spring, summer, fall, winter: Lists of months corresponding to those seasons
	"""
class weather_model():
	# Number of label columns
	n_labels = 3

	# Define seasons to split the weather
	spring = [3, 4, 5]
	summer = [6, 7, 8]
	fall = [9, 10, 11]
	winter = [12, 1, 2]

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
			self.log_dir = '../logs/{0}/'.format(runtime)
			self.model_dir = '../models/{0}/'.format(runtime)

			# Build & evaluate the model
			self.offset = offset
			self.forests, eval_input = self.build(weather_data)
			self.MAE = 	self.evaluate(eval_input.values.tolist(), log_output=log_output)

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
		spring, summer, fall, winter = self.split_weather(train)
		
		# Build the forests
		model = dict()
		model['spring'] = df.DecisionForest(spring.values.tolist(), n_labels=weather_model.n_labels)
		model['summer'] = df.DecisionForest(summer.values.tolist(), n_labels=weather_model.n_labels)
		model['fall'] = df.DecisionForest(fall.values.tolist(), n_labels=weather_model.n_labels)
		model['winter'] = df.DecisionForest(winter.values.tolist(), n_labels=weather_model.n_labels)

		# Write the results to the file
		with open('{0}train/{1}h_build.log'.format(self.log_dir, self.offset), 'x+') as file:
			for key in model.keys():
				file.write('Model: {0}\n{1}\n'.format(key, model[key].results_to_str()))

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
		output_str = 'Weather Model {0}h:\nNumber of Forests: {4}\nSize of Evaluation Set: {3} Rows\nMAE:\tWind Speed: {0}\tRelative Humidity: {1}\t Temperature: {2}'.format(self.offset, MAE[0], MAE[1], MAE[2], len(rows), len(self.forests))
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
		# Lambda function to dump attribute-value object dictionaries
		default_save_fn = lambda f: f.__dict__

		# Write to model_dir file
		with open('{0}{1}h_model.json'.format(self.model_dir, self.offset), 'x+') as f:
			f.write(json.dumps(self, default=default_save_fn))

	def load(self, model_file):
		with open(model_file) as f:
			model_dict = json.loads(f.read())

		self.offset = model_dict['offset']
		self.MAE = model_dict['MAE']

		self.log_dir = model_dict['log_dir']
		self.model_dir = model_dict['model_dir']

		self.forests = dict()
		for season, forest in model_dict['forests'].items():
			self.forests[season] = None # TODO: Load DecisionForest object

	""" Function to compute the labels for a row of input features

		Inputs:
			input_row: List of input features
			log: Where the output should be written to

		Outputs:
			expected: List of label values
		"""
	def run(self, input_row, log = print):
		# Get the month to determine which forest to use
		month = int(input_row[1])

		# Move the row down the appropriate forest
		if month in weather_model.spring:
			expected = self.forests['spring'].get_expected(input_row)
		elif month in weather_model.summer:
			expected = self.forests['summer'].get_expected(input_row)
		elif month in weather_model.fall:
			expected = self.forests['fall'].get_expected(input_row)
		elif month in weather_model.winter:
			expected = self.forests['winter'].get_expected(input_row)
		else:
			log('Error: Month not within season range - month = {0}\n'.format(month))
			expected = [None]

		return expected

	""" Function to split input data based on the month value 
	
		Inputs
			data: Pandas dataframe
		Outputs
			4 Pandas dataframes whose union == Input data
		"""
	def split_weather(self, data): 
		spring_data = data.loc[data['month'].isin(weather_model.spring)]
		summer_data = data.loc[data['month'].isin(weather_model.summer)]
		fall_data = data.loc[data['month'].isin(weather_model.fall)]
		winter_data = data.loc[data['month'].isin(weather_model.winter)]

		return spring_data, summer_data, fall_data, winter_data

if __name__=='__main__': 
	# Build dataframes
	data = pf.load_data()

	# Build the models
	model_1h = weather_model(weather_data=data, offset=1, log_output=True)
	model_4h = weather_model(weather_data=data, offset=4, log_output=True)
	model_8h = weather_model(weather_data=data, offset=8, log_output=True)
	model_12h = weather_model(weather_data=data, offset=12, log_output=True)
	model_24h = weather_model(weather_data=data, offset=24, log_output=True)

	# Save the models
	model_1h.save()
	model_4h.save()
	model_8h.save()
	model_12h.save()
	model_24h.save()