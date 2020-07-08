import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


class ImageProcessing():
	'''class for image processing'''
	def __init__(self,file_path):
		'''define file path and initialize proprities'''
		self.file_path = file_path
		self.imageProcessing() # start processing image after create object
		self.upgradeImage()

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
		#self.image = cv.GaussianBlur(self.oImage, (5, 5), 0)
		self.Image = cv.Canny(self.oImage, 30, 70)
		self.inv()

		def getPic(self,key):
			self.upgradeImage()
			pic = {"dark":self.wImage,
					"orig":self.oImage,
					"white":self.wImage}
			return pic[key]
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
