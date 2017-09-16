"""Analyzer

Analyzer module for setting menu bar setup for OSX
"""
__author__ = 'ales lerch'

import os
import cv2
import numpy

def check_image_color(image):
    """Returns string containing 'ligh' or 'dark' that tells if image is for day or night,
    Y -- converting to gray to detect if it's really dark or light"""

    def check_color(i,j,k):
        """ Function used only for DEBUGGING"""
        from PIL import Image
        #img.show()
        image = Image.new("RGB", (200, 200), (int(Y),int(Y),int(Y)))
        image.show()
        image = Image.new("RGB", (200, 200), (int(i),int(j),int(k)))
        image.show()

    if not os.path.isfile(image):
        return "Image not found"

    try:
        img = cv2.imread(image)
        average_color_per_row = numpy.average(img, axis=0)
        average_color = numpy.average(average_color_per_row, axis=0)
        B, G, R = tuple(average_color)
        height, width = img.shape[:2]
        Y = (0.299*R+0.587*G+0.114*B)
    except:
        return "Error with image"

    if Y < 72.0:
        _type = "dark"
    elif Y >= 73.0 and Y <= 108.0:
        _type = "evening"
    else:
        _type = "light"

    return _type
