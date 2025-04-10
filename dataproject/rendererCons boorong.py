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

#a3 export


#skybox export
#########################################################################################

#CONFIG
sizepower=14 #size power for dimensions of expor timage #normal 14 for 16k

#stars
#min radius of star
minradius=1
maxradius=2
sizedeviCoef=5
#color min intensity of star rgb
colormin=200

Cmax=255
#color varience divider
rbvariencediv=4
#app mag req
appmagreq = 8
#greyshade
#makes color into shade of grey x
greyshade=False

colorOverride=False
overrideRGB=(255,255,255)

#color border for ocnstalations
consborderRGB = (100,100,100) 
#line width for constalations
conslinewidth=4

#width power of 2, height half
width=int(2**sizepower)
height=int(width/2)

#txtcondif
txtfill = (194, 215, 234)
txtfontsize=32
consLabel=True

#bg
bgcolor=(0,0,0)

###############################################################
###################################





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

    

    #abs mag visible 8 to -1.5
    global appmagreq
    consider = appmagreq-star.appmag 
    #consider: value = brightness 0 to 9.5 
    coef=consider/(appmagreq+1.5)

    global colormin
    min=colormin
    baseline= int( (255-min)**(coef+0.5) +min)
    
    if baseline >255:
        baseline=255
    diff=255-baseline
    global rbvariencediv
    diff/=rbvariencediv
    global Cmax
    if greyshade:
        if baseline>Cmax:
            baseline=Cmax
        dot.rgb=(baseline,baseline,baseline)
    else:

        rb=10**(star.bprp/2.5)
        u=diff/(rb+1)
        r=int(u*rb+baseline)
        b=int(u+baseline)
        # print(f"({r},{baseline},{b}) rb{rb} diff{diff} u{u}")

        g=baseline
    
        
        if r>Cmax:
            r=Cmax
        if g>Cmax:
            g=Cmax
        if b>Cmax:
            b=Cmax
        
        global colorOverride, overrideRGB
        if colorOverride:
            dot.rgb = overrideRGB
        else:
            dot.rgb=(r,g,b)
    

    # dot.radius=5
    global minradius
    global sizedeviCoef
    dot.radius=int(round((coef*sizedeviCoef+minradius)))
    # print(str(coef)+" | ceof")
    # print(dot.radius)
    if dot.radius>maxradius:
        dot.radius=maxradius
    

    return dot

def count():
    global n
    n += 1
    # print(n)

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
    global bgcolor
    img = Image.new(mode="RGB",size=(width,height), color=bgcolor )
    return img

def placestar(imgstar:stargraphic,img):
    draw = ImageDraw.Draw(img)

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
    

def plot(img:Image):
    fig = plt.figure()
    ax = fig.add_subplot()
    p=ax.scatter(xlist, ylist,c=maglist,s=sizelist)

    ax.set_xlabel('RA Label')
    ax.set_ylabel('DEC Label')
    fig.colorbar(p,ax=ax,label="Absolute Magnitude")

    handleconsjson(ax,img)

    plt.show()
    plt.close()


#------------------------------------------------------------------------------

def drawline(xlist,ylist,img):
    draw = ImageDraw.Draw(img)
    global consborderRGB
    xl=xlist
    yl=ylist
    cordslist=[]

    for i in range(len(xlist)):
        x=xl[i]
        y=yl[i]

        #TODO convert to pixel

        x= width-int((float(x) / 360) * width)  # inverted
        y= int(((float(y-90)*-1)/180) * height) 

        cordslist.append((x,y))

        # print(cordslist)

    
    global conslinewidth
    draw.line(cordslist, fill =consborderRGB, width = conslinewidth)

def drawtext(ralist : list, declist : list, strlist : list, img:Image):
    draw=ImageDraw.Draw(img)
    rl=ralist
    dl=declist
    namelist=strlist
    global txtfill,txtfontsize

    for i in range(len(rl)):
        x=rl[i]
        y=dl[i]
        x= width-int((float(x) / 360) * width)  # inverted
        y= int(((float(y-90)*-1)/180) * height)

        cord=(x,y)
        name=namelist[i]

        global txtfontsize,txtfill
        font = ImageFont.truetype(r'fonts/times.ttf', txtfontsize) 
        draw.text(cord,name,fill = txtfill,font=font)

# ImageDraw.Draw.text(xy, text, fill=None, font=None, anchor=None, spacing=0, align=”left”)    



#=============================================================================================================

# 24 hour
def wrapped_line(ra,de): #numpy arrays
    # [23.63561223  0.30546109] [43.26807662 36.78522667] * pi. And * del And
    # takes an ra,dec pair and creates two new lines crossing 00:00-24:00 to join them
    # assumes Cartesian 2-D plot
    ra_new = np.zeros(4)
    de_new = np.zeros(4)
    ra_new[0] = ra[0]
    de_new[0] = de[0]
    ra_new[3] = ra[1]
    de_new[3] = de[1]
    if ra[0] > 12.0:
        ra_new[1] = 24.0
        de_new[1] = de[0] + (24.0-ra[0])/((ra[1]+24)-ra[0]) * (de[1]-de[0])
        ra_new[2] = 0.0
        de_new[2] = de[0] + (24.0-ra[0])/((ra[1]+24)-ra[0]) * (de[1]-de[0])
    else:
        ra_new[1] = 0.0
        de_new[1] = de[0] - (0.0-ra[0])/(ra[1]-ra[0]) * (de[1]-de[0])
        ra_new[2] = 24.0
        de_new[2] = de[0] - (0.0-ra[0])/(ra[1]-ra[0]) * (de[1]-de[0])
    
    

    return ra_new, de_new

def get_ra_dec(starname,identity,ra,de):
    #print(list(identity))
    index = list(identity).index(starname.strip())
    return ra[index], de[index]

def handleconsjson(ax,img):
    namelist=[]
    ralist=[]
    declist=[]


    # open list of stars with coordinates
    identity, ra_dec = np.loadtxt("csv/boorong/boorong_cords.txt",usecols=(3,6),delimiter='|',unpack=True,dtype=str)
    for i in range(len(identity)):
        identity[i] = identity[i].strip()
    Nstars = len(ra_dec)
    ra = np.zeros(Nstars)
    de = np.zeros(Nstars)
    for i in range(len(ra_dec)):
        ra[i] = float(ra_dec[i].split()[0])
        de[i] = float(ra_dec[i].split()[1])
        
    # Opening JSON file
    f = open('csv/boorong/boorong.json')

    # returns JSON object as a dictionary
    data = json.load(f)

    # Iterating through the json list need
    for constellation in data['constellations']:
        #TODO: get constalation name

        n,rasum,decsum=0,0,0
        
        constellationName = constellation['names'][0]['english']
        namelist.append(constellationName)

        this_lines = constellation['lines']
        # print(this_lines)
        # 
        for line in range(len(this_lines)):
            stars = this_lines[line]
            this_line_ra = np.zeros(len(stars))
            this_line_de = np.zeros(len(stars))
            
            for star in range(len(stars)):
                this_line_ra[star], this_line_de[star] = get_ra_dec(stars[star],identity,ra,de)
                this_line_ra[star] /= 15.0

                

                #ax.text(this_line_ra[star], this_line_de[star], str(stars[star]))
            #ax.scatter(this_line_ra, this_line_de, s=320, facecolors='none', edgecolors='k')
            for i in range(len(this_line_ra)-1):
                if abs(this_line_ra[i+1]-this_line_ra[i])<12:
                    #pass
                    finalra = ra2deg(this_line_ra)
                    # finalra=this_line_ra
                    # print(finalra)
                    for j in range(len(finalra)):
                        n+=1
                        rasum+=finalra[j]
                        decsum+=this_line_de[j]

                    
                    ax.plot(finalra[i:i+2], this_line_de[i:i+2], 'g-',alpha=0.5)
                    drawline(finalra[i:i+2],this_line_de[i:i+2],img)
                else:
                    # print(this_line_ra[i:i+2], this_line_de[i:i+2], stars[star-1], stars[star])
                    ra_new, de_new = wrapped_line(this_line_ra[i:i+2], this_line_de[i:i+2])
                    
                    finalra=ra2deg(ra_new)
                    # finalra=ra_new
                    #condition for edge


                    
                    ax.plot(finalra[0:2], de_new[0:2], 'g-',alpha=0.5)
                    ax.plot(finalra[2:4], de_new[2:4], 'g-',alpha=0.5)

                    drawline(finalra[0:2], de_new[0:2],img)
                    drawline(finalra[2:4], de_new[2:4],img)
                #TODO: get a position
        
        ramean=((rasum/n))
        decmean= ((decsum/n))
        # print(f"ra {ramean} de {decmean}")
        ralist.append(ramean)
        declist.append(decmean)
    
    global consLabel
    if consLabel:
        drawtext(ralist,declist,namelist,img)

    # Close file
    f.close()

def ra2deg(ra:list):
    list=ra
    result=[0]*len(list)
    for i in range(len(list)):
        result[i]=float(list[i])/24*360
    return result


#===============================================================================================================

def main():
    img=createimg()
    plot(img)
    
    processcsv("csv/visstars8_NewCat.csv",img)
    processBS("csv/brightstars.csv",img)
    

    
    
    

    saveimg(img)








main()