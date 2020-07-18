import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


class ImageProcessing():
	'''class for image processing'''
	def __init__(self,file_path):
		'''define file path and initialize proprities'''
		self.file_path = file_path
		self.readImage() # start processing image after create object
		self.upgradeImage()

	def readImage(self):
		'''read image'''
		self.oImage = cv.imread(self.file_path, cv.IMREAD_GRAYSCALE) #read image
		self.oImage = cv.GaussianBlur(self.oImage, (5, 5), 0) # delete trash

	def upgradeImage(self):
		'''preprocessing image'''
		image = cv.GaussianBlur(self.oImage, (5,5), 0)
		image = cv.Canny(image,20,50)

		kernel = np.ones((5,5),np.uint8)

		dilation = cv.dilate(image.copy(),kernel,iterations=3)
		self.Image = cv.morphologyEx(dilation, cv.MORPH_GRADIENT, kernel) # gradient
		# self.Image = cv.Canny(gradient,20,50) # maybe delete!!!!
		return image

	def getContours(self):
		contours0, hierarchy = cv.findContours( self.Image.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
		sredY= 0
		count = 0
		contours1 = []
		y,x = self.Image.shape
		for n in range(2):
			for cont in contours0:
				rect = cv.minAreaRect(cont)
				box = cv.boxPoints(rect)
				(x0,y0,x1,y1) = cv.boundingRect(box) #find two dot for rectagle
				'''
				(x0,y1)----0
				|          |
				0-----(x1,y1)
				'''
				if n==0:
					sredY+= y1/len(contours0)
				else:
					if sredY < y1:
						if x0<0:
							x0=0
						if x1<0:
							x1=0
						if y0<0:
							y0=0
						if y1<0:
							y1=0
						contours1.append([x0,y0,x1,y1])
		self.contours = contours1
		# print(len(contours1))
		return contours1

	def getCanny(self):

		img = self.oImage
		img = cv.GaussianBlur(img, (5, 5), 0)
		img = cv.Canny(img,20,70)

		kernel = np.ones((5,5),np.uint8)
		edges = cv.dilate(img,kernel,iterations = 1)
		closing = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel,iterations=2)
		image = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)

		self.Image = image
		# img = cv.cvtColor(closing,cv.COLOR_BGR2RGB)
		# plt.imshow(img)
		# plt.show()

	def getLine(self):
		img = self.oImage
		y,x = img.shape # image size
		contours = self.contours # get contours
		lines = []
		contours.sort(key=lambda i: i[1]) # cort for better find line coordinates
		min,max = 0,0
		for i in range(len(contours)-1):
			'''find up and down border string of max or min value
                max for down and min for up'''
			if contours[i+1][1] -contours[i][1] < 20:
				'''find count line and it value'''
				if min < contours[i][1] :
					min = contours[i][1] # find up line border
			else:
				'''find average value'''
				max = contours[i-1][3] + contours[i][1] # find down line border
				lines.append([min-5,max+5])
		images = [] # list of slice string
		for line in lines:
			'''draw up and down line in every string'''
			y0,y1 = line # get up and down border
            # cv.line(img,(0,y0),(x,y0),(0,0,0),2)
            # cv.line(img,(0,y1),(x,y1),(0,0,0),2)
			images.append(img[y0:y1,0:x])
		self.Lines = images
		return images
	def drawCont(self):
		img = self.Image
		contours = self.contours
		# print(len(contours))
		for cont in contours:
			'''func for draw all rectangle'''
			x0,y0,x1,y1 = cont
			x1+=x0
			y1+=y0
			cv.rectangle(img, (x0,y0), (x1,y1), (43, 43, 125), 3)

		return cv.cvtColor(img,cv.COLOR_BGR2RGB)

	def visualizationString(self):
		'''func for show result'''
		lines = self.Lines
		row = len(lines)//2 + 1
		column =2
		lenght = len(lines)
		for n in range(1,lenght):
			plt.subplot(row,column,n),plt.imshow(cv.cvtColor(lines[n],cv.COLOR_BGR2RGB))
			plt.title(n), plt.xticks([]),plt.yticks([])
		plt.show()
obj = ImageProcessing('../dataFiles/origImage/perfect2.jpg')
obj.getCanny()
obj.getContours()
obj.getLine()
obj.visualizationString()
img = obj.drawCont()
plt.imshow(img)
plt.show()
