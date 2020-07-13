import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import image_processing as im

class Get_cont(im.ImageProcessing):
    def __init__(self,file_path):
        im.ImageProcessing.__init__(self,file_path)

    def get_cont(self):
        img = self.oImage
        plt.subplot(1,3,1),plt.imshow(cv.cvtColor(img,cv.COLOR_BGR2RGB))
        plt.title('Orig'), plt.xticks([]),plt.yticks([])
        ''' pull dot '''
        kernel = cv.getStructuringElement(cv.MORPH_RECT,(3,3))
        canny = cv.morphologyEx(self.Image,cv.MORPH_CLOSE,kernel)
        # canny = self.Image
        plt.subplot(1,3,2),plt.imshow(cv.cvtColor(canny,cv.COLOR_BGR2RGB))
        plt.title('canny'), plt.xticks([]),plt.yticks([])
        # contours, hierarchy = cv.findContours(canny,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        '''draw all contours'''
        contours, hierarchy = cv.findContours(canny.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(img, contours, -1, (0, 0, 0), 2, cv.LINE_AA, hierarchy, 1)
        '''draw all contours in rectage'''
        # for contour in contours:
        #     (x,y,w,h) = cv.boundingRect(contour)
        #     cv.rectangle(img, (x,y), (x+5,y+5), (0, 0, 0), 2)
        plt.subplot(1,3,3),plt.imshow(cv.cvtColor(img,cv.COLOR_BGR2RGB))
        plt.title('mod'), plt.xticks([]),plt.yticks([])
        plt.show()



    def test_method(self):
        def drawCont(img,contours):
            for cont in contours:
                '''func for draw all rectangle'''
                x0,y0,x1,y1 = cont
                x1+=x0
                y1+=y0
                cv.rectangle(img, (x0,y0), (x1,y1), (255, 255, 255), 3)
            return img
        def drawLine(self,img,contours):
            y,x = img.shape
            lines =[]
            contours.sort(key=lambda i: i[1])
            '''define count variables'''
            sredLine1,sredLine2,num=0,0,0

            '''find average value line in one string and add in list'''
            for i in range(len(contours)-1):
                if contours[i+1][1] -contours[i][1] < 30:
                    '''find count line and it value'''
                    num+=1
                    sredLine1+=contours[i][1]
                    sredLine2+= contours[i][3]
                else:
                    '''find average value'''
                    sredLine1 = int(sredLine1/num)
                    sredLine2 = int(sredLine2/num)
                    num = 0

                    lines.append([sredLine1,sredLine2+sredLine1])
            '''sort by Y coordinate'''
            lines.sort(key=lambda i:i[1])
            for line in lines:
                '''draw up and down line in every string'''
                y0,y1 = line

                cv.line(img,(0,y0-10),(x,y0-10),(255,255,255),2)
                cv.line(img,(0,y1+10),(x,y1+10),(255,255,255),2)




            return img





        oImg = self.oImage
        image = cv.GaussianBlur(oImg, (5,5), 0)
        image = cv.Canny(image,20,50)

        kernel = np.ones((5,5),np.uint8)

        dilation = cv.dilate(image.copy(),kernel,iterations=3)
        gradient = cv.morphologyEx(dilation, cv.MORPH_GRADIENT, kernel)
        '''show gradient image'''
        # plt.imshow(cv.cvtColor(gradient,cv.COLOR_BGR2RGB))
        # plt.show()

        edges = cv.Canny(gradient,20,50)

        '''show edges'''
        # plt.imshow(cv.cvtColor(edges,cv.COLOR_BGR2RGB))
        # plt.show()



        contours0, hierarchy = cv.findContours( gradient.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # lines = cv.HoughLines(edges,1,np.pi/180,200)
        # for line in lines:
        self.sredY= 0
        count = 0
        contours1 = []
        y,x = edges.shape

        for n in range(2):
            for cont in contours0:
                rect = cv.minAreaRect(cont)
                box = cv.boxPoints(rect)
                (x0,y0,x1,y1) = cv.boundingRect(box) #find two dot for rectagle
                '''
                (x0,y1)----0
                |          |
                0-----(x1,y1)
                '''
                if n==0:
                    self.sredY+= y1/len(contours0)
                else:
                    if self.sredY < y1:
                        if x0<0:
                            x0=0
                        if x1<0:
                            x1=0
                        if y0<0:
                            y0=0
                        if y1<0:
                            y1=0
                        contours1.append([x0,y0,x1,y1])

        edges =drawLine(self,edges,contours1)


        # edges = drawCont(edges,contours1)
        #
        plt.imshow(edges)
        plt.show()



image = Get_cont('../dataFiles/origImage/perfect3.jpg')
image.test_method()
