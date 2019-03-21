from keras.models import load_model
from lib.helpers import resize_to_fit
import numpy as np
import imutils
import cv2
import pickle
from imutils import paths


MODEL_FILENAME = '/usr/SmartLibrary/lib_captcha_model.hdf'
MODEL_LABELS_FILENAME = '/usr/SmartLibrary/lib_model_labels.dat'
CAPTCHA_IMAGE_FOLDER = '/usr/SmartLibrary/user/static/reservation_captchas'


def get_verify_via_model():
    # load
    with open(MODEL_LABELS_FILENAME, "rb") as f:
        lb = pickle.load(f)

    # load the trained neural network
    model = load_model(MODEL_FILENAME)

    captcha_image_files = list(paths.list_images(CAPTCHA_IMAGE_FOLDER))
    # captcha_image_files = np.random.choice(captcha_image_files, size=(10,), replace=False)

    # loop over the image paths
    for image_file in captcha_image_files:
        # load the image and convert it to Gray

        image = cv2.imread(image_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_REPLICATE)

        thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours = contours[0] if imutils.is_cv2() else contours[1]

        letter_image_regions = []

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if w / h > 1.25:
                half_width = int(w / 2)
                letter_image_regions.append((x, y, half_width, h))
                letter_image_regions.append((x + half_width, y, half_width, h))
            else:
                # This is a normal letter by itself
                letter_image_regions.append((x, y, w, h))

        if len(letter_image_regions) != 4:
            continue

        letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

        # hold our predicted letters
        output = cv2.merge([image] * 3)
        predictions = []

        for letter_bounding_box in letter_image_regions:
            x, y, w, h = letter_bounding_box

            letter_image = image[y - 2: y + h + 2, x - 2:x + w + 2]
            # 20 * 20 the same as the model img
            letter_image = resize_to_fit(letter_image, 20, 20)

            letter_image = np.expand_dims(letter_image, axis=2)
            letter_image = np.expand_dims(letter_image, axis=0)

            prediction = model.predict(letter_image)

            letter = lb.inverse_transform(prediction)[0]
            predictions.append(letter)

            cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
            cv2.putText(output, letter, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
        captcha_text = "".join(predictions)

        # if captcha_text == "":
        #     result = False
        # else:
        #     result = True

        # print("CAPTCHA text is {}".format(captcha_text))
        return captcha_text
