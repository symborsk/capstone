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
windchill_formula = lambda row: 13.12 + (0.6215*row['temperature']) - (11.37*(row['wind_speed']**0.16)) \
			+ (0.3965*row['temperature']*(row['wind_speed']**0.16)) if row['temperature']<0  else row['temperature']

# Equation to estimate dewpoint
# Taken from https://www.ajdesigner.com/phphumidity/dewpoint_equation_dewpoint_temperature.php on Feb 7, 2018
dewpoint_formula = lambda row: ((row['relative_humidity'] / 100) ** 0.125) * (112 + (0.9 * row['temperature'])) \
			+ (0.1 * row['temperature']) - 112

# Equation to estimate humidex
# Taken from https://web.archive.org/web/20130627223738/http://climate.weatheroffice.gc.ca/prods_servs/normals_documentation_e.htmlon Feb 7, 2018
humidex_formula = lambda row: 6.11 * float(np.exp(5417.7530 * ((1/273.16)-(1/(row['dew_point'] + 273.16)))))


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
		data['windchill'] = data.apply(windchill_formula, axis=col_axis)
		data['dew_point'] = data.apply(dewpoint_formula, axis=col_axis)
	
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
def split_data(dataframe, split_fraction=0.8, seed=None): 
	# Generate the random seed
	np.random.seed(seed)

	# Split the data into test & training pairs
	train = dataframe.sample(frac=split_fraction, random_state=seed)
	test = dataframe.drop(train.index)

	# Return the datsets
	return train, test