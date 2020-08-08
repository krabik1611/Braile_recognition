from processing_string import *
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import pandas as pd

def show(img):
    plt.imshow(cv.cvtColor(img,cv.COLOR_BGR2RGB))
    plt.show()

def rotateHorizontal(img):
    '''Rotate image to normal position'''
    image = img.copy()
    y,x = img.shape

    edges = imgModify(image, 'edges')               # get Canny
    contours = contour(edges)                       # get contours
    i=0

    while i < len(contours):                        #delete long contours
        if len(contours[i])>50:
            del contours[i]
        else:
            i+=1

    dark = np.zeros((y,x,3),np.uint8)               # create dark pic
    dark[:] = (0,0,0)
    cv.drawContours(dark, contours, -1, (255, 255, 255), 3) # draw contourn in dark
    close = imgModify(dark, "open",(5,5))                   # some process image
    dilate = imgModify(close, "dilate",(5,30))
    close = imgModify(dilate, "open",(10,30))
    canny = imgModify(close,"edges")
    lines = cv.HoughLines(canny,1,np.pi/180,250)            # get line
    sredG = 0
    for line in lines:
        rho,theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 10000*(-b))
        y1 = int(y0 + 10000*(a))
        x2 = int(x0 - 10000*(-b))
        y2 = int(y0 - 10000*(a))
        sredG+=a/len(lines)                                 # calculate average
                                                            # value of angle
    center = (x//2,y//2)
    grad = abs(math.degrees(sredG))
    M = cv.getRotationMatrix2D(center, grad, 1.0)
    lines = cv.warpAffine(image, M, (x, y))                 # transofrm image
    return lines



def cutA(image):
    """tranfer image to another place with mask"""
    img = image.copy()
    y,x = img.shape
    # add black and white image for next action
    dark = np.zeros((y,x,3),np.uint8)               # create dark pic
    white = np.ones((y,x,3),np.uint8)               # create white pic
    white[:] = (255,255,255)
    white = cv.cvtColor(white,cv.COLOR_RGB2GRAY)
    # get Canny image
    edges = imgModify(img,"edges")
    # show(edges)
    # get all contours
    contours = contour(edges)
    # draw all contour
    dark_contours = cv.drawContours(dark.copy(), contours, -1, (255, 255, 255), 3)
    lenLines = []
    for cont in contours:
        lenLines.append(len(cont))
    mean = np.mean(lenLines)
    deviations = (np.var(lenLines))**0.5
    lenLines = []
    i = 0
    while i < len(contours):                        #delete long contours
        if len(contours[i])>mean+deviations:
            del contours[i]
        else:
            i+=1

    for cont in contours:
        lenLines.append(len(cont))
    mean = np.mean(lenLines)


    dark_contours1 = cv.drawContours(dark.copy(), contours, -1, (255, 255, 255), 1)
    # show2Image(edges,dark_contours1)

    open = imgModify(dark_contours1,'open',(5,10))
    dilate_open = imgModify(open,"dilate",(5,5))
    close = imgModify(dilate_open,"open",(20,20))
    contours = contour(close)
    ones = 1
    for cont in contours:
        rect = cv.minAreaRect(cont)
        box = cv.boxPoints(rect)
        x0,y0,x1,y1 = cv.boundingRect(box)
        if ones:
            ones=0
            minX = x0
            minY = y0
            maxX=x0+x1
            maxY=y0+y1
        else:
            if minX>x0:
                minX=x0
            if minY > y0:
                minY=y0
            if maxX<x1+x0:
                 maxX=x1+x0
            if maxY < y0+y1:
                maxY = y0+y1
    if minX<0:
        minX=0
    if minY<0:
        minY=0
    if maxX>x:
        maxX=x
    if maxY>y:
        maxY=y
    # cv.rectangle(close,(minX,minY),(maxX,maxY),(255,255,255),2)
    return img[minY:maxY,minX:maxX]



def check_bright(image):
    img = image.copy()
    y,x = img.shape
    if np.mean(img) > 210:
        return 0
    else:
        return 1



    # show2Image(img,img1)

def runMany(images):
    if images is list or images is tuple:
        for img in images:
            try:
                cut = cutA(img)
            except:
                print("Cut error:%i"%i)

            try:
                rotated = rotateHorizontal(cut)
                # complete.append(rotated)
            except:
                print("rotated error:%i"%i)
            try:
                show2Image(img,rotated)
            except:
                print("show Error:%i"%i)
    else:
        print("Not list or tuple")

def runSingle(img):
    try:
        cut = cutA(img)
    except:
        print("Cut error")
        return 0
    try:
        rotated = rotateHorizontal(cut)
    except:
        print("rotated error")
        return 0
    try:
        # show2Image(img,rotated)
        return rotated
    except:
        print("show Error")
        return 0

def main():
    # path = '../dataFiles/origImage/4.jpg'
    path = '../dataFiles/origImage/book/8.jpeg'
    img = cv.imread(path,cv.IMREAD_GRAYSCALE)
    if 1:#check_bright(img):
        rotated = runSingle(img)
    else:
        print("Light image")
    showLines(rotated)
if __name__ == '__main__':
    main()
