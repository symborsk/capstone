import datetime

from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(1)
camera.capture('/home/thor/capstone/pi_image/image_recognition/images/img_'+ str("{:%b_%d_%Y-%H:%M:%S}".format(datetime.datetime.now())) + ".jpg")
camera.stop_preview()	
