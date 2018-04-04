# AI Weather Model

This is a python weather model. Using a decision forest algorithm, it can predict temperature, wind speed and relative humidity, which can be used to calculate the windchill temperature and the dewpoint. This model has been trained for Edmonton weather data.

## Requirements

 - Python 3.6.4 64-Bit
 - TensorFlow Python Library
 - Pandas Python Library
 - Numpy Python Library

## Folders

 - **models:** Directory holding weather model JSON objects
 - **scripts:** Location of all python scripts
 - **logs:** Storage for model building/evaluation logs
 - **historical_weather_data**: Folder containing historical training/testing data

## Running the Model
If you wish to build new models, simply run the following command from the scripts folder:
`python weather_model.py`
Parameters within  *decision_forest.py* can be altered to change the configuration of the decision forest. 
Currently, there is no method for re-loading the saved JSON objects. 