from flask import Flask, render_template, request
from flask_cors import CORS
from imageio import imread
from scipy.misc import imresize
from PIL import Image
from keras.preprocessing import image
import sys
import os
import re
import base64

from keras.models import load_model
import tensorflow as tf
import numpy as np

app = Flask(__name__)
CORS(app, intercept_exceptions=False)
tf.debugging.set_log_device_placement(True)

# Path to our saved model
sys.path.append(os.path.abspath("./cnn-mnist"))
#Initialize some global variables


global model, graph

@app.route('/')
def index():
    return render_template("index.html")
    
def convertImage(imgData1):
  imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
  with open('output.png', 'wb') as output:
    output.write(base64.b64decode(imgstr))

def loadImage(filename):
        import cv2
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        img_rows = img_cols = 28
       # img = image.load_img(filename,grayscale=True)
        img = imresize(img, (28, 28))
        img = image.img_to_array(img)
        img = img / 255
        # Reshape from (28,28) to (1,28,28,1) : 1 sample, 28x28 pixels, 1 channel (B/W)
        img = np.expand_dims(img, axis=0)
        img = np.expand_dims(img, axis=0)
        img = np.reshape(img, (1,img_cols,img_rows,1))
        print("Image loaded")
        return np.array(img)
    
@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    print("Before graph")
    
    graph = tf.Graph()
    with graph.as_default():
        model = load_model('./cnn-mnist')
        print("model loaded")
        imgData = request.get_data()
        convertImage(imgData)
        img = loadImage("output.png")
        print("image complete")
        classes = model.predict(img)
        predicted = np.argmax(classes)
        print("image  predicted")
        print(predicted)
        return str(predicted)
    
    print("after graph")




    return str(response[0])
    print("after second return")
    
    print(imgData)
    
    #return "leo"

if __name__ == "__main__":
# run the app locally on the given port
    app.run(host='0.0.0.0', port=5000)