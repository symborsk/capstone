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
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-alsa python-dev libmtdev-dev \
   xclip

echo "Install cpython"
sudo pip3 install -U Cython==0.27.3

echo "Install kiv from github"
sudo pip3 install git+https://github.com/kivy/kivy.git@master

echo "Script finished."