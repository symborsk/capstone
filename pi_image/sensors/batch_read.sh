#!/bin/bash

# batch_read.sh
# By: Joey-Michael Fallone, Dallin Toth and Brett Wilkinson
# This file does a batch read of all sensors & sends the data to the IoT Hub

# DHT22
python /home/thor/capstone/pi_image/sensors/interfacing/SingleBus/run_single_bus.py
python /home/thor/capstone/pi_image/sensors/interfacing/Interpreters/SingleBus/DHT22.py

# WindVane
python /home/thor/capstone/pi_image/sensors/interfacing/WindVane/runVaneDirection.py
python /home/thor/capstone/pi_image/sensors/interfacing/Interpreters/WindVane/WindVane.py

# Station
python /home/thor/capstone/pi_image/sensors/interfacing/SDL/runStation.py
python /home/thor/capstone/pi_image/sensors/interfacing/Interpreters/SDL/SDL.py

# Barometer
python /home/thor/capstone/pi_image/sensors/interfacing/Barometer/run_barometer.py

# IoT Hub Message
python /home/thor/capstone/pi_image/sensors/iot_hub_transfer.py
