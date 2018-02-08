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

baseline      = cv2.imread('baseline.jpg')
base_histo    = cv2.calcHist([baseline], [0], None, [256], [0,256])

current       = cv2.imread('test.jpg')
current_histo = cv2.calcHist([current], [0], None, [256], [0,256])

histograms = {'baseline': base_histo, 'current': current_histo}

OPENCV_METHODS = (
    ("Correlation", 0),
    ("Chi-Squared", 1),
    ("Intersection", 2),
    ("Hellinger", 3))

 # Use all four methods
results = dict()
for methodName, method in OPENCV_METHODS:
    reverse = False

    if methodName in ("Correlation", "Intersection"):
        reverse = True

    difference = cv2.compareHist(base_histo, current_histo, method)
    results[methodName] = difference


for key in results:
    print(results[key])


