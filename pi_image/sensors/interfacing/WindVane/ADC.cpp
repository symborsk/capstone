/*
 * ADC.cpp
 *
 * By: Joey-Michael Fallone and Dallin Toth
 * ADC Wrapper fro python ADC Lib
 *
 * This simple wrapper uses os calls to read ADC values in over I2C 
 * using the existing python lib for this ADC on raspberry pi
 *
 *
*/

#include "ADC.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
// constructor
ADC::ADC () {
  ; // for now no init steps
}
/*
 * ADC::readVoltage()
 *
 * Reads in the voltage value and returns it as a float
 * between 0 and 3.3 V
 *
 *
 *
*/
float ADC::readVoltage() {
  // based on stackoverflow.com/questions/17071702/c-language-read-from-stdout


	int stdout_bk; // backup stdout

	stdout_bk = dup(fileno(stdout));
	int pipefd[2];
	pipe2(pipefd, NON_BLOCKING);

	dup2(pipefd[1], fileno(stdout));
	system("python ADC.py");
	fflush(stdout);
	close(pipefd[1]);

	dup2(stdout_bk, fileno(stdout));

	char buff[50];

	read(pipefd[0], buff, 49);
	return ADC::convertReadingToVoltage(atoi(buff));

}

float ADC::convertReadingToVoltage(int reading) {
  return ((reading*VDD)/MAX_READ);
}
