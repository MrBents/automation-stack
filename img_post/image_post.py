import requests
import time
from datetime import datetime


url = 'http://localhost:3000/image'
filpath = [ './IMG_194_good_0.JPEG' ,'./IMG_2871_bad_3.JPEG', './IMG_3634_bad_3.JPEG', './IMG_3633_bad_3.JPEG', './IMG_2317_bad_4.JPEG']
counter = 0



while True:
    #print open(filpath[counter%5], 'rb')
    with open(filpath[counter%5], 'rb') as fil:
        files = {'image' : fil}
 #       print("gobriel")
 #       print(filpath[0])
        print (files)
        now = datetime.now()
        response = requests.post(url, files=files)
        after = datetime.now()

        print(after - now)
 #       requests.post(url, params=payload, headers=headers)

        counter += 1
        time.sleep(5)
