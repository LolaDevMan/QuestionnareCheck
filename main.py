import numpy as np
import cv2
import csv
import os

<<<<<<< HEAD
path = "C://Users//alwin//Desktop//images"
dir_list = os.listdir(path)
print(dir_list)
for j in dir_list:
    q=1
    questions = ["Qno."]
    options = []
    s = path + "//" + j
    print(s)
    uid = j.split('.')[0]
    print(type(uid))
    options.append(uid)
    print("options",options)
    image = cv2.imread(s)
    coordinates = []
    count = 0
    original = image.copy()
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

    for i in coordinates:
        if(850 <= i[0] < 970): 
            options.append(3)
        elif(970 <= i[0] < 1091):
            options.append(2)
        elif(1091 <= i[0] < 1213):
            options.append(1)
        questions.append(q)
        q+=1
    with open('ans_scan.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(questions)
        writer.writerow(options)
=======
image = cv2.imread('example_page-0001.jpg')
question = 1
coordinates = []
count = 0
original = image.copy()
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
q=1
questions = ["Qno."]
options = ["Person 1"]
for i in coordinates:
    if(850 <= i[0] < 970): 
        options.append(3)
    elif(970 <= i[0] < 1091):
        options.append(2)
    elif(1091 <= i[0] < 1213):
        options.append(1)
    questions.append(q)
    q+=1
with open('ans_scan.csv', 'a', newline='') as file:

c=1
arr=[]
with open('ans_scan.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(questions)
    writer.writerow(options)
>>>>>>> 925a778edc3e35a123fc6c60143616867b750b56
file.close()

image = cv2.resize(image, (800, 1000))

cv2.imshow("Input Image", original)
cv2.waitKey()