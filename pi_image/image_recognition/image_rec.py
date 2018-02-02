# https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
# above needs to be cited. 

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

#    fig = plt.figure("Baseline")
#    ax = fig.add_subplot(1, 1, 1)
#    ax.imshow(baseline)
#
#    fig = plt.figure("Results: %s" % (methodName))
#    fig.suptitle(methodName, fontsize=20)

for key in results:
    print(results[key])


