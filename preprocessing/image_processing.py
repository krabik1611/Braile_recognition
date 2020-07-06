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
		# self.Image = cv2.medianBlur(self.Image,3)

	def test(self):
		self.showImage()
	def upgradeImage(self):
		self.Image = cv2.adaptiveThreshold(self.oImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
					cv2.THRESH_BINARY,11,2)
		# self.upImage = morphology.remove_small_holes(np.array(self.Image,bool),10)
	def showImage(self,image=0):
		if image==0:
			image = self.oImage
		plt.subplot(1,2,1),plt.imshow(self.oImage)
		plt.title('Orig'), plt.xticks([]),plt.yticks([])
		plt.subplot(1,2,2),plt.imshow(image)
		plt.title('test'), plt.xticks([]),plt.yticks([])
		plt.show()
image = ImageProcessing('../dataFiles/origImage/1.jpg')
image.test()
