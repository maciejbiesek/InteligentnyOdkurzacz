import cv2
import numpy as np


class NNTrainData:
    def __init__(self, img, output):
        self.img = img
        self.height, self.width, self.depth = self.img.shape
        self.color = np.int_(img[self.height / 2, self.width / 2])
        self.output = output

    def getContours(self):
        for x in range(self.height):
            for y in range(self.width):
                if (self.img[x, y] == [29, 230, 181]).all():
                    self.img[x, y] = [255, 255, 255]
                elif (self.img[x, y] != [255, 255, 255]).any():
                    self.img[x, y] = [0, 0, 0]

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 1)  # get a bi-level (binary) image out of a grayscale image
        contours, h = cv2.findContours(thresh, 1, 2)

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            self.contours = len(approx)

    def prepareTrainData(self):
        self.getContours()
