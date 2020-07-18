from processing_string import *
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

path = '../dataFiles/origImage/perfect3.jpg'
img = readImage(path)
imgMod = imgModify(img, 'open')
contour = getCont(imgMod)
lines = getString(img, contour)
global_sred = 0
image = []
for line in lines:
    y,x = line.shape
    count = 0
    img = line
    line = imgModify(line,"edges")

    kernel_close = np.ones((10,5),np.uint8)
    kernel_open = np.ones((3,3),np.uint8)

    line = cv.morphologyEx(line,cv.MORPH_CLOSE,kernel_close,iterations=2)
    line = cv.morphologyEx(line,cv.MORPH_OPEN,kernel_open,iterations=2)

    contours, hierarchy = cv.findContours( line.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    symbols = []
    sredX = 0
    for i in range(2):
        for cont in contours:
            rect = cv.minAreaRect(cont)
            box = cv.boxPoints(rect)
            x0,y0,x1,y1 = cv.boundingRect(box)
            if i == 0:
                sredX += x1/len(contours)
            else:
                if sredX < x1:
                    symbols.append(x1)
                    count += 1



global_sred = 0
for s in symbols:
    global_sred += s / len(symbols)
print("sred ",global_sred)
sq = 0
for s in symbols:
    sq += (s**2) / len(symbols)
print("sq ", sq**0.5)
sq = int(sq**0.5)
lines_new =[]
for line in lines:
    sym = []
    y,x = line.shape
    img = line.copy()
    line = imgModify(line,"edges")

    kernel_close = np.ones((10,5),np.uint8)
    kernel_open = np.ones((3,3),np.uint8)

    line = cv.morphologyEx(line,cv.MORPH_CLOSE,kernel_close,iterations=2)
    line = cv.morphologyEx(line,cv.MORPH_OPEN,kernel_open,iterations=2)

    contours, hierarchy = cv.findContours( line.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    symbols = []
    sredX = 0

    for cont in contours:
        rect = cv.minAreaRect(cont)
        box = cv.boxPoints(rect)
        x0,y0,x1,y1 = cv.boundingRect(box)
        sym.append(x0)

    sym.sort()
    x_start = sym[0] #- 5
    x_end = sym[-1] + sq

    while(x_start < x_end):
        end_blok = x_start+sq +5# +10
        cv.rectangle(img,(x_start,0),(end_blok,y),(0,0,0),2)
        x_start = end_blok# + 10
    lines_new.append(img)

print(len(lines),len(lines_new))

showImage(lines_new[5])
