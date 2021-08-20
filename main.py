import numpy as np
import cv2

image = cv2.imread('example_page-0001.jpg')
result = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([155,25,0])
upper = np.array([179,255,255])
mask = cv2.inRange(image, lower, upper)
result = cv2.bitwise_and(result, result, mask=mask)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y),
                    (x + w, y + h),
                    (25, 255, 255), 2)

    cv2.putText(image, "Orange", (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 0))

result = cv2.resize(result, (360, 500))

cv2.imshow('mask', mask)
cv2.imshow('result', result)
cv2.waitKey()
