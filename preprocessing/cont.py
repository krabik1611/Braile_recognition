import cv2 as cv
from matplotlib import pyplot as plot
class Processing():
    def __init__(self, file):
        self.file = file
        self.image = cv.imread(self.file)
    def search_contours(self):
        self.image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        self.image = cv.GaussianBlur(self.image, (5, 5), 0)
        self.image = cv.Canny(self.image, 20, 50)
    def show_image(self):
        plot.imshow(cv.cvtColor(self.image, cv.COLOR_BGR2RGB))
        plot.show()
test = Processing('../dataFiles/origImage/2.jpg')
test.search_contours()
test.show_image()
