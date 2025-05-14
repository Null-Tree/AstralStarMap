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


width = 3360
height= int(round(9/16 * width))


xlist=[]
ylist=[]
zlist=[]
maglist=[]
rgblist=[]
pxlist=[]
pylist=[]
ralist=[]
declist=[]
llist=[]
dlist=[]

rgbbaseline=217 
rgbdifference=255-rgbbaseline

def scattar():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    p=ax.scatter(xlist, ylist, zlist,c=maglist)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    fig.colorbar(p,ax=ax,label="Absolute Magnitude")

    plt.show()

def processcsv(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        rowcount=0


        # ['designation', 'ra', 'dec', 'parallax', 'phot_g_mean_mag', 'bp_rp']
        for row in reader:
            if (row[1] and row[2] and row[3] and row[4] and row[5] and rowcount != 0 and float(row[3]) > 0):    #validation
                ra= float(row[1])
                dec= float(row[2])
                appmag = float(row[4])
                parallax = float(row[3])
                bprp= float(row[5])
                
                galacticcoord = equatorialtogalactic(ra,dec)  #convert to galactic
                llist.append(galacticcoord.l.deg)
                dlist.append(galacticcoord.d.deg)

                processmanual(parallax,appmag,galacticcoord.l.deg,galacticcoord.b.deg,bprp)
                ralist.append(ra)
                declist.append(dec)
                
                    
            rowcount+=1


def processmanual(parallax,appmag,long,lat,bprp):
    parallax = float(parallax)
    parsec = 1/(parallax/1000)
    lightyears=(parsec * 3.26156)

    appmag = float(appmag)
    absmag = appmag - (5* (math.log10(parsec/10)))

    ra= float(long)
    dec= float(lat)

    x= lightyears * math.cos(math.radians(dec)) * math.cos(math.radians(ra))
    y= lightyears * math.cos(math.radians(dec)) * math.sin(math.radians(ra))
    z= lightyears * math.sin(math.radians(dec))
    xlist.append(x)
    ylist.append(y)
    zlist.append(z)
    maglist.append(absmag)
    rgblist.append(torgb(bprp))
    




def spherify():
    
    for i in range(len(xlist)):
        dist = math.sqrt(xlist[i]**2 + ylist[i]**2 + zlist[i]**2)
        xlist[i] = xlist[i]/dist
        ylist[i] = ylist[i]/dist
        zlist[i] = zlist[i]/dist


def equatorialtogalactic(ra,dec): 
    coord = astropy.coordinates.TETE(
    ra=ra * u.deg,
    dec=dec * u.deg,
    obstime=astropy.time.Time("2023-04-12"))

    coord = coord.transform_to(astropy.coordinates.Galactic())
    return coord

def torgb(bprb):
    #converts bp-rp to rgb value
    # rgb(212, 217, 234)blue
    # rgb(235, 227, 225)red

    
    redcoeff=0.5
    bluecoeff=0.5
    
    # return [rgbbaseline + (rgbdifference * redcoeff),rgbbaseline,rgbbaseline+(rgbdifference * bluecoeff)]
    return [255,255,255]
    

# def project():
#     for i in len(xlist):
#         x,y,z=xlist[i],ylist[i],zlist[i]



def createimg():


    img = Image.new(mode="RGB",size=(width,height) )

    draw = ImageDraw.Draw(img)
    draw.circle((x,y), radius=3, fill=128, outline=128, width=2)
    # img.save(sys.stdout, "PNG")
    
    img.show()

    return img



def main():
    
    datafilename = "bsstars.csv"

    processcsv(datafilename)


    spherify()


    # scattar()
    createimg()


    



main()





# main()


# below plots stars based on dec and ra, long and lat
# it scales and colors stars based on absolute mangitude (brightness of star) and distance
# to show the galactic plane

