import requests
import time


url = 'http://localhost:3000/image'
filpath = ['IMG_16_good_0.JPEG', './IMG_69_good_0.JPEG', './IMG_1135_bad_1.JPEG', './IMG_2635_bad_4.JPEG', './IMG_3215_bad_2.JPEG']
counter = 0
while True:
    print open(filpath[counter%5], 'rb')
    with open(filpath[counter%5], 'rb') as fil:
        files = {'media': fil}

        requests.post(url, files=files)
        counter += 1
        time.sleep(1)
