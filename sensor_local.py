# -*- coding:utf-8 -*-

import cv2
import base64
import json
import numpy as np
import io
import requests

from PIL import Image
from pyfiglet import figlet_format

from show import show_image
from config import CASCADE_PATH
from train import Model

def greetings():
    print()
    print(figlet_format('boss sensor l', font='4max'))

def run():
    model = Model()
    model.load()

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
                # cv2.imshow('face', face)
                # cv2.waitKey(500)

                result = model.predict(face)
                if result == 0:
                    print('Boss is approaching')
                    # show_image()
                    cv2.imshow('face', face)
                    cv2.waitKey(500)

        # wait for a second
        k = cv2.waitKey(500)
        # exit when esc is pressed
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    greetings()
    run()
