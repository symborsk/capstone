#############################################################################
# cleanup.py
#
# By: Joey-Michael Fallone
#
# This script kills running processes and cleans up files to re-prepare
# the system to run "setup"
#
#############################################################################


import os

os.system("sudo sh /home/thor/capstone/pi_image/pi_scripts/makeclean.sh")
os.system("sudo pkill -9 station")
os.system("sudo rm -rf ~/.start")
os.system("sudo rm -rf ~/.connection_string.dat")
os.system("sudo rm -rf ~/.interval.dat")
os.system("sudo rm -rf ~/.use3G.dat")
os.system("sudo rm -rf ~/.email.dat")
os.system("sudo rm -rf ~/.bat_temp.dat")
