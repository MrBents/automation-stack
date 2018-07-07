#!/usr/bin/env python

##############
# Your name: Gabriel GoldszmidtS
##############

import re
import numpy as np
import pandas as pd
import cv2
import scipy.ndimage as ndi
from skimage import color, exposure, feature, filters, io
from skimage.feature import hog, daisy
from skimage.measure import block_reduce
from sklearn import metrics, model_selection, svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import pickle


class ImageClassifier:

    def __init__(self):
        self.classifer = None

    def imread_convert(self, f):
        return io.imread(f).astype(np.uint8)

    def load_data_from_folder(self, dir):
        # read all images into an image collection
        ic = io.ImageCollection(dir + "*.JPEG", load_func=self.imread_convert)

        # create one large array of image data
        data = io.concatenate_images(ic)

        # _, directoriesg, filesgood = next(os.walk('./rawgood'))
        # _, directoriesb, filesgood = next(os.walk('./rawgood'))
        # extract labels from image names
        labels = np.array(ic.files)
        for i, f in enumerate(labels):
            # m = re.search("_", f)
            m = f.split('_')
            # labels[i] = f[len(dir):m.start()]
            #print(m[2])
            labels[i] = m[2]

        return(data, labels)

 

    def extract_image_features(self, data):
        # Please do not modify the header above

        feature_data = []
        for i in range(data.shape[0]):
            # img = block_reduce(data[i], (3,3,3))
            # print (img.shape)
            print(i)

            img = data[i]

            
 #           img = img[100:-200,250:-250]
            

            # img = filters.gaussian(img, sigma=0.1)
            
            img = exposure.adjust_gamma(img, 2)
 #           img = exposure.rescale_intensity(img)
 #           img = color.rgb2gray(img)

            kernel1 = np.ones((2, 2), np.uint8)
            gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel1)
            gradient = gradient.flatten()
            # can = cv2.Canny(gradient, 100, 300)
            # grad = cv2.morphologyEx(can, cv2.MORPH_DILATE, kernel1, iterations=15)

            # Acc ~96% only with exposure(6,6)
 #           fd = hog(img, orientations= 18, pixels_per_cell=(36, 36), cells_per_block=(6,6), block_norm='L2-Hys', feature_vector=True)
    #          fd = daisy(img)
 #           fd = hog(img, orientations=10, pixels_per_cell=(12, 12), cells_per_block=(4, 4), block_norm='L2-Hys', feature_vector=True)
 #           fd = hog(gradient, orientations=18, pixels_per_cell=(12, 12), cells_per_block=(4, 4), block_norm='L2-Hys', feature_vector=True)
            
            feature_data.append(gradient)
        ########################
        # YOUR CODE HERE
        ########################

        # Please do not modify the return type below
        return(feature_data)

    def train_classifier(self, train_data, train_labels):
        # Please do not modify the header above
        x = [fd for fd in train_data]
        y = [lbl for lbl in train_labels]
        # train model and save the trained model to self.classifier
        model = svm.LinearSVC()
        # model = MLPClassifier(solver='lbfgs', alpha=1e-5,
        #                       hidden_layer_sizes=(256, 256), random_state=1)
        model.fit(x, y)
        self.classifier = model
        ########################
        # YOUR CODE HERE
        ########################

    def cross_validation(self, train_data, train_labels):
        # Please do not modify the header above
        x = [fd for fd in train_data]
        y = [lbl for lbl in train_labels]
        model = svm.LinearSVC()
        scores = cross_val_score(model, x, y, cv=5)
        self.scores = scores
        ########################
        # YOUR CODE HERE
        ########################

    def predict_labels(self, data):
        # Please do not modify the header

        # predict labels of test data using trained model in self.classifier
        # the code below expects output to be stored in predicted_labels

        ########################
        # YOUR CODE HERE
        ########################
        predicted_labels = []
        for pd in data:
            predicted_labels.append(self.classifier.predict([pd]))
        # Please do not modify the return type below
        return predicted_labels


def main():

    img_clf = ImageClassifier()

    # load images
    # (train_raw, train_labels) = img_clf.load_data_from_folder('./train/')
    # (test_raw, test_labels) = img_clf.load_data_from_folder('./test/')
    print("Fetching images...")
    (all_raw, all_labels) = img_clf.load_data_from_folder('./bothxx/')
    
    print("Extracting Image Features...")
    all_raw1 = img_clf.extract_image_features(all_raw)
    
    allist = []
    for ar, al in zip(all_raw1, all_labels):
        allist.append((ar, al))
        #print("Extracting Image Features...")
        #imgs_ftrs_data = img_clf.extract_image_features(allist)
        
        
    for i in range(1):
        print("Spltting data sets...")
        train_raw, test_raw = train, test = model_selection.train_test_split(
            allist , test_size=0.25)
        # convert images into features

        print("Formating data...")
        train_data, train_labels = np.array([i for i, _ in train_raw]), np.array([
            i for _, i in train_raw])
        test_data, test_labels = np.array([i for i, _ in test_raw]), np.array([
            i for _, i in test_raw])
        
        
        print("Training Classifier")
        img_clf.train_classifier(train_data, train_labels)
        predicted_labels = img_clf.predict_labels(train_data)


        print("Cross Validation Test")
        img_clf.cross_validation(train_data, train_labels)
        print(img_clf.scores)
        print("Accuracy: %0.5f (+/- %0.5f)" % (img_clf.scores.mean(), img_clf.scores.std() * 2))

        print("\n\n\nTraining results")
        print("=============================")
        print("Confusion Matrix:\n", metrics.confusion_matrix(train_labels, predicted_labels))
        tn, fp, fn, tp = metrics.confusion_matrix(train_labels, predicted_labels).ravel()
        print("False Positives: " + str(fp))
        print("False Negatives: " + str(fn))
        print("Accuracy: ", metrics.accuracy_score(train_labels, predicted_labels))
        print("F1 score: ", metrics.f1_score(
            train_labels, predicted_labels, average='micro'))

        # test model
        predicted_labels = img_clf.predict_labels(test_data)
        print("\nTesting results")
        print("=============================")
        print("Confusion Matrix:\n", metrics.confusion_matrix(
            test_labels, predicted_labels))
        tn, fp, fn, tp = metrics.confusion_matrix(test_labels, predicted_labels).ravel()
        print("False Positives: " + str(fp))
        print("False Negatives: " + str(fn))
        print("Accuracy: ", metrics.accuracy_score(test_labels, predicted_labels))
        print("F1 score: ", metrics.f1_score(
            test_labels, predicted_labels, average='micro'))

        with open(str(metrics.accuracy_score(test_labels, predicted_labels)) + '_ACC.pickle', 'wb') as handle:
            pickle.dump(img_clf, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()


if __name__ == "__main__":
    main()
