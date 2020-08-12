import cv2 as cv
import numpy as np
import math
from matplotlib import pyplot as plt
from os import system as sys
import os


class Image():
    def __init__(self,path):
        self.path = path
        self.Image = cv.imread(path)
        # if self.__checkBright__() == 255:
        #     return None
        self.y,self.x,_= self.Image.shape
        self.img = cv.cvtColor(self.Image,cv.COLOR_BGR2GRAY)
        self.__dark__ = dark = np.zeros((self.y,self.x,3),np.uint8)
        self.__defaultKernel__ = np.ones([5,5],np.uint8)

    def __checkBright__(self):
        img = self.Image.copy()
        if np.mean(img) > 220:
            return 255


    def showImage(self,*img):
        if len(img) == 0:
            plt.subplot(1,2,1),plt.imshow(self.Image)
            plt.title("Orig"), plt.xticks([]),plt.yticks([])
            plt.subplot(1,2,2),plt.imshow(cv.cvtColor(self.img,cv.COLOR_BGR2RGB))
            plt.title("mod"), plt.xticks([]),plt.yticks([])
        elif len(img) == 1:
            plt.subplot(1,2,1),plt.imshow(self.Image)
            plt.title("Orig"), plt.xticks([]),plt.yticks([])
            plt.subplot(1,2,2),plt.imshow(cv.cvtColor(img[0],cv.COLOR_BGR2RGB))
            plt.title("mod"), plt.xticks([]),plt.yticks([])
        elif len(img) == 2:
            plt.subplot(1,2,1),plt.imshow(cv.cvtColor(img[0],cv.COLOR_BGR2RGB))
            plt.title("1"), plt.xticks([]),plt.yticks([])
            plt.subplot(1,2,2),plt.imshow(cv.cvtColor(img[1],cv.COLOR_BGR2RGB))
            plt.title("2"), plt.xticks([]),plt.yticks([])

        plt.show()

    def imgModify(self,img,key,kernel_size=(5,30)):
        '''modify image and return need type'''

        img = img.copy()
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
        self.imgMod = image
        return image

    def findContour(self,img,**kword):
        '''draw contour in image'''
        if kword["key"]=="external":
            type = cv.RETR_EXTERNAL
        elif kword["key"] == "tree":
            type = cv.RETR_TREE
        else:
            print("Key not found")
            return -1
        if "debug" in kword:
            debug = kword["debug"]
        else:
            debug = 0
        img = img.copy()
        contours, hierarchy = cv.findContours(img.copy(), type, cv.CHAIN_APPROX_SIMPLE)
        if debug:
        # debug function
            cv.drawContours(img, contours, -1, (255, 255, 255), 2, cv.LINE_AA, hierarchy, 1)
            self.showImage(img)

        return contours

    def delCont(self,contours,**kword):
        "del long contours"

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


        dark = self.__dark__.copy()
        cv.drawContours(dark, contours, -1, (255, 255, 255), 1)
        dark = cv.cvtColor(dark,cv.COLOR_BGR2GRAY)
        self.__DarkContours__ = dark

        if "debug" in kword:
            debug = kword["debug"]
        else:
            debug = 0

        if debug:
        # debug function
            self.showImage(self.__DarkContours__)
        return contours

    def __findRect__(self,img,**kword):
        img = img.copy()
        contours = self.findContour(img,key="tree")
        boxes = []
        lines = []
        for cont in contours:
            rect = cv.minAreaRect(cont)
            box = cv.boxPoints(rect)
            x0,y0,x1,y1 = cv.boundingRect(box)
            boxes.append([x0,y0,x1,y1])

        boxes.sort(key=lambda x: x[1])
        for box in boxes:
            x0,y0,x1,y1 = box
            lines.append(self.img[y0:y1+y0,x0:x0+x1])


        if "debug" in kword:
            debug = kword["debug"]
        else:
            debug = 0

        if debug:
            img = self.img.copy()
            for line,box in zip(lines,boxes):
                x0,y0,x1,y1 = box
                cv.rectangle(img,(x0,y0),(x0+x1,y0+y1),(0,0,0),2)

            self.showImage(img)
        return lines

    def cutWithMask(self,**kword):
        """create image mask and cut image"""

        img = self.__DarkContours__.copy()
        img = cv.morphologyEx(img.copy(),cv.MORPH_CLOSE,self.__defaultKernel__)

        y,x = img.shape
        horizontalMask = self.imgModify(img=img,key="dilate",kernel_size=(5,int(self.x*1.5)))
        verticalMask = self.imgModify(img=img,key="dilate",kernel_size=(int(self.y),15))
        mask = cv.bitwise_and(horizontalMask,verticalMask)
        self.lines = self.__findRect__(mask)
        # sredY  = 0
        for line in self.lines:
            y,x = line.shape
            # sredY += (y)/len(self.lines)
        # print(sredY)
        try:
            self.lines = self.__rotationsLines__(self.lines)
        except:
            pass

        check = False
        for line in self.lines:
            y,_ = line.shape
            if y > 70:
                check = True
                break

        if check:
            lines = []
            for line in self.lines:
                y,_ = line.shape
                if y > 70:
                    add = self.checkString(line)
                    lines.extend(add)
                else:
                    lines.append(line)

            self.lines = lines
        return self.lines


        if "debug" in kword:
            debug = kword["debug"]
        else:
            debug = 0

        if debug:
        # debug function
            # self.showImage(horizontalMask)
            self.showImage(mask)

    def __rotationsLines__(self,lines):
        def checkAngle(img,img1):
            img = img.copy()
            lines = cv.HoughLines(img,1,np.pi/180,250)            # get line
            sredG = 0

            for line in lines:
                rho,theta = line[0]
                a = np.cos(theta)

                sredG+=a/len(lines)

            return abs(math.degrees(sredG))

        lines1 = []
        kernel = np.ones([5,5],np.uint8)
        kernel_dilate = np.ones([1,50],np.uint8)
        for line in lines:
            y,x = line.shape
            line = cv.GaussianBlur(line,(5,5),0)
            edges = self.imgModify(line,"edges")
            close = cv.morphologyEx(edges,cv.MORPH_CLOSE,kernel)
            dilate = cv.dilate(close,kernel_dilate,iterations=2)
            grad = checkAngle(dilate,line)
            center = (x//2,y//2)
            M = cv.getRotationMatrix2D(center, grad, 1.0)
            test = cv.warpAffine(line, M, (x, y))
            lines1.append(test)
        return lines1



    def checkString(self,img):
        '''check string in cut lines'''
        img = img.copy()
        string = []
        y,x = img.shape
        edges = cv.Canny(img,30,70)
        cont = self.findContour(edges,key="tree")
        contours = self.delCont(cont)
        image = self.__DarkContours__
        kernel = np.ones([1,int(x*1.5)],np.uint8)
        line1 = cv.dilate(image,kernel,iterations=1)
        contours, hierarchy = cv.findContours(line1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contour = []
        for cont in contours[::-1]:
            rect = cv.minAreaRect(cont)
            box = cv.boxPoints(rect)
            x0,y0,x1,y1 = cv.boundingRect(box)

            contour.append([0,y0-3,x,y1+3+y0])
        for cont in contour:
            x0,y0,x1,y1 = cont
            string.append(img[y0:y1,x0:x1])

        return string

    def getSymbol(self,img):
        img = img.copy()
        img = cv.GaussianBlur(img,(3,3),0)
        edges = cv.Canny(img,30,70)

        # create kernel any size for next actions
        kernel_dialte = np.ones((100,5),np.uint8)
        kernel_close = np.ones((5,5),np.uint8)

        # Dilate image and close it for get rectagle contours symbols
        dilate = cv.dilate(edges,kernel_dialte,iterations=1)
        close = cv.morphologyEx(dilate,cv.MORPH_CLOSE, kernel_close, iterations=1)
        self.showImage(dilate,close)
        contours = self.findContour(close,key="external")[::-1]

        sredX = 0 # sred value X1
        symbols = [] # list for keep coordinates all symbols
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
                        space.append([x_,sredX+5])
                    x0_ , x1_ = symbols[i]
                    x_ = x0_ + x1_                          # calculate coords symbol
                                                            # for next iterations

            symbols.extend(space)                           # add space in default list
            symbols.sort()
            y,x = img.shape
        # for sym in symbols:
        #     image = img.copy()
        #     x0,x1 = sym
        #     cv.rectangle(image,(x0,0),(x1,y),(255,255,255),2)
        #     plt.imshow(image)
        #     plt.show()


        return symbols



def main():
    for i in range(1,2):
        path = "../dataFiles/origImage/book/1.jpeg"
        image = Image(path)
        if image.__checkBright__()==255:
            continue
        else:
            print(path)
            canny = image.imgModify(image.img,key="edges")
            contours = image.findContour(canny,key="tree")
            contours = image.delCont(contours)
            lines = image.cutWithMask()

            for line in lines:
                symb = image.getSymbol(line)
                # plt.imshow(line)
                # plt.show()
    # image.showImage(canny)


if __name__ == '__main__':
    main()
