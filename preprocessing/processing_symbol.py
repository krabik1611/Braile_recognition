from processing_string import *
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


path = '../dataFiles/origImage/perfect3.jpg'
lines = returnLines(path)

image = []

def getCoordSymbols(line):
    '''func for return coords X0 and X1 for All symbol'''
    line = line.copy()
    img = imgModify(line,'edges')


    # create kernel any size for next actions
    kernel_dialte = np.ones((100,5),np.uint8)
    kernel_close = np.ones((5,5),np.uint8)
    # Dilate image and close it for get rectagle contours symbols
    dilate = cv.dilate(img,kernel_dialte,iterations=1)
    close = cv.morphologyEx(dilate,cv.MORPH_CLOSE, kernel_close, iterations=1)
    # close is useful image for next actions
    contours, hierarchy = cv.findContours( close.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = contours[::-1]
    sredX = 0 # sred value X1
    symbols = [] # list for keep coordinates all symbols
    sredX = int(sredX)
    for i in range(2):
        for cont in contours:
            rect = cv.minAreaRect(cont)                # get coordinates
            box = cv.boxPoints(rect)                   # for all symbol
            x0,y0,x1,y1 = cv.boundingRect(box)         #
            if not i:
                sredX += (x1)/len(contours)            # calculate average X1
            else:
                if x1/sredX > 1.5:                     # divide big rectangle
                    x1 = int(x1//2)                    # into 2 small
                    symbols.append([x0,x1])
                    symbols.append([x0+x1,x1])
                elif x1/sredX < 0.7:                   # multiplicate small rectangle
                    x1 = x1*2
                    symbols.append([x0,x1])
                else:
                    symbols.append([x0,x1])            # add normal rectangle

        if not i:
            sredX = int(sredX)
        symbols.sort()
        space = []                                     # keep space value
        for i in range(len(symbols)):
            if not i:
                x0_ , x1_ = symbols[i]
                x_ = x0_ + x1_                         # calculate coords prevous symbol
            else:
                x0 , _ = symbols[i]
                if sredX < x0-x_:
                    space.append([x_,sredX])
                x0_ , x1_ = symbols[i]
                x_ = x0_ + x1_                          # calculate coords symbol
                                                        # for next iterations


        symbols.extend(space)                           # add space in default list
        symbols.sort()
    return symbols

# for line in lines:
#     line  = line.copy()
#     symbols = getCoordSymbols(line)
#     y,x = line.shape
#     check = 0
#     for sym in symbols:
#         x0,x1 = sym
#         # cv.line(line,(x0,0),(x0,y),(255,255,255),2)
#         if not check:
#             cv.rectangle(line,(x0,0),(x1+x0,y),(0,0,0),2)
#             check = 1
#         else:
#             cv.rectangle(line,(x0,0),(x1+x0,y),(255,255,255),2)
#     image.append(line)
# showImage(image)


def getSymbols(lines):
    image = []
    for line in lines:
        line = line.copy()
        symbols = getCoordSymbols(line)
        y,x = line.shape
        for sym in symbols:
            x0,x1 = sym
            image.append(line[0:y,x0:x1+x0])
    return image
symbols = getSymbols(lines)
show2Image(symbols[0], symbols[1])
