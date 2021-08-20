import numpy as np
import cv2
import csv

image = cv2.imread('example_page-0001.jpg')
# image = image[190:450, 10:1290]
coordinates = []
count = 0
result = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([155,25,0])
upper = np.array([179,255,255])
mask = cv2.inRange(image, lower, upper)
result = cv2.bitwise_and(result, result, mask=mask)
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for pic, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if area > 50:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (25, 255, 255), 2)
        centre_x, centre_y = ((x * 2 + w) // 2, (y * 2 + h) // 2)
        cv2.circle(image, (centre_x, centre_y), 1, (0, 250, 0), thickness=1)
        coordinates.append([centre_x, centre_y])
        count += 1

coordinates = sorted(coordinates, key=lambda x:x[1])

print(coordinates)
print("The number of ticks", count)
c=1
arr=[]
with open('ans_scan.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["QNo.", "Option"])
    for i in coordinates:
        if(850 <= i[0] < 970):
            writer.writerow([c,3])
        elif(970 <= i[0] < 1091):
            writer.writerow([c,2])
        elif(1091 <= i[0] < 1213):
            writer.writerow([c,1])
        c+=1

file.close()

image = cv2.resize(image, (800, 1000))

cv2.imshow('image', image)
cv2.waitKey()
