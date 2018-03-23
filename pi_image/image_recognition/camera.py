'''
	camera.py
	By: Joey-Michael Fallone

	The following script takes a photo with the camera and saves it for 
	future use with the image recognition algorithm
'''


import datetime

from picamera import PiCamera
from time import sleep

import glob
import os

class Camera:
	img_path = r'/home/thor/capstone/pi_image/image_recognition/img/'

	def __init__(self):
		self.camera = PiCamera()

	def take_photo(self, path=None):
		if not path:
			path = (Camera.img_path + "img_" + 
			  str("{:%b_%d_%Y_%H_%M_%S}".format(datetime.datetime.now())) + ".jpg")

		self.camera.start_preview()
		sleep(1)
		self.camera.capture(path)
		self.camera.stop_preview()

	# MIT license: https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder-using-python
	# add to readme
	def get_latest_photo_filename(self):
		list_of_files = glob.glob('/home/thor/capstone/pi_image/image_recognition/img/*.jpg')
		latest_file = max(list_of_files, key=os.path.getctime)
		return latest_file

if __name__ == "__main__":
	camera = Camera()
	camera.take_photo()
	print(camera.get_latest_photo_filename())
