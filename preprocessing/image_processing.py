import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


class ImageProcessing():
	'''class for image processing'''
	def __init__(self,file_path):
		'''define file path and initialize proprities'''
		self.file_path = file_path
		self.imageProcessing() #start processing image after create object
		
	def imageProcessing(self):
		'''main processing function'''
		img = cv.imread(img_path, cv.IMREAD_GRAYSCALE) #read image
		img = cv.medianBlur(img,3)
		th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
					cv.THRESH_BINARY,11,2)
		
		self.images =  [img,th3]
		self.mainImage = th3
	def showPlot(self):
		'''visualization changes'''
		titles = ['Original Image', 'Adaptive Gaussian Thresholding'] #titles for plot
		for i in range(2):
			plt.subplot(1,2,i+1)
			plt.imshow(self.images[i],'gray')
			plt.title(titles[i])
			plt.xticks([]),plt.yticks([])

		plt.show()
		
	def getGaussianImage(self):
		'''get processing image'''
		return self.mainImage
		
	def saveGaussianImage(self,save_path):
		'''save image'''
		plt.imshow(self.mainImage)
		cv.imwrite(save_path,self.mainImage)

img_path = "test/1.jpg"

obj = ImageProcessing(img_path)
obj.showPlot()
