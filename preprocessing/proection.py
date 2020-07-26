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
    # show(canny)
    M = cv.getRotationMatrix2D(center, grad, 1.0)
    lines = cv.warpAffine(image, M, (x, y))                 # transofrm image
    return lines
    mask = np.zeros((y+2,x+2),np.uint8)
    cv.floodFill(dark,mask,(0,0),255)
    dark_imv = cv.bitwise_not(dark)

    show(dark_imv)


def cut(image):
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
    # show(dark_contours)
    lenLines = []
    sredLenCont = 0
    for cont in contours:
        lenLines.append(len(cont))
    mean = np.mean(lenLines)
    # print("Before:\n",np.var(lenLines),"\n",mean)
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
    # print("After:\n",np.var(lenLines),"\n",mean)


    dark_contours1 = cv.drawContours(dark.copy(), contours, -1, (255, 255, 255), 4)
    # open = imgModify(dark_contours1,'open',(5,10))

    # dilateX = imgModify(open,"dilate",(100,2*x))
    # dilateX_ = cv.bitwise_not(dilateX)
    # dilateY = imgModify(open,"dilate",(2*y,100))
    # area = cv.bitwise_and(dilateX,dilateX,mask=dilateY)
    # area_ = cv.bitwise_not(area)
    # white_layer = cv.bitwise_and(white,white,mask=area_)
    # testImg = cv.bitwise_and(img,img,mask=area)
    # dst = cv.add(white_layer,testImg)
    # show2Image(dilateX,dilateY)
    # show(dst)
    # areaCont = contour(area)[::-1]
    # rect = cv.minAreaRect(areaCont[0])                # get coordinates
    # box = cv.boxPoints(rect)                   # for all symbol
    # x0,y0,x1,y1 = cv.boundingRect(box)
    # imgArea = img[y0:y0+y1,x0:x1+x0]
    # showImage([img,imgArea,dst])
    # show2Image(dilateX,dilateY)
    # show(dark_contours1)
    open = imgModify(dark_contours1,'open',(5,10))
    dilate_open = imgModify(open,"dilate",(5,5))
    close = imgModify(dilate_open,"open",(20,20))
    # show(close)
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
    cv.rectangle(close,(minX,minY),(maxX,maxY),(255,255,255),2)
    # show(close)
    return img[minY:maxY,minX:maxX]
    # show2Image(img,dilate_open)


def cutH(img):
    '''find and cut image for horizontal position'''
    def AB(d1,d2):
        '''calculate parametrs for straight'''
        x1,y1 = d1
        x2,y2 = d2
        a = (y2-y1)/(x2-x1)
        b = y1-a*x1
        return (a,b)

    y,x = img.shape


    edges = imgModify(img,"edges")
    lines = cv.HoughLines(edges,1,np.pi/180,250)
    line1 = []
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
        line1.append([(x1,y1),(x2,y2)])

    line1.sort(key = lambda i: i[0][1])
    for i in range(len(line1)):                 # find need lines
        if not i:
            last = line1[i][0][1]
            continue
        else:
            if line1[i][0][1] - last < y/4:
                minY = line1[i]
                last = line1[i][0][1]
            else:
                maxY = line1[i]
                break
# calculate parametr Y for line
    _,b1 = AB(minY[0],minY[1])

    _,b2 = AB(maxY[0],maxY[1])
    return img[int(b1):int(b2),0:x]            # slice image
# edges = imgModify(img1, "edges")
# show(img1)



def test_many():
    for i in range(1,30):

        path = '../dataFiles/origImage/book/%i.jpeg' %i
        try:
            img = cv.imread(path,cv.IMREAD_GRAYSCALE)
        except:
            print("read error:%i"%i)
            continue
        # img1 = cutH(img)
        try:
            cut = cut(img)
        except:
            print("Cut error:%i"%i)
            continue
        try:
            rotated = rotateHorizontal(cut)
        except:
            print("rotated error:%i"%i)
            continue
        try:
            show2Image(img,rotated)
        except:
            print("show Error:%i"%i)
            continue

def main():
    path = '../dataFiles/origImage/2.jpg'
    try:
        img = cv.imread(path,cv.IMREAD_GRAYSCALE)
    except:
        print("read error")
        return 0
    # img1 = cutH(img)
    try:
        cut = cut(img)
    except:
        print("Cut error")
        return 0
    try:
        rotated = rotateHorizontal(cut)
    except:
        print("rotated error")
        return 0
    try:
        show2Image(img,rotated)
    except:
        print("show Error")
        return 0
if __name__ == '__main__':
    main()
