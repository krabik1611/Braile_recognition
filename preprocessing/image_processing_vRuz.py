import cv2 as cv
import numpy as np
#import imutils
from matplotlib import pyplot as plt
from skimage import morphology
import math


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
					cv.THRESH_BINARY,11,3)

		self.images =  [img,th3]
		self.mainImage = th3

	def upgradeImage(self):
		self.upImage = morphology.remove_small_holes(np.array(self.mainImage,int),15)

		#plt.subplot(1,2,1),plt.imshow(self.mainImage)
		#plt.subplot(1,2,2),plt.imshow(self.upImage)
		#plt.show()

		return self.upImage
	def saveImage(self,save_path):
		self.upgradeImage()

		cv.imwrite(save_path,self.upImage)
	def detectLines(self):

		img = cv.imread(self.file_path)
		gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

		gray = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
					cv.THRESH_BINARY,11,3)

		plt.subplot(1,3,1),plt.imshow(gray)
		plt.title('gray'), plt.xticks([]),plt.yticks([])
		edges = cv.Canny(gray,50,150,apertureSize = 3)

		lines = cv.HoughLines(edges,1,np.pi/180,200)
		for i in lines:
			for rho,theta in i:
				a = np.cos(theta)
				b = np.sin(theta)
				x0 = a*rho
				y0 = b*rho
				x1 = int(x0 + 1000*(-b))
				y1 = int(y0 + 1000*(a))
				x2 = int(x0 - 1000*(-b))
				y2 = int(y0 - 1000*(a))
				cv.line(img,(x1,y1),(x2,y2),(0,0,255),1)

				cv.line(edges,(x1,y1),(x2,y2),(0,0,255),1)
		plt.imshow(img)
		# cv.imshow("Source1", gray)
		# plt.imshow(edges)
		plt.show()
		# plt.subplot(1,2,1),plt.imshow(gray)
		# plt.show()


		'''
		image = cv.imread(self.file_path, cv.IMREAD_GRAYSCALE)

		img = cv.imread(self.file_path, cv.COLOR_RGB2GRAY)
		img = imutils.resize(img, height = 800)

			for cnt in contours0:

				rect = cv2.minAreaRect(cnt) #
				box = cv2.boxPoints(rect)
				box = np.int0(box)
				if sca < cv2.contourArea(box) < AREA:
					sca = cv2.contourArea(box)
					ss = box

				center = (int(rect[0][0]), int(rect[0][1]))
				area = int(rect[1][0] * rect[1][1])


				#cv2.drawContours(img,[box],0,(255,0,0),2)

				edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
				edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))


				usedEdge = edge1
				if cv2.norm(edge2) > cv2.norm(edge1):
					usedEdge = edge2
				reference = (1, 0)

				angle = 180.0 / math.pi * math.acos((reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv2.norm(reference) * cv2.norm(usedEdge)))


				aa = abs(angle - sred_angle)
				if tt == 1 and aa > 70:
					print(aa)
					cv2.drawContours(img,[box],0,(255,0,0),2)
				if tt != 1:
					sred_angle += angle

			sred_angle = sred_angle / (len(contours0))





		cv2.imshow('contours', img)


		plot.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
		plot.show()

a = ImageProcessing('../dataFiles/origImage/2_.jpg')
a.upgradeImage()
a.detectLines()
