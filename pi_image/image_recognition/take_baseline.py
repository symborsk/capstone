#############################################################################
# take_baseline.py
# By: Joey-Michael Fallone
#
# Uses Camera object to take a photo and then saves it as a baseline jpg
# for use with img rec
#############################################################################

from camera import Camera

import os

img_path = '/home/thor/capstone/pi_image/image_recognition/img/'

camera = Camera()
camera.take_photo()

os.system("mv '" + camera.get_latest_photo_filename + "' " +
			img_path + "baseline.jpg'");
