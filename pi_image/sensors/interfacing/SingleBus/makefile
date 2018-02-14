#############################################################################
# makefile for SingleBus GPIO Sensor Driver
#
# By: Dallin Toth
#
# This makefile will compile or clean the SingleBus C++ object used to 
# read data from a single bus serial sensor over a specified single 
# GPIO pin
############################################################################

CC = g++

CFLAGS = -g -Wall -std=gnu++11 -fno-stack-protector

TARGET = SingleBus

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).cpp -lwiringPi -lwiringPiDev

clean:
	$(RM) $(TARGET)
	
		
