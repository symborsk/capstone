# power saving tricks

# requires reboot
sudo mv /home/thor/capstone/pi_image/pi_scripts/power_saving/rc.local /etc/rc.local

# Disable USB and Ethernet
echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind

 sudo shutdown -r now
