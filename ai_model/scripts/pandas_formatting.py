import pandas as pd
import numpy as np

# # # # # # # # # #
# Data  Variables #
# # # # # # # # # #

# Path to the weather data folder
data_path = '../historical_weather_data/'

# List of weather csv files
weather_files = ['weatherstats_edmonton_hourly.csv', 'weatherstats_barrhead_hourly.csv', \
	'weatherstats_edson_hourly.csv', 'weatherstats_esther_hourly.csv', \
	'weatherstats_laclabiche_hourly.csv', 'weatherstats_lloydminsterab_hourly.csv', \
	'weatherstats_nordegg_hourly.csv', 'weatherstats_reddeer_hourly.csv', \
	'weatherstats_rockymountainhouse_hourly.csv', 'weatherstats_slavelake_hourly.csv', \
	'weatherstats_wainwright_hourly.csv']

# Dataframe columns that are kept as features
data_cols = ['date_time_local', 'unixtime', 'pressure_station', 'wind_dir_10s', \
	'wind_speed', 'relative_humidity', 'dew_point', 'temperature', 'windchill']

# Dataset suffixes for corresponding datasets
suffixes = ['_barrhead', '_edson', '_esther', '_laclabiche', '_lloydminster', '_nordegg', \
 	'_reddeer', '_rockymtnhouse', '_slavelake', '_wainwright']

# The hourly forecasts offered of forecasts used
forecast_offsets = [1, 4, 8, 12, 24]

# The columns that will be forecasted using the model
forecast_cols = ['wind_speed', 'relative_humidity', 'temperature']

# Variables for accessing dataframe rows/columns
row_axis = 0
col_axis = 1

# Indexes used
join_index = data_cols[1]
return_index = data_cols[0]

# # # # # # # # # #
# Other Variables #
# # # # # # # # # #
 
# Seconds in an hour used to shift unixtime
secs_per_hour = 3600

# Equation to calculate windchill
# Taken from https://web.archive.org/web/20130627223738/http://climate.weatheroffice.gc.ca/prods_servs/normals_documentation_e.html on Feb 7, 2018
windchill_row_formula = lambda row: 13.12 + (0.6215*row['temperature']) - (11.37*(row['wind_speed']**0.16)) + (0.3965*row['temperature']*(row['wind_speed']**0.16)) if row['temperature']<0  else row['temperature']
windchill_formula = lambda t, w: 13.12 + (0.6215*t) - (11.37*(w**0.16)) + (0.3965*t*(w**0.16)) if row['temperature']<0  else row['temperature']

# Equation to estimate dewpoint
# Taken from https://www.ajdesigner.com/phphumidity/dewpoint_equation_dewpoint_temperature.php on Feb 7, 2018
dewpoint_row_formula = lambda row: ((row['relative_humidity'] / 100) ** 0.125) * (112 + (0.9 * row['temperature'])) + (0.1 * row['temperature']) - 112

# Equation to estimate humidex
# Taken from https://web.archive.org/web/20130627223738/http://climate.weatheroffice.gc.ca/prods_servs/normals_documentation_e.htmlon Feb 7, 2018
humidex_row_formula = lambda row: 6.11 * float(np.exp(5417.7530 * ((1/273.16)-(1/(row['dew_point'] + 273.16)))))


""" Function used to load data from csvs 

	Inputs
		path: String containing folder path for data
		files: List of strings containing filenames to load

	Outputs
		Corresponding list of pandas dataframes
	"""
def load_data(path=data_path, files=weather_files): 
	# Create an list of dataframes
	weather_data = [pd.read_csv(path + x, header=0, low_memory=False).filter(items=data_cols) for x in files]

	# Additional formatting for all the dataframes
	for data in weather_data:
		# Fill in calculated winchill values
		data['windchill'] = data.apply(windchill_row_formula, axis=col_axis)
		data['dew_point'] = data.apply(dewpoint_row_formula, axis=col_axis)
	
		# Round temperatures & pressures
		data.update(data['temperature'].round(0))
		data.update(data['windchill'].round(0))
		data.update(data['dew_point'].round(0))
		data.update(data['pressure_station'].round(1))

	# Drop rows with blanks in other columns
	weather_data = [x.dropna(axis=row_axis, how='any') for x in weather_data]

	return weather_data

""" Function used to add feature columns from "offset" in the future 

	Inputs
		dataframe: Pandas dataframe which doubles as current inputs and past outputs
		offset: Amount in time to shift the past outputs back

	Outputs
		dataframe: Pandas dataframe with label columns on the right
	"""
def shift_results(dataframe, offset): 
	# Create a duplicate & shift the unixtime column in the copy
	dataframe_copy = dataframe.copy()
	dataframe_copy.update(dataframe_copy[join_index].sub(other = secs_per_hour * offset, axis=row_axis))

	# Set the join index
	dataframe = dataframe.set_index(join_index)
	dataframe_copy = dataframe_copy.set_index(join_index)

	# Keep only the desired future forecast columns
	dataframe_copy = dataframe_copy.filter(items=forecast_cols)

	# Join the dataframes
	dataframe = dataframe.join(dataframe_copy, how='inner', rsuffix= '_' + str(offset) + 'h')

	# Return the dataframe w/ proper index
	return dataframe.reset_index(drop=True).set_index(return_index)

""" Function used to generate a dataset with label columns 
	
	Inputs
		dataframes: List of pandas dataframes, where the 0th element is also the label for "offset" in the past
		offset: Time difference between features & labels for rows in 0th dataframe

	Outputs
		dataframe: Pandas dataframe with label columns as rightmost columns
	"""
def build_dataset(dataframes, offset): 
	# Create the copy dataset
	temp_weather_data = list(dataframes)

	# Join together all the future data in the offset column
	temp_weather_data[0] = shift_results(temp_weather_data[0], offset)

	# Concatenate all the dataframes together
	dataframe = join_dataframes(temp_weather_data)

	return dataframe

""" Function used to concatenate dataframes together & add individual date columns 

	Inputs
		dataframes: list of identical pandas dataframes to be joined

	Outputs
		Singe pandas dataframe
	"""
def join_dataframes(dataframes): 
	# Loop over dataframes[1] & onward, joining them to dataframes[0]
	for i in range(1, len(dataframes)):
		# Set the index to join on
		temp_dataframe = dataframes[i].set_index('date_time_local').drop('unixtime', axis=col_axis)

		# Join the dataframe
		dataframes[0] = temp_dataframe.join(dataframes[0], how='inner', lsuffix=suffixes[i-1])

	# Pop out the index in order to grab the time values
	dataframes[0] = dataframes[0].reset_index(drop=False)

	# Constants for the start/end of date portions
	y_start, y_end = 0, 4
	m_start, m_end = 5, 7
	d_start, d_end = 8, 10
	h_start, h_end = 11, 13

	# Insert year, month, day, hour columns into dataset
	dataframes[0].insert(loc=1, column='year', value=dataframes[0]['date_time_local'].str.slice(y_start,y_end).astype('int'), allow_duplicates=True)
	dataframes[0].insert(loc=2, column='month', value=dataframes[0]['date_time_local'].str.slice(m_start,m_end).astype('int'), allow_duplicates=True)
	dataframes[0].insert(loc=3, column='day', value=dataframes[0]['date_time_local'].str.slice(d_start,d_end).astype('int'), allow_duplicates=True)
	dataframes[0].insert(loc=4, column='hour', value=dataframes[0]['date_time_local'].str.slice(h_start,h_end).astype('int'), allow_duplicates=True)

	# Set the index & return
	return dataframes[0].set_index(return_index)

""" Function used to split the data into training & evaluation sets 

	Inputs
		dataframe: Pandas dataframe to split
		split_fraction: Fraction of data that should go to training
		seed: Seed for the numpy RNG

	Outputs
		train, test: Two mutually exclusive pandas dataframes
	"""
def split_data(dataframe, split_fraction=0.85, seed=None): 
	# Generate the random seed
	np.random.seed(seed)

	# Split the data into test & training pairs
	train = dataframe.sample(frac=split_fraction, random_state=seed)
	test = dataframe.drop(train.index)

	# Return the datsets
	return train, test

""" Function used to return the dataframe & specified label

	Inputs
		dataframe: Pandas dataframe
		label_col: String for the desired label to keep

	Outputs
		result: 2D List[row][column] of input data with selected label
	"""
def select(dataframe, drop_cols):
	# Drop the undesired labels
	filtered_dataframe = dataframe.drop(drop_cols, axis=col_axis)
	# Return the 2D List
	return filtered_dataframe.values.tolist()

""" Function used to create the result dataframe with the predictions

	Inputs
		expected: 2D list of expected results [row][column]
		input_features: Pandas DataFrame that can optionally be appended to

	Outputs
		dataframe: Pandas DataFrame
	"""
def create_prediciton_dataframe(expected, input_features=None):
	# Create the parent dataframe
	df_dict = dict([('{0}_{1}h'.format(x, y), None) for y in forecast_offsets for x in forecast_cols])
	for row in expected:
		for i in range(len(forecast_cols)):
			df_dict['{0}_{1}h'.format(forecast_cols[i], row[0])] = row[1][i]

	if input_features != None:
		return input_features.join(pd.DataFrame(df_dict))
	else:
		return pd.DataFrame(df_dict)


""" Function used to round 8 wind direction approximations to a degree

	Inputs:
		dir_str: string indicating N, NE, E, SE, S, SW, W, NW
	Outputs:
		int ranging between 1 & 36 indicating 10's of degrees
"""
def convert_wind_direction(dir_str):
	if dir_str=='N':
		return 0
	elif dir_str=='NE':
		return 45
	elif dir_str=='E':
		return 90
	elif dir_str=='SE':
		return 135
	elif dir_str=='S':
		return 180
	elif dir_str=='SW':
		return 225
	elif dir_str=='W':
		return 270
	elif dir_str=='NW':
		return 315
	else:
		print('Error: invalid wind direction provided: {0}'.format(dir_str))
		exit()

if __name__=='__main__':
	data = load_data()
	data = build_dataset(data, 1)
	print(data.axes[1])
	print(data[data.axes[1][7]][0])
	print(select(data, drop_cols=['wind_speed_1h', 'relative_humidity_1h'])[0][7])