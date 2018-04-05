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

make -c ~/capstone/pi_image/sensors/SDL/
make -c ~/capstone/pi_image/SingleBus/
make -c ~/capstone/pi_image/WindVane/