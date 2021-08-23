import numpy as np
import cv2
from collections import deque


##TRackbar 1.py
# default called trackbar function ,function gets executed everytime trackbar value changes

def setValues(x):
    print("")
    # return


cv2.namedWindow("Color detectors")
# First argument is the trackbar name, second one is the window name
# Fifth one is the callback function # 3rd Argument is  Default value,4rth Value is maximum limit
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255, setValues)
cv2.resizeWindow('Color detectors', 300, 30)

'''  
    Deque initialization

 '''

bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# The kernel to be used for dilation purpose ,just to clear small impurities
# If your WebCAM is clear then no need of dilation
kernel = np.ones((5, 5), np.uint8)
# BLue         Green             Red       Yellow      BGR represenation
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

''' PAINTWINDOW creation '''
# Here is code for Canvas setup
paintWindow = np.zeros((471, 636, 3)) + 255  # adding 255 so that background is white
paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)  # Clear all
paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275, 1), (370, 65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), colors[3], -1)

# putting text in our Color rectangle boxes
#                                  Co-ordinates      Font type       Font scale  #BGR #Thickness line type
cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

frame = cv2.imread("New/1.jpg")  # primarycamera that's why  0 is used
frame = cv2.flip(frame, 1)  # to flip it again
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # just to convert from BGR to HSV colorspace

''' TRackbars part2'''
# getting HSV values both upper and lower from trackbar
u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")

l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
# We'll take  HSV the values and convert it to numpy array ,would be required to create mask
Upper_hsv = np.array([u_hue, u_saturation, u_value])
Lower_hsv = np.array([l_hue, l_saturation, l_value])

''' Live_frame.py '''
# Adding the colour buttons to the live frame for colour access
frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)  # clear all button
frame = cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
frame = cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
frame = cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
frame = cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
#                                 #co-ordinates          Font type               Font scale       #BGR
cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

'''mask.py'''
# Identifying the pointer by making its mask
# removing impurities in it,if impurities in mask ring then circle/contour will lag
Mask = cv2.inRange(frame, Lower_hsv, Upper_hsv)  # Create  A mask of these HSV ranges
Mask = cv2.erode(Mask, kernel, iterations=1)
Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
Mask = cv2.dilate(Mask, kernel, iterations=1)
# res = cv2.bitwise_and(frame,frame, mask= Mask)

'''contours.py'''

# Find contours for the pointer after identifying it
cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(frame, cnts, -1, (0, 255, 0), 3)  # in docmentations
cv2.imshow("frame", frame)
center = None

'''main algorithm.py'''

# Ifthe contours are formed
if len(cnts) > 0:
    # sorting the contours to find biggest
    cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    # Get the radius of the enclosing circle around the found contour
    ((x, y), radius) = cv2.minEnclosingCircle(cnt)
    # Draw the circle around the contour
    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    # Calculating the center of the detected contour
    M = cv2.moments(cnt)
    # x cordinates #y coordinates
    center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

    # Now checking if the user wants to click on any button above the screen
    if center[1] <= 65:  # if y cordinate location center is
        if 40 <= center[0] <= 140:  # Clear Button
            bpoints = [deque(maxlen=512)]
            gpoints = [deque(maxlen=512)]
            rpoints = [deque(maxlen=512)]
            ypoints = [deque(maxlen=512)]

            blue_index = 0
            green_index = 0
            red_index = 0
            yellow_index = 0

            paintWindow[67:, :, :] = 255  # white background is set again
        elif 160 <= center[0] <= 255:
            colorIndex = 0  # setting ColorIndex to Blue
        elif 275 <= center[0] <= 370:
            colorIndex = 1  # setting ColorIndex to Green
        elif 390 <= center[0] <= 485:
            colorIndex = 2  # setting ColorIndex to Red
        elif 505 <= center[0] <= 600:
            colorIndex = 3  # setting ColorIndex to Yellow
    else:
        if colorIndex == 0:
            bpoints[blue_index].appendleft(center)  # appending center co-ordinates
        elif colorIndex == 1:
            gpoints[green_index].appendleft(center)
        elif colorIndex == 2:
            rpoints[red_index].appendleft(center)
        elif colorIndex == 3:
            ypoints[yellow_index].appendleft(center)
# Append the next deques when nothing is detected to avoid messing up
else:  # doesn't mess with indexes and line creation
    bpoints.append(deque(maxlen=512))
    blue_index += 1
    gpoints.append(deque(maxlen=512))
    green_index += 1
    rpoints.append(deque(maxlen=512))
    red_index += 1
    ypoints.append(deque(maxlen=512))
    yellow_index += 1

# Draw lines of all the colors on the canvas and frame
points = [bpoints, gpoints, rpoints, ypoints]
for i in range(len(points)):
    for j in range(len(points[i])):  # points in deque
        for k in range(1, len(points[i][j])):  # coordinates in those deque
            if points[i][j][k - 1] is None or points[i][j][k] is None:
                continue  # starting coordinates #ending coordinates #color #thickness
            cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i],
                        2)  # painting line in both Paint window and tracking window
            cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

# Show all the windows
frame = cv2.resize(frame, (900, 900))
Mask = cv2.resize(Mask, (800, 800))
cv2.imshow("Tracking", frame)
cv2.imshow("Paint", paintWindow)
cv2.imshow("mask", Mask)
cv2.waitKey(0)
cv2.destroyAllWindows()


