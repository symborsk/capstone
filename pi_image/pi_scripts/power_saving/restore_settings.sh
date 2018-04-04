# restore ops

# requires reboot
sudo mv /home/thor/capstone/pi_image/pi_scripts/power_saving/rc.local.bak /etc/rc.local

echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/bind

sudo shutdown -r now