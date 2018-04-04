#############################################################################
# install_kivy.sh
#
# By: Joey-Michael Fallone
#
# The following script installs the dependencies and python module for the 
# kivy GUI framework on the raspberry pi 3 on Ubuntu MATE.
#
#############################################################################

#!/bin/bash
echo "Instally Kivy on Ubuntu MATE for PI"

echo "Dependencies"
sudo apt-get update
sudo apt-get install libsdl2-dev 
sudo apt-get install libsdl2-image-dev 
sudo apt-get install libsdl2-mixer-dev 
sudo apt-get install libsdl2-ttf-dev
sudo apt-get install pkg-config 
sudo apt-get install libgl1-mesa-dev 
sudo apt-get install libgles2-mesa-dev
sudo apt-get install python-setuptools 
sudo apt-get install libgstreamer1.0-dev 
sudo apt-get install git-core
sudo apt-get install gstreamer1.0-plugins-{bad,base,good,ugly}
sudo apt-get install gstreamer1.0-alsa 
sudo apt-get install python-dev 
sudo apt-get install libmtdev-dev
sudo apt-get install xclip

echo "Install cpython"
sudo pip3 install -U Cython==0.27.3

echo "Install kiv from github"
sudo pip3 install git+https://github.com/kivy/kivy.git@master

echo "Script finished."