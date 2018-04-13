#############################################################################
# power_saver.sh
#
# By: Joey-Michael Fallone
#
<<<<<<< HEAD
# The following script uses some power saving tricks to put the pi into
# a low power operating mode
#
############################################################################## 
=======
# Sends email with the visibility image if below the threshold
# based on this tutorial: http://naelshiab.com/tutorial-send-email-python/
#
#############################################################################

# power saving tricks
>>>>>>> a95d6ca48eb0f0f83e698865af3b06b311b134ef

# requires reboot
# sudo cp /home/thor/capstone/pi_image/pi_scripts/power_saving/rc.local /etc/rc.local

# Disable HDMI
#/usr/bin/tvservice -o

# Disable LEDs
sudo sh -c 'echo none > /sys/class/leds/led0/trigger'
sudo sh -c 'echo none > /sys/class/leds/led0/trigger'
sudo sh -c 'echo 0 > /sys/class/leds/led0/brightness'
sudo sh -c 'echo 0 > /sys/class/leds/led0/brightness'


# Disable USB and Ethernet
echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind

# sudo shutdown -r now

sleep 20

/usr/bin/tv/service -p
