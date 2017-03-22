# -*- coding: utf-8 -*-
import sys
import os

from PyQt5 import QtGui, QtCore, QtWidgets
from config import LIB_DIR

def show_image():
    image_path = os.path.join(LIB_DIR, 'screenshot.png')

    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    pixmap = QtGui.QPixmap(image_path)
    pixmap.setDevicePixelRatio(2)

    screen = QtWidgets.QLabel()
    screen.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    screen.setPixmap(pixmap)
    screen.showFullScreen()

    sys.exit(app.exec_())


if __name__ == '__main__':
    show_image()
