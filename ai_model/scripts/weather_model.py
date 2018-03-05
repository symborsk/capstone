import tensorflow as tf
import pandas_formatting as pf
import numpy as np
import decision_forest as df
import time
import sys

# Lists for the two types of columns
categorical_keys = ['month', 'day', 'hour']
categorical_cols = dict()
numeric_keys = pf.data_cols[2:] + [x + y for x in pf.data_cols[2:] for y in pf.suffixes]
numeric_cols = dict()

# Mapping of boundaries to be used for the categorical data
categorical_boundaries = {'month':[x for x in range(2, 13)], 'day':[x for x in range(2, 32)], 'hour':[x for x in range(0, 23, 4)]}

# Runtime of the program
runtime = round(time.time())

# Folder to be used to store the models & logs
log_dir = '../logs/{0}/'.format(runtime);
model_dir = '../models/{0}/'.format(runtime;)

# Lambda function to save the model
default_save_fn = lambda f: f.__dict__

# Define seasons to split the weather
spring = [3, 4, 5]
summer = [6, 7, 8]
fall = [9, 10, 11]
winter = [12, 1, 2]

""" Function to build a decision forest regression model for weather prediction 

	Inputs
		dataframes: List of pandas dataframes where dataframes[0] is the current feature & future label
		offset: Time (in hours) we are attempting to forecast
		n_labels: Number of rightmost columns to be used as labels
		split_fraction: Fraction of dataframes to be used for building vs testing

	Outputs
		model: Dictionary of DecisionForest objects
		test: Subset of initial dataframes to be used for training
	"""	
def build_model(dataframes, offset, n_labels, split_fraction=0.8): 
	# Print initialization to command line 
	print('Building {0}h...'.format(offset))

	# Prepare the datasets
	weather = pf.build_dataset(dataframes, offset)
	train, test = pf.split_data(weather, split_fraction=split_fraction)
	spring, summer, fall, winter = split_weather(train)
	
	# Build the forests
	model = dict()
	model['spring'] = df.DecisionForest(spring.values.tolist(), n_labels=n_labels)
	model['summer'] = df.DecisionForest(summer.values.tolist(), n_labels=n_labels)
	model['fall'] = df.DecisionForest(fall.values.tolist(), n_labels=n_labels)
	model['winter'] = df.DecisionForest(winter.values.tolist(), n_labels=n_labels)

	# Write the results to the file
	with open('{0}train/{1}h_build.log'.format(log_dir, offset), 'x') as file:
		for key in model.keys():
			file.write('Model: {0}\n{1}\n'.format(key, model[key].results_to_str()))

	return model, test

""" Function to evaluate the decision frest regression model 
	
	Inputs
		model: Dictionary of DecisionForest objects
		rows: Pandas dataframe to be used for evaluation
		offset: The forecasted time
		n_labels: Number of rightmost label columns in rows

	Outputs
		MAE: List n_labels in length containing mean absolute error for each label
	"""
def evaluate_model(model, rows, offset, n_labels): 
	# Open log file
	print('Evaluating {0}h...'.format(offset))
	eval_file = open('{0}eval/{1}h_breakdown.log'.format(log_dir, offset), 'x')
	eval_file.write('Evaluating {0}h Model...\nNumber of labels: {1}\n'.format(offset, n_labels))


	# Loop over all rows in test set & compute their absolute errors
	AE = []
	for row in rows:
		labels = row[-n_labels:]
		
		expected = run_model(model, row, n_labels)

		row_ae = [abs(expected[i] - labels[i]) for i in range(n_labels)]

		# Add absolute error to list
		AE += [row_ae]

		# Log results
		eval_file.write('Expected: {0}\tActual: {1}\tAbsolute Error: {2}\n'.format(expected, labels, row_ae))

    # Close the evaluation file
    eval_file.close()

	# Calculate mean absolute error & log it
	MAE = [np.mean([E[i] for E in AE]) for i in range(n_labels)]
	with open('{0}/eval/{1}h_forest.log'.format(log_dir, runtime, offset), 'x') as file:
		file.write('Weather Model {0}h:\nNumber of Forests: {4}\nSize of Evaluation Set: {3} Rows\nMAE:\tWind Speed: {0}\tRelative Humidity: {1}\t Temperature: {2}'.format(offset, MAE[0], MAE[1], MAE[2], len(rows), len(model)))

	# Return the mean absolute error for each label
	return MAE

def run_model(model, input_row, n_labels):
	# Get the month to determine which forest to use
	month = int(row[1])

	# Move the row down the appropriate forest
	if month in spring:
		expected = model['spring'].get_expected(input_row[:-n_labels])
	elif month in summer:
		expected = model['summer'].get_expected(input_row[:-n_labels])
	elif month in fall:
		expected = model['fall'].get_expected(input_row[:-n_labels])
	elif month in winter:
		expected = model['winter'].get_expected(input_row[:-n_labels])
	else
		eval_file.write('Error: Month not within season range - month = {0}\n'.format(month));
		expected = [-1]

	return expected


def save_model(model, offset):
	# Write to model_dir file
	with open('{0}{1}h_model.json'.format(model_dir, offset), 'x+') as f:
		f.write(json.dumps(model, default=default_save_fn))

def split_weather(data):
	spring_data = data.loc[data['month'].isin(spring)]
	summer_data = data.loc[data['month'].isin(summer)]
	fall_data = data.loc[data['month'].isin(fall)]
	winter_data = data.loc[data['month'].isin(winter)]

	return spring_data, summer_data, fall_data, winter_data

if __name__=='__main__': 
	# Build dataframes
	initial_weather_data = pf.load_data()

	# Build & Evaluate 1h Forest
	model_1h, test_1h = build_model(initial_weather_data, 1, 3)
	MAE_1h = evaluate_model(model_1h, test_1h.values.tolist(), 1, 3)
	save_model(model_1h, 1)

	# Build & Evaluate 4h Forest
	model_4h, test_4h = build_model(initial_weather_data, 4, 3)
	MAE_4h = evaluate_model(model_4h, test_4h.values.tolist(), 4, 3)
	save_model(model_4h, 4)

	# Build & Evaluate 8h Forest
	model_8h, test_8h = build_model(initial_weather_data, 8, 3)
	MAE_8h = evaluate_model(model_8h, test_8h.values.tolist(), 8, 3)
	save_model(model_8h, 8)

	# Build & Evaluate 12h forest
	model_12h, test_12h, = build_model(initial_weather_data, 12, 3)
	MAE_12h = evaluate_model(model_12h, test_12h.values.tolist(), 12, 3)
	save_model(model_12h, 12)

	# Build & Evaluate 24h forest
	model_24h, test_24h = build_model(initial_weather_data, 24, 3)
	MAE_24h = evaluate_model(model_24h, test_24h.values.tolist(), 24, 3)
	save_model(model_24h, 24)