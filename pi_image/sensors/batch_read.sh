#!/bin/bash

# batch_read.sh
# By: Joey-Michael Fallone, Dallin Toth and Brett Wilkinson
# This file does a batch read of all sensors & sends the data to the IoT Hub

# DHT22
echo "DHT22"
python /home/thor/capstone/pi_image/sensors/interfacing/SingleBus/run_single_bus.py
python /home/thor/capstone/pi_image/sensors/interfacing/Interpreters/SingleBus/DHT22.py

# WindVane
echo "Wind Direction"
python /home/thor/capstone/pi_image/sensors/interfacing/WindVane/runVaneDirection.py
python /home/thor/capstone/pi_image/sensors/interfacing/Interpreters/WindVane/WindVane.py

# Station
echo "Wind/Rain... At least 20 second wait!"
python /home/thor/capstone/pi_image/sensors/interfacing/SDL/runStation.py
python /home/thor/capstone/pi_image/sensors/interfacing/Interpreters/SDL/SDL.py

# Barometer
echo "Barometer"
python /home/thor/capstone/pi_image/sensors/interfacing/Barometer/run_barometer.py
python /home/thor/capstone/pi_image/sensors/interfacing/Interpreters/Barometer/Barometer.py

# Visibility
echo "visibility"
python /home/thor/capstone/pi_image/image_recognition/image_rec.py

# IoT Hub Message
python /home/thor/capstone/pi_image/sensors/iot_hub_transfer.py
