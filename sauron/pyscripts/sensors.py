import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import Queue
import cv2
import imutils
import numpy as np
import pandas as pd
from sklearn import svm, metrics, model_selection, tree
from skimage import io, feature, filters, exposure, color
from skimage.feature import hog
import pickle

ObstaclePin1 = 3
ObstaclePin2 = 5

velocity = 0
sensor_dist = 6
camera_dist = 53
now1 = True
now2 = True
downtime1 = datetime.now()
downtime2 = datetime.now()
sleep = timedelta(microseconds=250000)
queue1 = Queue.Queue()
timer1 = Queue.Queue()
timer2 = Queue.Queue()

cap = cv2.VideoCapture(0)

def image_processing(image):
    img = image[0:-140,226:-160]
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
    im = cv2.cvtColor(img[y:h, x:w], cv2.COLOR_BGR2GRAY)
    im = cv2.resize(im, (400, 400))
    im = exposure.adjust_gamma(im, 2)
    kernel1 = np.ones((2, 2), np.uint8)
    gradient = cv2.morphologyEx(im, cv2.MORPH_GRADIENT, kernel1)
    return gradient

def convert_time(time1):
    sec_to_micr = time1.seconds * 1000000
    final_micro = sec_to_micr + time1.microseconds
    return final_micro

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(ObstaclePin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ObstaclePin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    global downtime1
    global downtime2

    while True:
        if (datetime.now() > downtime1):
            now1 = True

        if (1 == GPIO.input(ObstaclePin1)) and now1:
                print "Obstacle First!"
                now1 = False
                timer1.put(datetime.now())
                downtime1 = datetime.now() + sleep


        if (datetime.now() > downtime2):
            now2 = True

        if (1 == GPIO.input(ObstaclePin2)) and now2:
            print "Obstacle Second!"
            now2 = False
            timer2.put(datetime.now())
            downtime2 = datetime.now() + sleep
            velocity = (sensor_dist/(convert_time(timer2.get()-timer1.get())))
            time_to = datetime.now() + timedelta(microseconds=(camera_dist/velocity))
            queue1.put(time_to)

        if (queue1.qsize() > 0):
            if(queue1.queue[0] < datetime.now()):
                queue1.get()
                ret, frame = cap.read()
                frame = frame
                pd = extract_image_features(frame)



def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
