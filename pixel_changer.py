from __future__ import print_function
import argparse
import cv2
import numpy as np
from statistics import mean

def getAreas(contours):
    areas = []
    for line_points in contours:
        area = cv2.contourArea(line_points)
        areas.append(area)
    return areas

def drawContours(areas, contours, image):
    for index, area in enumerate(areas, start=0):
        if (area > mean(areas)):
            cnt  = contours[index]
            rect = cv2.minAreaRect(cnt)
            box  = cv2.boxPoints(rect)
            box  = np.int0(box)
            cv2.drawContours(image,[box],0,(0,0,255),2)

ap = argparse.ArgumentParser()
ap.add_argument("-i", required = True, help = "Route to image")
args = vars(ap.parse_args())

image = cv2.imread(args["i"])

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

inverse_red_mask  = cv2.inRange(hsv_image, (0,50,20), (5,255,255))
red_mask          = cv2.inRange(hsv_image, (175,50,20), (180,255,255))
inverse_gray_mask = cv2.inRange(hsv_image, (0,0,0), (155,155,155))
gray_mask         = cv2.inRange(hsv_image, (255,255,255), (100,100,100))

eyes_mask    = cv2.bitwise_or(inverse_red_mask, red_mask)
mouth_mask   = cv2.bitwise_or(inverse_gray_mask, gray_mask)
eyes_croped  = cv2.bitwise_and(image, image, mask=eyes_mask)
mouth_croped = cv2.bitwise_and(image, image, mask=mouth_mask)

eyes_contours, hierarchy  = cv2.findContours(eyes_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
mouth_contours, hierarchy = cv2.findContours(mouth_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

eyes_areas = getAreas(eyes_contours)
mouth_areas = getAreas(mouth_contours)
drawContours(eyes_areas, eyes_contours, image)
drawContours(mouth_areas, mouth_contours, image)
  
cv2.imshow("eyes_mask", eyes_mask)
cv2.imshow("eyes_croped", eyes_croped)
cv2.imshow("mouth_mask", mouth_mask)
cv2.imshow("mouth_croped", mouth_croped)
cv2.imshow("image", image)
cv2.waitKey(0)
