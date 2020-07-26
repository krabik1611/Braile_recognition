import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from os import system as sys
import os

def showImage(*img):
    '''show one or two image in one plot'''
    if type(img[0]) is list:
        images = img[0]
        row = len(images)//2 + 1
        column =2
        lenght = len(images)+1
        # print(lenght-1)
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
def show2Image(img1,img2):
    '''func for show 2 image inone plot'''
    # powerful compared for showImage
    plt.subplot(1,2,1), plt.imshow(cv.cvtColor(img1,cv.COLOR_BGR2RGB))
    plt.title(1), plt.xticks([]),plt.yticks([])
    plt.subplot(1,2,2), plt.imshow(cv.cvtColor(img2,cv.COLOR_BGR2RGB))
    plt.title(2), plt.xticks([]),plt.yticks([])
    plt.show()

def saveString(path,lines):
    '''save string'''
    file_save = path[:-4]
    try:
        os.mkdir(file_save)
        print("Folder create")
    except OSError:
        print("Folder exist")
    count = 1
    for string in lines:
        file_save = path[:-4] + "/%i.jpg" %count
        print(file_save)
        cv.imwrite(file_save,string)
        count+=1
    print('complete')
def saveSymbols(path,symbols):
    '''save all Symbols'''
    file_save = path[:-4]
    try:
        os.mkdir(file_save)
        print("Folder create")
    except OSError:
        print("Folder exist")
    count = 1
    for sym in symbols:
        file_save = path[:-4] + "/%i.png" %count
        print(file_save)
        try:
            cv.imwrite(file_save,sym)
            count+=1
        except cv.error:
            pass


def readImage(file_path):
    '''only read image and return it'''
    img = cv.imread(file_path,cv.IMREAD_GRAYSCALE)
    return img

def imgModify(img,key,kernel_size=(5,30)):
    '''modify image and return need type'''
    img = cv.GaussianBlur(img, (5, 5), 0)
    img = cv.GaussianBlur(img, (5, 5), 0)
    if key=="edges":
        image = cv.Canny(img,20,70)
    else:
        kernel = np.ones(kernel_size,np.uint8)
        if key=="dilate" or key=="closing" :
            edges = cv.Canny(img,20,70)
            image = cv.dilate(edges,kernel,iterations=1)
        elif key=="closing":
            edges = cv.Canny(img,20,70)
            dilate = cv.dilate(edges,kernel,iterations=1)
            image = cv.morphologyEx(dilate,cv.MORPH_CLOSE,kernel,iterations=2)
        elif key=="open":
            edges = cv.Canny(img,20,70)
            dilate = cv.dilate(edges,kernel,iterations=1)
            closing = cv.morphologyEx(dilate,cv.MORPH_CLOSE,kernel,iterations=2)
            image  = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel,iterations=2)
        elif key =="erode":
            image = cv.erode(img,kernel,iterations = 1)
    return image

def drawRect(img,contours):
    '''draw rect in any image'''
    img = img.copy()
    check = 0
    for cont in contours:

        x0,y0,x1,y1 = cont
        if not check:

            cv.rectangle(img,(x0,y0),(x1,y1),(0,0,0),2)
            check = 1
        else:
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
def contour(img):
    '''draw contour in image'''
    img = img.copy()
    contours, hierarchy = cv.findContours(img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(img, contours, -1, (255, 255, 255), 2, cv.LINE_AA, hierarchy, 1)
    return contours

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
    return contour[::-1]


def getString(img,contours):
    '''return slice image'''
    img = img.copy()
    _,x = img.shape
    lines = []
    for cont in contours:
        _, y0, _, y1 = cont
        lines.append(img[y0:y1,0:x])
    return lines
def getSymbols(lines):
    '''return slice image'''
    image = []
    for line in lines:
        line = line.copy()
        symbols = getCoordSymbols(line) # get coords symbols
        y,x = line.shape
        for sym in symbols:
            x0,x1 = sym
            image.append(line[0:y,x0:x1+x0])
    return image

def returnLines(path):
    '''return list of lines'''
    img = readImage(path)
    imgMod = imgModify(img, 'open')
    contour = getCont(imgMod)
    lines = getString(img, contour)
    return lines

def allAction(path):
    '''func for run all action'''
    img = readImage(path)
    imgMod = imgModify(img, 'open')
    contour = getCont(imgMod)
    lines = getString(img, contour)
    # lines = drawRect(img, contour)
    # symbols = getSymbols(lines)
    # saveSymbols(path, symbols)
    showImage(lines)



if __name__ == '__main__':
    allAction('../dataFiles/origImage/perfect1.jpg')
