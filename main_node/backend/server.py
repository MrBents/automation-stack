from flask import Flask, render_template, request
from flask_cors import CORS
from IMGPreProcessing.IMGPreprocessing import IMGPreprocessing
import cv2
import json
import numpy as np
import PIL
from PIL import Image
import os
from PIL import Image
from io import StringIO
import datetime

gb_array = []
crop_img_path = '/Users/gabrielgoldszmidt/Desktop/Quant/Kaggle/data_factory/automation-stack/sauron/public/CROPPED_IMGS/'


def get_percentages(tag):
    global gb_array
    gb_array.append(tag)
    good_count = gb_array.count('good')
    bad_count = gb_array.count('bad')
    total = good_count + bad_count
    good_perc = np.round((good_count/total) * 100,2)
    bad_perc = np.round((bad_count/total) * 100,2)
    if (len(gb_array) > 100):
        gb_array = gb_array[0:100]
    return good_perc, bad_perc

def convert_time(time1):
    sec = time1.seconds
    micro_to_sec =  time1.microseconds * (10**-6)
    final_sec = np.round(sec + micro_to_sec,4)
    return final_sec


def ImgFromBuffer(buf):
    im = Image.open(StringIO(buf))
    # im.thumbnail(size, Image.ANTIALIAS)
    return im

app = Flask(__name__)
# app.run(host='127.0.0.1', port=5008, debug=True)
CORS(app)
preprocessing = IMGPreprocessing()


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def send_img():
    if request.method == 'POST':
        # print(request.data.decode("utf-8"))
        data = request.data;
        path = str(json.loads(data.decode('utf-8'))["path"])
        new_path = str(path[94:])
        img = cv2.imread(root_dir() + '/' + new_path,-1)
        # print(img)
        # oldtime = datetime.datetime.now()
        c_img, vector = preprocessing.preprocess(img)
        tag = preprocessing.classify_img(vector)
        #errortag = preprocessing.classify_img_byerror(vector)
        errortag = '0'
        crop_path = crop_img_path + new_path[16:-4] + '_'+ tag[0] + '_' + errortag[0][:-5] + '.jpg'
        cv2.imwrite(crop_path,c_img)
        good_p , bad_p = get_percentages(tag[0])
        # timestamp = datetime.datetime.now()
        # print(crop_path)
        print(tag)
        print(errortag)
        # print(datetime.datetime.utcnow())
        # print(new_path[16:-4])
        # print(root_dir())
        # print (tag[0] + new_path)
        arr = {'name' : new_path[16:-4],'tag': tag[0]}
        # cv2.imwrite('laputa.jpg', np.asarray(json.loads(request.data.decode("utf-8"))['data']['data']))
        # print(ImgFromBuffer(str(json.loads(request.data.decode("utf-8"))['data'])))
        f_str = new_path[16:-4] + '_' + tag[0] + '_' + errortag[0][:-5] + '_' + str(good_p) + '_' + str(bad_p)
        # img = (np.asarray(json.loads(request.data.decode("utf-8"))['data']['data']))
        # print(img)
        # img = cv2.imdecode(request.data, 1)
        # cv2.imwrite('jose.jpg', img)
        # print(request.files.copy().to_dict())
        # tag = preprocessing.classify_img(img)
        #arreturn tag
        return f_str
        #
