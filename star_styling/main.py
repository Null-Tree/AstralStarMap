

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




def main():
    canvas:Image=createimg()

    
    place_star(canvas,star_img, 300,300,300)

    place_star(canvas,star_img, 300,450,1)
    

    canvas.show()



if __name__ == "__main__":

    main()
