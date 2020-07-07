import cv2
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
		self.oImage = cv2.imread(self.file_path, cv2.IMREAD_GRAYSCALE) #read image
		self.oImage = cv2.GaussianBlur(self.oImage, (5, 5), 0) # delete trash

	def test(self):
		'''func for test launch'''
		self.upgradeImage()
		self.showImage()
	def upgradeImage(self):
		'''upgrage image 2 times'''
		self.Image = cv2.Canny(self.oImage, 20, 50)
		self.inv()

	def inv(self):
		'''make inverse pic'''
		_,self.wImage = cv2.threshold(self.Image,127,255,cv2.THRESH_BINARY_INV)


	def showImage(self):
		'''show changes in one layout'''
		orig = cv2.cvtColor(self.oImage,cv2.COLOR_BGR2RGB)
		mod = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
		mod2 = self.wImage #cv2.cvtColor(self.wImage,cv2.COLOR_BGR2RGB)
		plt.subplot(1,3,1),plt.imshow(orig)
		plt.title('Orig'), plt.xticks([]),plt.yticks([])
		plt.subplot(1,3,2),plt.imshow(mod)
		plt.title('mod1'), plt.xticks([]),plt.yticks([])
		plt.subplot(1,3,3),plt.imshow(mod2,'gray')
		plt.title('mod2'), plt.xticks([]),plt.yticks([])
		plt.show()
image = ImageProcessing('../dataFiles/origImage/1.jpg')
image.test()
