import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage import morphology


class ImageProcessing():
	'''class for image processing'''
	def __init__(self,file_path):
		'''define file path and initialize proprities'''
		self.file_path = file_path
		self.imageProcessing() # start processing image after create object

	def imageProcessing(self):
		'''main processing function'''
		self.oImage = cv.imread(self.file_path, cv.IMREAD_GRAYSCALE) #read image
		self.oImage = cv.GaussianBlur(self.oImage, (5, 5), 0) # delete trash

	def test(self):
		'''func for test launch'''
		self.upgradeImage()
		self.showImage()
	def upgradeImage(self):
		'''upgrage image 2 times'''
		image = cv.Canny(self.oImage, 10, 100)
		# self.inv()
		kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
		image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
		cnts = cv.findContours(image.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE )[1]
		self.Image = cv.drawContours(self.oImage,cnts,(127,127,127),3)

	def inv(self):
		'''make inverse pic'''
		_,self.wImage = cv.threshold(self.Image,127,255,cv.THRESH_BINARY_INV)


	def showImage(self):
		'''show changes in one layout'''
		orig = cv.cvtColor(self.oImage,cv.COLOR_BGR2RGB)
		mod = cv.cvtColor(self.Image, cv.COLOR_BGR2RGB)
		# mod2 = self.wImage #cv.cvtColor(self.wImage,cv.COLOR_BGR2RGB)
		plt.subplot(1,3,1),plt.imshow(orig)
		plt.title('Orig'), plt.xticks([]),plt.yticks([])
		plt.subplot(1,3,2),plt.imshow(mod)
		plt.title('mod1'), plt.xticks([]),plt.yticks([])
		# plt.subplot(1,3,3),plt.imshow(mod2,'gray')
		# plt.title('mod2'), plt.xticks([]),plt.yticks([])
		plt.show()
image = ImageProcessing('../dataFiles/origImage/2.jpg')
image.test()
