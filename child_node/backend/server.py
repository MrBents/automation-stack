from flask import Flask, render_template
from flask_cors import CORS
from sensors_app.sensors import loopit

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
  return render_template('index.html')

@app.route('/image')
def send_img():
    loopit()
    return "200 OK"
    # return "/static/imgs/IMG_12_good_0_L.JPEG"
