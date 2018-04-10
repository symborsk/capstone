#############################################################################
# image_rec.py
# By: Joey-Michael Fallone & Brett Wilkinson
#
# Basic Histogram analysis using four different algorithms to judge the 
# similarities of similar images. Sample results can be found in this dir
# under perfect_match.txt
#
# The opencv3 tutorials available at pyimagesearch.com were used in this 
# process
#############################################################################

import cv2
import json
import os
from camera import Camera


# Output file location
output_path = r'/home/thor/capstone/pi_image/sensors/.out/'
output_file = r'output.json'

# Img Paths
img_path = r'/home/thor/capstone/pi_image/image_recognition/img/'

# Variable sent to IoT Hub
sensor_name = 'Camera'

def _get_visibility_rating(base, curr):
    baseline      = cv2.imread(base)
    base_histo    = cv2.calcHist([baseline], [0], None, [256], [0,256])

    current       = cv2.imread(curr)
    current_histo = cv2.calcHist([current], [0], None, [256], [0,256])

    histograms = {'baseline': base_histo, 'current': current_histo}

    OPENCV_METHODS = (
        ("Correlation", 0))

     # Use correlation
    results = dict()
    reverse = True

    difference = cv2.compareHist(base_histo, current_histo, 0)

    return difference

    
def get_current_visibility_rating():
    camera = Camera()
    camera.take_photo()
    return _get_visibility_rating(img_path + "baseline.jpg", camera.get_latest_photo_filename())

if __name__ == '__main__':
	# Get current visibility rating & build JSON object    
	vis = get_current_visibility_rating()
	if vis < 0.6:
		print("low visibility, sending email")
		os.system("sudo python send_email.py")
	output = {
				"sensor": sensor_name,
				"data":{"visibility":vis}
			}

	# Write the output JSON object to the file
	with open(output_path + output_file, 'a+') as f:
		f.write('\n'+json.dumps(output))
