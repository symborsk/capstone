#!/bin/bash

############################################################################
# opencv_setup.sh
# By: Joey-Michael Fallone
#
# The following is a modified version of the default install process available
# for opencv3 for use with Ubuntu MATE ARM on the Raspberry Pi 3. 
# 
# There does exist a setup for the Pi 3 specifically, but it is designed
# for Raspbian OS and has some configuration differences and python version
# differences that were not desired. 
#
# This script was based on the install notes from:
# from https://www.learnopencv.com/install-opencv3-on-ubuntu/
# combined with the install notes from:
# https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
############################################################################

echo "Setting up opencv on pi"
echo "apt stuff"
sudo apt-get update

# install git
echo "git"
sudo apt-get install git

echo "FORTRAN"
sudo apt-get install gfortran

# dependencies
 echo "dependencies"
sudo apt-get install build-essential checkinstall cmake pkg-config

# Ubuntu 16.04 + raspberry 

# these are likely included in MATE already, but just in case
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
 
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install libxvidcore-dev
sudo apt-get install libgstreamer0.10-dev
sudo apt-get install qt5-default libgtk2.0-dev libtbb-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libfaac-dev libmp3lame-dev libtheora-dev
sudo apt-get install libvorbis-dev libxvidcore-dev
sudo apt-get install libopencore-amrnb-dev libopencore-amrwb-dev
sudo apt-get install x264-dev

# python libraries
echo "python3 install"
sudo apt-get install python3-dev python3-pip

echo "Downloading opencv & libs to home dir"
cd ~
rm -rf opencv*
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip

echo "decompressing"
unzip opencv.zip
unzip opencv_contrib.zip

echo "Installing numpy - This can take around 15 minutes"
pip3 install numpy

# compile
echo "compile and install opencv"
cd opencv-3.1.0
mkdir build
cd build


cmake -D MAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=/usr/local \
		-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules ..

echo "Main Make process (single core - multicore kept failing)"
echo "This can take up to 24 hours"
sudo make

echo "Make install process"
sudo make install

cd ~/.virtualenvs/facecourse-py3/lib/python3.5/site-packages
# The following line needs to be updated with the ocrrect path
ln -s /usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so
