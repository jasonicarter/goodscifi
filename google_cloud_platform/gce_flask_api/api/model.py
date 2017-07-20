import argparse

from keras.models import load_model
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input
import numpy as np
import tensorflow as tf

# TF Graph
# https://github.com/fchollet/keras/issues/2397
model = load_model('/opt/app/models/inception_dl.h5')
graph = tf.get_default_graph()

def predict(image_file):
    # Normalize image
    img = image.load_img(image_file, target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis=0)
    x = preprocess_input(x)

    global graph
    with graph.as_default():
        preds = model.predict(x)

    # Decode probability e.g. [[ 0.56786007  0.4321399 ]]
    label, probability = ('good', preds[0][0])

    # Return prediction
    return [{'label': label, 'probability': probability * 100.0}]


# if __name__ == '__main__':
#     a = argparse.ArgumentParser()
#     a.add_argument("--image", help="path to image")
#     args = a.parse_args()
#
#     if args.image is not None:
#       predictions = predict(args.image)
#
#     print(predictions)
