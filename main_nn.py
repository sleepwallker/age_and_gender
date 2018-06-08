import cv2
import dlib
import numpy

from wide_resnet import WideResNet

WEIGHT_FILE = "./model/age_and_gender.hdf5"

WIDTH = 8
DEPTH = 16

IMAGE_SIZE = 64

detector = dlib.get_frontal_face_detector()

model = WideResNet(IMAGE_SIZE, DEPTH, WIDTH)()
model.load_weights(WEIGHT_FILE)


def prediction(image_path):
    image = cv2.imread(image_path)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img_height, img_weight = numpy.shape(grayscale)

    detected = detector(grayscale, 1)
    faces = numpy.empty((len(detected), IMAGE_SIZE, IMAGE_SIZE, 3))

    result = []
    face_result = []

    for i, d in enumerate(detected):
        x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
        face_result.append([int(x1), int(y1), int(x2), int(y2)])

        xw1 = max(int(x1 - 0.4 * w), 0)
        yw1 = max(int(y1 - 0.4 * h), 0)
        xw2 = min(int(x2 + 0.4 * w), img_weight - 1)
        yw2 = min(int(y2 + 0.4 * h), img_height - 1)

        faces[i, :, :, :] = cv2.resize(image[yw1:yw2 + 1, xw1:xw2 + 1, :], (IMAGE_SIZE, IMAGE_SIZE))

    results = model.predict(faces)
    predicted_genders = results[0]
    ages = numpy.arange(0, 101).reshape(101, 1)
    predicted_ages = results[1].dot(ages).flatten()

    for i, d in enumerate(detected):
        age, gender = predicted_ages[i], "Female" if predicted_genders[i][0] > 0.5 else "Male"

        result.append({'face': face_result[i],
                       'age': int(age),
                       'gender': gender})

    return result