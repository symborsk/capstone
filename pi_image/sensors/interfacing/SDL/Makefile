#############################################################################
# Makefile for SDL Rain/Wind Sensor
#
# By: Joey-Michael Fallone
#
# Makefile to compile SDL driver (this driver is meant to run continuously)
#
# SIGUSR1 to trigger an output of data
############################################################################

CC = g++

CFLAGS = -g -Wall -std=gnu++11

TARGET = station

all: $(TARGET)

$(TARGET): SDL_Weather_80422.cpp
	$(CC) $(CFLAGS) -o $(TARGET) SDL_Weather_80422.cpp -lwiringPi -lwiringPiDev

clean:
	$(RM) $(TARGET)
	
		
