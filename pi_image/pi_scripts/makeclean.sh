#############################################################################
# makeall.sh
#
# By: Joey-Michael Fallone
#
# The following script makes all necessary dependencies for a clean 
# build at startup
#
#############################################################################

#!/bin/bash
make clean -C ~/capstone/pi_image/sensors/interfacing/SDL
make clean -C ~/capstone/pi_image/sensors/interfacing/SingleBus/
make clean -C ~/capstone/pi_image/sensors/interfacing/WindVane/
