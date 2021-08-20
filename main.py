import numpy as np
import cv2

image = cv2.imread('example_page-0001.jpg')
result = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([155,25,0])
upper = np.array([179,255,255])
mask = cv2.inRange(image, lower, upper)
result = cv2.bitwise_and(result, result, mask=mask)

result = cv2.resize(result, (360, 500))

cv2.imshow('mask', mask)
cv2.imshow('result', result)
cv2.waitKey()
