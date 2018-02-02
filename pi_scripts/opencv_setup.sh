# from https://www.learnopencv.com/install-opencv3-on-ubuntu/

echo "Setting up opencv on pi"
echo "apt stuff"
sudo apt-get update
sudo apt-get remove x264 libx264-dev

# dependencies
 echo "dependencies"
sudo apt-get install build-essential checkinstall cmake pkg-config yasm
sudo apt-get install git gfortran
sudo apt-get install libjpeg8-dev libjasper-dev libpng12-dev

# Ubuntu 16.04
sudo apt-get install libtiff5-dev
 
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev
sudo apt-get install libxine2-dev libv4l-dev
sudo apt-get install libgstreamer0.10-dev libgstreamer-plugins-base0.10-videv
sudo apt-get install qt5-default libgtk2.0-dev libtbb-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libfaac-dev libmp3lame-dev libtheora-dev
sudo apt-get install libvorbis-dev libxvidcore-dev
sudo apt-get install libopencore-amrnb-dev libopencore-amrwb-dev
sudo apt-get install x264 v4l-utils
 
# Optional dependencies
echo "optional dependencies"
sudo apt-get install libprotobuf-dev protobuf-compiler
sudo apt-get install libgoogle-glog-dev libgflags-dev
sudo apt-get install libgphoto2-dev libeigen3-dev libhdf5-dev doxygen

# python libraries
echo "python libraries"
sudo apt-get install python3-dev python3-pip
sudo -H pip3 install -U pip numpy

# Install virtual environment (python3 only)
echo "Installing virtual env on python3"
sudo apt-get install virtualenvwrapper
sudo pip3 install virtualenv virtualenvwrapper
echo "# Virtual Environment Wrapper"  >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

############ For Python 3 ############
# create virtual environment
mkvirtualenv opencv-py3 -p python3
workon opencv-py3
  
# now install python libraries within this virtual environment
pip3 install numpy scipy matplotlib scikit-image scikit-learn ipython
  
# quit virtual environment
deactivate
######################################

# download opencv
echo "downloading opencv"
git clone https://github.com/opencv/opencv.git
cd opencv 
git checkout 3.3.1 
cd ..

git clone https://github.com/opencv/opencv_contrib.git
cd opencv_contrib
git checkout 3.3.1
cd ..

# compile
echo "compile and install opencv"
cd opencv
mkdir build
cd build


cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_EXAMPLES=ON ..

# substitute 4 by output of nproc
make -j4
sudo make install
sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig

cd ~/.virtualenvs/facecourse-py3/lib/python3.5/site-packages
ln -s /usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so
