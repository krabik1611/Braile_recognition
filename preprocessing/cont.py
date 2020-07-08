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
        canny = self.Image
        contours, hierarchy = cv.findContours(canny,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        # contours, hierarchy = cv.findContours(canny.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(img, contours, -1, (0, 0, 0), 2, cv.LINE_AA, hierarchy, 2)
        plt.subplot(1,3,3),plt.imshow(cv.cvtColor(img,cv.COLOR_BGR2RGB))
        plt.title('mod'), plt.xticks([]),plt.yticks([])
        plt.subplot(1,3,2),plt.imshow(cv.cvtColor(canny,cv.COLOR_BGR2RGB))
        plt.title('canny'), plt.xticks([]),plt.yticks([])
        plt.show()
image = Get_cont('../dataFiles/origImage/cont_test.jpg')
image.get_cont()
