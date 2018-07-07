from flask import Flask, render_template, request
from flask_cors import CORS
from IMGPreProcessing.IMGPreprocessing import IMGPreprocessing
import cv2
import json


app = Flask(__name__)
# app.run(host='127.0.0.1', port=5008, debug=True)
CORS(app)
preprocessing = IMGPreprocessing()

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def send_img():
    if request.method == 'POST':
        print('ggg')

        print(json.loads(request.data.decode("utf-8")).data)
        # img = cv2.imdecode(request.data, 1)
        # cv2.imwrite('jose.jpg', img)
        # print(request.files.copy().to_dict())
        # tag = preprocessing.classify_img(request.files.image)
        #arreturn tag
        return "/static/imgs/IMG_12_good_0_L.JPEG"
