import cv2
from matplotlib import pyplot as plot
import numpy as  np
import math

class Processing():
	def __init__(self, file):
		self.file = file
		self.image = cv2.imread(self.file)
	def search_contours(self):
		self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		self.image = cv2.GaussianBlur(self.image, (5, 5), 0)
		self.image = cv2.Canny(self.image, 20, 50)
		img = self.image.copy()
		
		kernel = np.ones((5,5),np.uint8)
		
		dilation = cv2.dilate(img.copy(),kernel,iterations = 3)
		gradient = cv2.morphologyEx(dilation, cv2.MORPH_GRADIENT, kernel)
		
		
		edges = cv2.Canny(gradient,20,50)

		lines = cv2.HoughLines(edges,1,np.pi/180,200)
		
		contours0, hierarchy = cv2.findContours( gradient.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		
		sca = 0
		height, width = img.shape
		AREA =  height* width * 0.9
		sred_angle = 0
		for tt in range(2):

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

	def show_image(self):
		plot.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
		plot.show()
test = Processing('../dataFiles/origImage/7.jpg')
test.search_contours()
test.show_image()
