import cv2 as cv
import numpy as np
import imutils
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
		cv.imshow("Source", img)
		cv.imshow("Source1", gray)
		plt.subplot(1,2,1),plt.imshow(gray)
		plt.show()
		

		'''
		image = cv.imread(self.file_path, cv.IMREAD_GRAYSCALE)
		
		img = cv.imread(self.file_path, cv.COLOR_RGB2GRAY)
		img = imutils.resize(img, height = 800)

		image = imutils.resize(image, height = 800)

		
		image = np.array(image, dtype=np.uint8)
		
		
		gray = cv.adaptiveThreshold(image,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
					cv.THRESH_BINARY,11,3)
					
		#gray = cv.GaussianBlur(image, (5, 5 ), 0)
		
		edged = cv.Canny( image, 75, 200, None,3)
		
		src = img
		dst = edged
		cdst = img
		cdstP = np.copy(cdst)
		
		#	*************
		lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
		
		
		
		if lines is not None:
				for i in range(0, len(lines)):
					rho = lines[i][0][0]
					theta = lines[i][0][1]
					a = math.cos(theta)
					b = math.sin(theta)
					x0 = a * rho
					y0 = b * rho
					pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
					pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
					cv.line(cdst, pt1, pt2, (0,0,255), 1, cv.LINE_AA)
    
    
		linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
		
		sav = []
		class linetest():
			def __init__(self,temp,i):
				self.i = i
				self.temp = temp
			def F(pp):
				return pp.i	
		def F(pp):
			return pp.temp
				
		for i in linesP:
			temp = math.sqrt((i[0][0]-i[0][2])**2 + (i[0][1]-i[0][3])**2)
			sav.append(linetest(temp,i))

		sav = sorted(sav, key=F , reverse=True)

		if linesP is not None:
			for i in range(0,len(sav)):
				l = sav[i].F()[0]
				cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
		
		cv.imshow("Source", src)
		cv.imshow("Standard Hough", cdst)
		cv.imshow("Probabilistic", cdstP)
		'''
		
		
		'''
		plt.subplot(1,2,1),plt.imshow(img)
		plt.subplot(1,2,2),plt.imshow(edged)
		plt.show()
		'''
		
		
a = ImageProcessing('../dataFiles/origImage/2.jpg')
a.upgradeImage()
a.detectLines()


