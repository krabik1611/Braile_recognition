from processing_string import *
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math

def show(img):
    plt.imshow(cv.cvtColor(img,cv.COLOR_BGR2RGB))
    plt.show()

def rotateHorizontal(img):
    '''Rotate image for normal position'''
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

path = '../dataFiles/origImage/3.jpg'

img = cv.imread(path,cv.IMREAD_GRAYSCALE)
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
img1 = cutH(img)
# edges = imgModify(img1, "edges")
# show(img1)


rotated = rotateHorizontal(img1)
show(rotated)
