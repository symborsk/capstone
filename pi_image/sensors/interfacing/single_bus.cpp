// The following is an adaptation of tutorial code specific to the DHT11 sensor
// that has been modified to work with (hopefully) any single bus sensor. 
// Here is the link: 
// http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define DELAY	85
#define SENSOR. 7
int *data = (int *) malloc(sizeof(int));
 
void read_single_bus_dat(int bytes)
{
	uint8_t laststate	= HIGH;
	uint8_t counter		= 0;
	uint8_t j		= 0, i;
	float	f; 
 
	for (int i = 0; i < bytes; i++)
	{
		data = realloc(data, i * sizeof(int));
		data[i] = 0;
	}
	

	pinMode(SENSOR, OUTPUT);
	digitalWrite(SENSOR, LOW);
	delay(20);
	digitalWrite(SENSOR, HIGH);
	delayMicroseconds(40);
	pinMode(SENSOR, INPUT);
 
	for (i = 0; i < DELAY; i++ )
	{
		counter = 0;
		while ( digitalRead(SENSOR) == laststate)
		{
			counter++;
			delayMicroseconds( 1 );
			if ( counter == 255 )
			{
				break;
			}
		}
		laststate = digitalRead(SENSOR);
 
		if ( counter == 255 )
			break;
 
		if ( (i >= 4) && (i % 2 == 0) )
		{
			dht11_dat[j / 8] <<= 1;
			if ( counter > 16 )
				dht11_dat[j / 8] |= 1;
			j++;
		}
	}
 
	if ( (j >= 40) &&
	     (dht11_dat[4] == ( (dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF) ) )
	{
		f = dht11_dat[2] * 9. / 5. + 32;
		printf( "Humidity = %d.%d %% Temperature = %d.%d C (%.1f F)\n",
			dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3], f );
	} else 
	{
		printf( "Data not good, skip\n" );
	}
}
 
int main(void)
{
	printf( "Raspberry Pi wiringPi DHT11 Temperature test program\n" );
 
	if ( wiringPiSetup() == -1 )
		exit( 1 );
 
	while ( 1 )
	{
		read_dht11_dat();
		delay( 1000 ); 
	}
 
	return(0);
}