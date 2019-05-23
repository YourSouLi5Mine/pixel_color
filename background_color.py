import argparse
import cv2
import numpy as np
 
ap = argparse.ArgumentParser()
ap.add_argument("-i", required = True, help = "Route to image")
args = vars(ap.parse_args())

image = cv2.imread(args["i"])
image[np.where((image == [255, 255, 255]).all(axis = 2))] = [255, 0, 0]
cv2.imwrite('red.jpg', image)

image = cv2.imread(args["i"])
image[np.where((image == [255, 255, 255]).all(axis = 2))] = [0, 255, 0]
cv2.imwrite('green.jpg', image)

image = cv2.imread(args["i"])
image[np.where((image == [255, 255, 255]).all(axis = 2))] = [0, 0, 255]
cv2.imwrite('blue.jpg', image)

image = cv2.imread(args["i"])
image[np.where((image == [255, 255, 255]).all(axis = 2))] = [0, 0, 0]
cv2.imwrite('black.jpg', image)
