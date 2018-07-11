"""Analyzer

Analyzer module for setting menu bar setup for OSX
"""
__author__ = "ales lerch"

import os
import cv2
import numpy
from PIL import Image


def check_image_color(image):
    """Returns string containing 'ligh' or 'dark' that tells if image is for day or night,
    Y -- converting to gray to detect if it's really dark or light"""

    def check_color(i, j, k):
        """ Function used only for DEBUGGING"""
        img.show()
        image = Image.new("RGB", (200, 200), (int(Y), int(Y), int(Y)))
        image.show()
        image = Image.new("RGB", (200, 200), (int(i), int(j), int(k)))
        image.show()

    if not os.path.isfile(image):
        return "Image not found"

    def calculate_bgr(data):
        average_color_per_row = numpy.average(data, axis=0)
        average_color = numpy.average(average_color_per_row, axis=0)
        return tuple(average_color)

    def calculate_y(r, g, b):
        alpha = 0.299
        betta = 0.587
        gamma = 0.114
        return alpha * r + betta * g + gamma * b

    # split the image for four squares calucate averate pixel for them and take higest value
    # blure image and save to /Library/Caches as com.apple.desktop.admin.png
    # in case using blur tool --> blur = cv2.blur(img,(5,5))
    try:
        img_cv_data = cv2.imread(image)
        B, G, R = calculate_bgr(img_cv_data)
        Y = calculate_y(B, G, R)
        height, width = img_cv_data.shape[:2]
    except Exception as err:
        print(f"[ERROR] {err} with image: {image}")
        return "Error parsing image"

    # image detection
    if Y < 72.0:
        _type = "dark"
    elif Y >= 73.0 and Y <= 108.0:
        _type = "evening"
    else:
        _type = "light"

    return _type
