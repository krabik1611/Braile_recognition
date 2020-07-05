import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img_path = "test/1.jpg"

class ImageProcessing():
	def __init__(self,file_path):
		self.file_path = file_path
		self.images = []
		self.titles = ['Original Image', 'Global Thresholding (v = 127)',
						'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
		self.imageProcessing()
		
	def imageProcessing(self):
		img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
		img = cv.medianBlur(img,3)
		ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
		th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
					cv.THRESH_BINARY,11,2)
		th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
					cv.THRESH_BINARY,11,2)
		
		self.images = [img, th1, th2, th3]
		self.mainImage = th3
	def showPlot(self):
		
		for i in range(4):
			plt.subplot(2,2,i+1)
			plt.imshow(self.images[i],'gray')
			plt.title(self.titles[i])
			plt.xticks([]),plt.yticks([])

		plt.show()
	def getGaussianImage(self):
		return self.mainImage
	def saveGaussianImage(self,save_path):
		plt.imshow(self.mainImage)
		cv.imwrite(save_path,self.mainImage)
		
obj = ImageProcessing(img_path)
obj.showPlot()
