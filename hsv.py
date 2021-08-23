import cv2
import numpy as np
from numpy.lib.type_check import imag
pixel = (20,60,80) 
image_src = cv2.imread("New/1.jpg")
image_src = cv2.resize(image_src, (800, 900))

def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]
        upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(pixel, lower, upper)
        image_mask = cv2.inRange(image_hsv,lower,upper)
        cv2.imshow("mask",image_mask)
def main():
    import sys
    global image_hsv, pixel
    image=cv2.GaussianBlur(image_src,(93,93),0)
    cv2.imshow("bgr",image_src)
    cv2.namedWindow('hsv')
    cv2.setMouseCallback('hsv', pick_color)
    # now click into the hsv img , and look at values:
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    image_hsv = cv2.resize(image_hsv, (900, 900))
    cv2.imshow("hsv",image_hsv)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
main()