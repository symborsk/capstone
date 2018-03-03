#!/bin/bash

# This file does a batch read of all sensors & sends the data to the IoT Hub

# DHT22
python3 ~/capstone/pi_image/sensors/interfacing/SingleBus/run_single_bus.py
python3 ~/capstone/pi_image/sensors/interfacing/Interpreters/SingleBus/DHT22.py

# WindVane

python3 ~capstone/pi_image/sensors/interfacing/WindVane/runVaneDirection.py
python3 ~capstone/pi_image/sensors/interfacing/Interpreters/WindVane/WindVane.py

# Station

python3 ~/capstone/pi_image/sensors/interfacing/SDL/runStation.py
python3 ~/capstone/pi_image/sensors/interfacing/Interpreters/SDL/SDL.py

# IoT Hub Message
python3 ~/capstone/pi_image/sensors/iot_hub_transfer.py
