import argparse
import cv2
import numpy as np
from statistics import mean

def color_range(pixel):
    lower =  np.array([pixel[0] - 50, 50, 50])
    upper =  np.array([pixel[0] + 50, 255, 255])
    return [lower,upper]

def process(pixel, hsv, image, color):
    spectrum    = color_range(pixel) 
    mask        = cv2.inRange(hsv, spectrum[0], spectrum[1])
    restore     = cv2.bitwise_and(image,image,mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    paint_image(contours, image, color)
    return [restore, mask]

def paint_image(contours, image, color):
    for contour in contours:
        cv2.drawContours(image, contour, -1, color, 2)

ap = argparse.ArgumentParser()
ap.add_argument("-i", required = True, help = "Route to image")
args = vars(ap.parse_args())

image         = cv2.imread(args["i"])
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
hsv           = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

red_pixel = (4, 116.025, 223.89)
red       = process(red_pixel, hsv, image, (0, 255, 0))
cv2.imshow("Red Restored", red[0])
cv2.imshow("Red Mask"    , red[1])

gray_pixel = (105, 21.675, 211.905)
gray       = process(gray_pixel, hsv, image, (255, 0, 0))
cv2.imshow("Gray Restored", gray[0])
cv2.imshow("Gray Mask"    , gray[1])

cv2.imshow("Original", image)
cv2.waitKey(0)
