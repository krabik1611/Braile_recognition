import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from os import system as sys

def showImage(*img):
    '''show one or two image in one plot'''
    if type(img[0]) is list:
        images = img[0]
        row = len(images)//2 + 1
        column =2
        lenght = len(images)+1
        print(lenght-1)
        for n in range(1,lenght):

            plt.subplot(row,column,n),plt.imshow(cv.cvtColor(images[n-1],cv.COLOR_BGR2RGB))
            plt.title(n), plt.xticks([]),plt.yticks([])

        plt.show()


    else:
        if len(img)//2 ==0:
            row = 1
        else:
            row = len(img)//2 + 2
        if len(img) % 2 == 0:
            column = 2
        else:
            column = 1
        lenght = len(img)
        for i in range(1,lenght+1):
            plt.subplot(row,column,i),plt.imshow(img[i-1])
            plt.title(i), plt.xticks([]),plt.yticks([])
        plt.show()

def saveString(path,lines):
    file_save = path[:-4]
    sys('mkdir %s' %file_save)
    count = 1
    for string in lines:
        file_save = path[:-4] + "/%i.jpg" %count
        print(file_save)
        cv.imwrite(file_save,string)
        count+=1
    print('complete')

def readImage(file_path):
    '''only read image and return it'''
    img = cv.imread(file_path,cv.IMREAD_GRAYSCALE)
    return img

def imgModify(img,key):
    '''modify image and return need type'''
    img = cv.GaussianBlur(img, (5, 5), 0)
    img = cv.GaussianBlur(img, (5, 5), 0)
    edges = cv.Canny(img,20,70)

    kernel = np.ones((5,30),np.uint8)


    dilate = cv.dilate(edges,kernel,iterations=1)
    closing = cv.morphologyEx(dilate,cv.MORPH_CLOSE,kernel,iterations=2)
    open  = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel,iterations=2)


    dict = {"edges":edges,
            "dilate":dilate,
            "closing":closing,
            "open":open}
    # use open. best result
    return dict[key]

def drawRect(img,contours):
    '''draw rect in any image'''
    img = img.copy()
    for cont in contours:
        x0,y0,x1,y1 = cont
        cv.rectangle(img,(x0,y0),(x1,y1),(255,255,255),2)
    return img

def drawLine(img,contours):
    '''draw line in image'''
    img = img.copy()
    y,x = img.shape
    for cont in contours:
        _, y0, _, y1 = cont
        cv.line(img,(0,y0),(x,y0),(0,0,0),2)
        cv.line(img,(0,y1),(x,y1),(0,0,0),2)
    return cv.cvtColor(img,cv.COLOR_BGR2RGB)
def cont(img):
    '''draw contour in image'''
    img = img.copy()
    contours, hierarchy = cv.findContours(img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(img, contours, -1, (255, 255, 255), 2, cv.LINE_AA, hierarchy, 1)
    return img

def getCont(img):
    '''find and return big contour'''
    contours, hierarchy = cv.findContours( img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour = []
    sredY = 0
    for n in range(2):
        for cont in contours:
            rect = cv.minAreaRect(cont)
            box = cv.boxPoints(rect)
            x0,y0,x1,y1 = cv.boundingRect(box)
            # y0-=5
            # y1+=5
            if n==0:
                sredY += y1/len(contours)
            else:
                if sredY<y1:
                    if x0<0:
                        x0=0
                    if x1<0:
                        x1=0
                    if y0<0:
                        y0=0
                    if y1<0:
                        y1=0
                    contour.append([x0,y0-5,x1,y1+y0+5])
    return contour

def getString(img,contours):
    '''return slice image'''
    img = img.copy()
    _,x = img.shape
    lines = []
    for cont in contours:
        _, y0, _, y1 = cont
        lines.append(img[y0:y1,0:x])
    return lines

def allAction(path):
    '''func for run all action'''
    img = readImage(path)
    imgMod = imgModify(img, 'open')
    contour = getCont(imgMod)
    # lines = getString(img, contour)
    img = drawLine(img, contour)
    showImage(img)
    # saveString(path,lines)
allAction('../dataFiles/origImage/perfect2.jpg')
