# -*- coding:utf-8 -*-
import os
import cv2
import datetime
from pyfiglet import figlet_format
from config import CASCADE_PATH, NUM_OF_SELFIES

def greetings():
    print()
    print(figlet_format('Selfie Cam', font='4max'))
    print()
    print("* The Cam will take %d selfie of yours" % NUM_OF_SELFIES)
    print("* Your selfies will be used to feed a robot overlord")
    print("* Don't smile!")
    print()
    input("[Press any key to start ...]")


def create_dir():
    faces_dir = 'faces'

    if not os.path.exists(faces_dir):
        os.makedirs(faces_dir)


def run():
    create_dir()
    cap = cv2.VideoCapture(0)

    count = NUM_OF_SELFIES
    # stop when count <= 0
    while count > 0:
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
                cv2.rectangle(frame, (x-2, y-2), (x+w+2, y+h+2), (0, 255, 0), 2)
                face = frame[y: y+h, x: x+w]

                cv2.imshow("face found", frame)
                # cv2.waitKey(0)

                # cv2.imshow('face',face)
                file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")
                file_path = os.path.join('faces', file_name+'.jpg')

                print('writing ['+file_path+']')
                cv2.imwrite(file_path, face)

        k = cv2.waitKey(100)
        if k == 27:
            break

        count -= 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    greetings()
    run()
