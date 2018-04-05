#############################################################################
# makefile for WindVane Sensor Driver
#
# By: Joey-Michael Fallone
#
# This makefile will compile or clean the WindVane C++ binary used to 
# read data from the wind vane
############################################################################

CC = g++

CFLAGS = -g -Wall -std=gnu++11

TARGET = WindVane

all: $(TARGET)

$(TARGET): $(TARGET).cpp $(TARGET).h
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).cpp

clean:
	$(RM) $(TARGET)
