
import matplotlib.pyplot as plt
import numpy as np
import csv
import math


from tkinter import * 
from PIL import Image,ImageDraw  #Pillow library
import scipy.ndimage as ndi

import astropy.units as u
import astropy.time
import astropy.coordinates

def rotmatrix(deg):
    theta = math.radians(deg)

    rotMatrix = np.array([[np.cos(theta), -np.sin(theta)], 
                            [np.sin(theta),  np.cos(theta)]])

    return rotMatrix

def rotate(x,y,rotmatrix):
    array = np.array([[x],[y]])

    print(array)
    print(rotmatrix)
    return rotmatrix.dot(array)


def createimg():


    img = Image.new("RGB",(width,height))

    draw = ImageDraw.Draw(img)

    draw.line((0, 0) + img.size, fill=128)
    draw.line((0, img.size[1], img.size[0], 0), fill=128)

    # write to stdout
    # img.save(sys.stdout, "PNG")

    return img