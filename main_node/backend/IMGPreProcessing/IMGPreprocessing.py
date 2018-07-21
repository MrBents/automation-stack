import cv2
import imutils
import numpy as np
import pandas as pd
from sklearn import svm, metrics, model_selection, tree
from skimage import io, feature, filters, exposure, color
from skimage.feature import hog
import pickle
import os

# class Classify():
#     def __init__():
#
#
# class Meta_Predictor():
#     def __init__(self):
#         self.clfs = {
#         0 : l1
#         1 : l2
#         }
#
#     def l1(self):
#         pass
#     def l1(self):
#         pass
#     def l1(self):
#         pass

class IMGPreprocessing():
    def __init__(self):
        os.system('pwd')
        with open('backend/static/new_attempt.pickle', 'rb') as filamento:
            self.img_clf = pickle.load(filamento)

        with open('backend/static/byerror_sirve.pickle', 'rb') as picalish:
            self.img_clf_byerr = pickle.load(picalish)


    def preprocess(self, data):
        img = data
        # img = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img,(640,480))
        img = img[0:140,226:-160]
        kernel1 = np.ones((2, 2), np.uint8)
        gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel1)
        can = cv2.Canny(gradient, 100, 300)
        grad = cv2.morphologyEx(can, cv2.MORPH_DILATE, kernel1, iterations=15)
        cnts = cv2.findContours(grad, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = cnts[0] if imutils.is_cv2() else cnts[1]

        c = max(cnts1, key=cv2.contourArea)
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        y = cY - 200
        h = cY + 200
        x = cX - 200
        w = cX + 200
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        #im = cv2.cvtColor(img[y:h, x:w], cv2.COLOR_BGR2GRAY)

        iii = img[y:h, x:w]
        cv2.imwrite('segal.jpg',im)
        imagen = cv2.resize(im, (400, 400))
        img = exposure.adjust_gamma(im, 2)
        kernel1 = np.ones((2, 2), np.uint8)
        gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel1)
        fd = gradient.flatten()
        return iii , fd

    def classify_img(self, vector):
        # vector = self.preprocess(image)
        return (self.img_clf.predict([vector]))

    def classify_img_byerror(self, vector):
            # vector = self.preprocess(image)
        return (self.img_clf_byerr.predict([vector]))
