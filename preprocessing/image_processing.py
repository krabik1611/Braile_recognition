import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage import morphology


class ImageProcessing():
	'''class for image processing'''
	def __init__(self,file_path):
		'''define file path and initialize proprities'''
		self.file_path = file_path
		self.imageProcessing() #start processing image after create object
		
	def imageProcessing(self):
		'''main processing function'''
		img = cv.imread(self.file_path, cv.IMREAD_GRAYSCALE) #read image
		img = cv.medianBlur(img,3)
		th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
					cv.THRESH_BINARY,11,2)
		
		self.images =  [img,th3]
		self.mainImage = th3

	def upgradeImage(self):
		self.upImage = morphology.remove_small_holes(np.array(self.mainImage,bool),10)
		plt.subplot(1,2,1),plt.imshow(self.mainImage)
		plt.subplot(1,2,2), plt.imshow(self.upImage)
		plt.show()
		
		return self.upImage
	def saveImage(self,save_path):
		self.upgradeImage()
		
		cv.imwrite(save_path,self.upImage)
		
a = ImageProcessing('../dataFiles/origImage/2.jpg')
a.saveImage('../dataFiles/Image/2.jpg')

