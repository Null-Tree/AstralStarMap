

import random
import json
import matplotlib.pyplot as plt
import numpy as np
import csv
import sqlite3
import math
import sys

from tkinter import * 
from PIL import Image,ImageDraw, ImageFont #Pillow library
import scipy.ndimage as ndi

import astropy.units as u
import astropy.time
import astropy.coordinates


###############################################

from dataclasses import dataclass

bgcolor = (0,0,0)


#CONFIG
sizepower=14 #size power for dimensions of expor timage #normal 14 for 16k

width=2000
height=2000



###############################################



star_img = Image.open("stargraphic.png")


star_radius = 128


def createimg():
    global bgcolor
    canvas:Image = Image.new(mode="RGB",size=(width,height), color=bgcolor )
    return canvas



def place_star(canvas:Image,star_img:Image,x,y,r):

    top_left_cords  = (x-r,y-r)
    
    star_img = star_img.resize((2*r,2*r))

    canvas.paste(star_img, top_left_cords ,star_img)


# kelvin_table = {
#     1000: (255,56,0),
#     1500: (255,109,0),
#     2000: (255,137,18),
#     2500: (255,161,72),
#     3000: (255,180,107),
#     3500: (255,196,137),
#     4000: (255,209,163),
#     4500: (255,219,186),
#     5000: (255,228,206),
#     5500: (255,236,224),
#     6000: (255,243,239),
#     6500: (255,249,253),
#     7000: (245,243,255),
#     7500: (235,238,255),
#     8000: (227,233,255),
#     8500: (220,229,255),
#     9000: (214,225,255),
#     9500: (208,222,255),
#     10000: (204,219,255)}


# def convert_temp(image, temp):
#     r, g, b = kelvin_table[temp]
#     matrix = ( r / 255.0, 0.0, 0.0, 0.0,
#                0.0, g / 255.0, 0.0, 0.0,
#                0.0, 0.0, b / 255.0, 0.0 )
#     return image.convert('RGB', matrix)


from PIL import ImageOps
def tint_img(src:Image, color="#FFFFFF"):
    src.load()
    # extract alpha transparency
    r, g, b, alpha = src.split()
    # extract greyscale
    gray = ImageOps.grayscale(src)
    # color by input
    result = ImageOps.colorize(gray, (0, 0, 0, 0), color) 
    # apply transparency
    result.putalpha(alpha)
    return result




def main():
    canvas:Image=createimg()

    print(type(canvas))
    print(type(star_img))
    
    place_star(canvas,  tint_img(star_img, (155,0,0)), 300,300,300)

    place_star(canvas,star_img, 300,450,1)
    

    canvas.show()



if __name__ == "__main__":

    main()
