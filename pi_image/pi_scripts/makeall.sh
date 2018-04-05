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

make -C ~/capstone/pi_image/sensors/SDL/
make -C ~/capstone/pi_image/sensors/SingleBus/
make -C ~/capstone/pi_image/sensors/WindVane/