# build the sensor executable for testing the data input
CC = g++

CFLAGS = -g -Wall

TARGET = SingleBus

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).cpp -lwiringPi -lwiringPiDev

clean:
	$(RM) $(TARGET)
	
		
		'	
