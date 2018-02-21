#!/bin/bash

# This file does a batch read of all sensors & sends the data to the IoT Hub

# DHT22
python3 ~/capstone/pi_image/sensors/interfacing/SingleBus/run_single_bus.py
python3 ~/capstone/pi_image/sensors/interfacing/Interpreters/SingleBus/DHT22.py

# IoT Hub Message
python3 ~/capstone/pi_image/sensors/iot_hub_transfer.py
