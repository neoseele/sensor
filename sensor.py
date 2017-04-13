# -*- coding:utf-8 -*-

import os
import cv2
import base64
import json
import numpy as np
import io
import requests
import subprocess

from PIL import Image
from pyfiglet import figlet_format

from show import show_image
from config import CASCADE_PATH, SERVICE_URL, IMAGE_SIZE
from train import Model

def greetings():
    print()
    print(figlet_format('boss sensor', font='4max'))

def resize_with_pad(image, height=IMAGE_SIZE, width=IMAGE_SIZE):

    def get_padding_size(image):
        h, w, _ = image.shape
        longest_edge = max(h, w)
        top, bottom, left, right = (0, 0, 0, 0)
        if h < longest_edge:
            dh = longest_edge - h
            top = dh // 2
            bottom = dh - top
        elif w < longest_edge:
            dw = longest_edge - w
            left = dw // 2
            right = dw - left
        else:
            pass
        return top, bottom, left, right

    top, bottom, left, right = get_padding_size(image)
    BLACK = [0, 0, 0]
    constant = cv2.copyMakeBorder(image, top , bottom, left, right,
        cv2.BORDER_CONSTANT, value=BLACK)
    resized_image = cv2.resize(constant, (height, width))

    return resized_image

def run():
    # model = Model()
    # model.load()

    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()

        cascade = cv2.CascadeClassifier(CASCADE_PATH)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) > 0:
            print("Found {0} faces!".format(len(faces)))

            for (x, y, w, h) in faces:
                face = frame[y: y+h, x: x+w]
                face = resize_with_pad(face)

                img_stream = io.BytesIO()
                pil = Image.fromarray(face)
                pil.save(img_stream,'JPEG')

                # file_path = os.path.join('faces', 'test.jpg')
                # cv2.imwrite(file_path, face)
                # img_code = subprocess.run(['base64', file_path], stdout=subprocess.PIPE)
                # img_code.stdout

                payload = {'data':
                    base64.b64encode(img_stream.getvalue()).decode('utf-8').rstrip()}
                # payload = {'data': img_code.stdout.decode("utf-8").rstrip()}
                # print(payload)

                try:
                    r = requests.post(SERVICE_URL, json=payload)
                    print(r.json())

                    if r.json()['prediction'] == 'boss':
                        print('boss is approaching!')

                        # file_path = os.path.join('faces', 'test.jpg')
                        # cv2.imwrite(file_path, face)
                        # print(payload)
                        show_image()

                except Exception:
                    pass
                # result = model.predict(face)
                # if result == 0:
                #     print('Boss is approaching')


        # wait for a second
        k = cv2.waitKey(200)
        # exit when esc is pressed
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    greetings()
    run()
