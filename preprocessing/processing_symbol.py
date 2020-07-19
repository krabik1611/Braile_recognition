from processing_string import *
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

path = '../dataFiles/origImage/perfect3.jpg'
img = readImage(path)
imgMod = imgModify(img, 'open')
contour = getCont(imgMod)
lines = getString(img, contour)

image = []
line = lines[0]
# for line in lines:
def getClose(line):
    line = line.copy()
    line = imgModify(line, "edges")

    kernel_dilate = np.ones((5,5),np.uint8)

    dilate = cv.dilate(line,kernel_dilate,iterations=1)

    kernel_close = np.ones((100,6),np.uint8)

    close = cv.morphologyEx(line,cv.MORPH_CLOSE, kernel_close,iterations=1)
    # image.append(close)
    return close
