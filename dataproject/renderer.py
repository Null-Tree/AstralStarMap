import random
import json
import matplotlib.pyplot as plt
import numpy as np
import csv
import sqlite3
import math
import sys

from tkinter import * 
from PIL import Image,ImageDraw  #Pillow library
import scipy.ndimage as ndi

import astropy.units as u
import astropy.time
import astropy.coordinates

from dataclasses import dataclass




@dataclass         
class Star:
    id:int=None
    designation: str=None

    
    appmag:float=None
    absmag:float=None
    bprp:float=None

    ra: float=None
    dec:float=None
    ly:float=None
    parallax: float=None
    parsec:float=None
    eX:float=None
    eY:float=None
    eZ:float =None#earth centered

    galacticl:float=None
    galacticb:float=None



@dataclass         
class stargraphic:
    rgb:list = None
    radius:int=1
    x:int=None
    y:int=None


#CONFIG
sizepower=13
#stars
minradius=2
#color min
colormin=150
#color divider
rbvariencediv=4
#app mag req
appmagreq = 3
#color border for ocnstalations
consborderRGB = (100,100,100)



#width power of 2, height half
width=int(2**sizepower)
height=int(width/2)



xlist=[]
ylist=[]
maglist=[]
sizelist=[]
size=1

n=0

# handles gaia stars
def processcsv(filepath,img:Image):
    with open(filepath, newline='') as csvfilein:
            reader = csv.reader(csvfilein, delimiter=',',)
            rowcount=0

            
            for row in reader:
                if rowcount==0:
                    rowcount+=1
                    continue
                star=Star(
                    int(row[0]),
                    row[1],
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[5]),
                    float(row[6]),
                    float(row[7]),
                    float(row[8]),
                    float(row[9]),
                    float(row[10]),
                    float(row[11]),
                    float(row[12]),
                    float(row[13]),
                    float(row[14]))
                global appmagreq
                if star.appmag<appmagreq:
                    xlist.append(star.ra)
                    ylist.append(star.dec)
                    maglist.append(star.absmag)
                    sizelist.append(size)
                    count()
                    imgstar=starformatter(star)
                    placestar(imgstar,img)

                
                    

                rowcount+=1
    

def starformatter(star:Star):
    
    dot=stargraphic()
    #bprp to blue red ratio
    #abs mag and app mag to brightness

    dot.x= width-int((float(star.ra) / 360) * width)  #TODO revert inversion
    dot.y= int(((float(star.dec-90)*-1)/180) * height) 

    

    #abs mag visible 6 to -1.5
    consider = 6-star.appmag 
    #consider: value = brightness 0 to 4.5
    coef=consider/4.5

    global colormin
    min=colormin
    baseline= int( (255-min)**(coef+0.5) +min)
    
    if baseline >255:
        baseline=255
    diff=255-baseline
    global rbvariencediv
    diff/=rbvariencediv

    

    

    rb=10**(star.bprp/2.5)
    u=diff/(rb+1)
    r=int(u*rb+baseline)
    b=int(u+baseline)
    print(f"({r},{baseline},{b}) rb{rb} diff{diff} u{u}")


    g=baseline

    dot.rgb=(r,g,b)

    # dot.radius=5
    global minradius
    dot.radius=int(coef*14+minradius)

    return dot

def count():
    global n
    n += 1
    print(n)

#handles bright stars
def processBS(filepath,img:Image):
    with open(filepath, newline='') as csvfilein:
            reader = csv.reader(csvfilein, delimiter=',',)
            rowcount=0

            # idents,ra,dec,V,B-V,parallax 
            for row in reader:
                if rowcount==0:
                    rowcount+=1
                    continue
                star=Star(
                    int(row[0]),
                    row[1],
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[5]),
                    float(row[6]),
                    float(row[7]),
                    float(row[8]),
                    float(row[9]),
                    float(row[10]),
                    float(row[11]),
                    float(row[12]),
                    float(row[13]),
                    float(row[14]))
                global appmagreq
                if star.appmag<appmagreq:
                    xlist.append(star.ra)
                    ylist.append(star.dec)
                    maglist.append(star.absmag)
                    sizelist.append(size)
                    count()

                    imgstar=starformatter(star)
                    
                    placestar(imgstar,img)
            

def createimg():

    img = Image.new(mode="RGB",size=(width,height) )
    return img

def placestar(imgstar:stargraphic,img):
    draw = ImageDraw.Draw(img)
    rgb=imgstar.rgb

    draw.circle((imgstar.x,imgstar.y), radius=imgstar.radius, fill=imgstar.rgb, outline=imgstar.rgb, width=1)

def saveimg(img):
    # img.save(sys.stdout, "PNG")
    img.show()    
    string=f"exports/Export{tempfile()}.png"
    print(f"saved as {string}")
    img.save(string)
    tempfile(1)

def tempfile(n = None):
    filePath = "exports/ref.txt"
    if not n:                      # If not provided return file content
        with open(filePath, "r") as f:
            n = int(f.read())
            return n
    else:
        with open(filePath, "r") as f:
            n = int(f.read())
        with  open(filePath, "a") as f:# Create a blank file
            f.seek(0)  # sets  point at the beginning of the file
            f.truncate()  # Clear previous content
            f.write(f"{n+1}") # Write file
            return n+1
    

def plot():
    fig = plt.figure()
    ax = fig.add_subplot()
    p=ax.scatter(xlist, ylist,c=maglist,s=sizelist)

    ax.set_xlabel('RA Label')
    ax.set_ylabel('DEC Label')
    fig.colorbar(p,ax=ax,label="Absolute Magnitude")

    plt.show()




def main():
    img=createimg()
    
    processcsv("csv/visstars8.csv",img)
    processBS("csv/brightstars.csv",img)
    


    saveimg(img)

    # plot()









main()