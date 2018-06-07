import os
import cv2
import dlib
import numpy as np

from wide_resnet import WideResNet
from keras.utils.data_utils import get_file

WEIGHT_FILE = "./model/age_and_gender.hdf5"

DEPTH = 16
WIDTH = 8

IMAGE_SIZE = 64

weight_file = get_file("age_and_gender.hdf5", origin='images', cache_subdir="model", cache_dir=os.path.dirname(os.path.abspath(__file__)))

detector = dlib.get_frontal_face_detector()

model = WideResNet(IMAGE_SIZE, DEPTH, WIDTH)()
model.load_weights(WEIGHT_FILE)


def prediction(image_path):
    input_image = cv2.imread(image_path)
    grayscale = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    img_height, img_weight = np.shape(grayscale)

    detected = detector(grayscale, 1)
    faces = np.empty((len(detected), IMAGE_SIZE, IMAGE_SIZE, 3))

    if len(detected) > 0:
        for i, d in enumerate(detected):
            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
            xw1 = max(int(x1 - 0.4 * w), 0)
            yw1 = max(int(y1 - 0.4 * h), 0)
            xw2 = min(int(x2 + 0.4 * w), img_weight - 1)
            yw2 = min(int(y2 + 0.4 * h), img_height - 1)
            cv2.rectangle(input_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            faces[i, :, :, :] = cv2.resize(input_image[yw1:yw2 + 1, xw1:xw2 + 1, :], (IMAGE_SIZE, IMAGE_SIZE))

        result = []

        results = model.predict(faces)
        predicted_genders = results[0]
        ages = np.arange(0, 101).reshape(101, 1)
        predicted_ages = results[1].dot(ages).flatten()

        for i, d in enumerate(detected):
            age, gender = predicted_ages[i], "F" if predicted_genders[i][0] > 0.5 else "M"

            result.append({'face{}'.format(i): [x1, y1, x2, y2],
                           'age': int(age),
                           'gender': gender})

    return result