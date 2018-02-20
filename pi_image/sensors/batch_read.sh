#!/bin/bash

# This file does a batch read of all sensors

# DHT22
python3 ~/capstone/pi_image/sensors/interfacing/SingleBus/run_single_bus.py
python3 ~/capstone/pi_image/sensors/interfacing/Interpreters/SingleBus/DHT22.py