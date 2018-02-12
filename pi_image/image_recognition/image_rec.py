#############################################################################
# image_rec.py
# By: Joey-Michael Fallone
#
# Basic Histogram analysis using four different algorithms to judge the 
# similarities of similar images. Sample results can be found in this dir
# under perfect_match.txt
#
# The opencv3 tutorials available at pyimagesearch.com were used in this 
# process
#############################################################################

import cv2
from camera import Camera


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
    return _get_visibility_rating("img/baseline.jpg", camera.get_latest_photo_filename())

if __name__ == '__main__':
    print(get_current_visibility_rating())