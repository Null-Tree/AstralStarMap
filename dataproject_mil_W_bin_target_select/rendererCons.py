import random
import time
import json
import matplotlib.pyplot as plt
import numpy as np
import csv
import sqlite3
import math
import sys
from tqdm import tqdm
from tkinter import * 
from PIL import Image,ImageDraw, ImageFont #Pillow library
import scipy.ndimage as ndi

import astropy.units as u
import astropy.time
import astropy.coordinates

from dataclasses import dataclass

from color_system.color_system import *

from PIL import ImageOps


@dataclass         
class Star:
    appmag:float=None
    bprp:float=None

    ra: float=None
    dec:float=None

    gal_l:float=None
    gal_b:float=None



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



# sizepower=14 #size power for dimensions of expor timage #normal 14 for 16k

# 14 for 16k 

# sizepower=15
# maxradius=  100 #32*2



sizepower=15
maxradius=  80 #32*2


#width power of 2, height half
width=int(2**sizepower)
height=int(width/2)




# 13 for 8k

# sizepower=13
# maxradius= 18

#stars
#min radius of star
minradius=0



#color min intensity of star rgb
colormin=0


#app mag req
appmagreq = 100
#greyshade
#makes color into shade of grey x

draw_cons=False

#color border for ocnstalations
consborderRGB = (80,80,80) 
#line width for constalations
conslinewidth=4

#txtcondif
txtfill = (194, 215, 234)
txtfontsize=32
consLabel=False
antialius=True

#bg
bgcolor=(0,0,0)

star_graphic_original = Image.open(r"graphics\stargraphic.png")


# color system
cs = cs_hdtv

# disable for better stars
basic_render=True

# /"celestial" or "galactic"
cord_mode="galactic"

# % of width
horizontal_shift=0.5

###############################################################
###################################


def bounded_shift(val,delta,interval):
    """general shift, note start and end of interval are same, will go to int min"""
    vmin,vmax=interval
    vsum=val+delta
    interval_range=(vmax-vmin) 
    if vsum>vmax:
        d=vsum-vmax
        n=math.ceil(d/interval_range)
        vsum-=n*(vmax-vmin) 
    
    if vsum<vmin:
        d=vmin-vsum
        n=math.ceil(d/interval_range)
        vsum+=n*(vmax-vmin) 
    return vsum

xlist=[]
ylist=[]
maglist=[]
sizelist=[]
size=1

n=0


star_g_items:list[stargraphic]=[]


chucked=0



def equatorialtogalactic(ra,dec): 
    coord = astropy.coordinates.TETE(
    ra=ra * u.deg,
    dec=dec * u.deg,
    obstime=astropy.time.Time("2023-04-12"))

    coord = coord.transform_to(astropy.coordinates.Galactic())
    return coord





def getfilelen(filepath):
    with open(filepath, 'r') as fp:
        for count, line in enumerate(fp):
            pass
    return count+1

# handles gaia stars
def processcsv(filepath,img:Image):
    flen=getfilelen(filepath)
    with open(filepath, newline='') as csvfilein:
            reader = csv.reader(csvfilein, delimiter=',',)
            rowcount=0

            
            for row in tqdm(reader,total=flen):
                if rowcount==0:
                    rowcount+=1
                    continue
                
                

                tochuck=False
                for titem in row:
                    item=titem.lstrip()
                    if item =='' or item == None:
                        global chucked
                        # print(f"     {rowcount} chuck: {row}")
                        chucked+=1
                        tochuck=True

                if tochuck:
                    continue 
                
                star=Star(
                        float(row[2]),
                        float(row[3]),
                        float(row[0]),
                        float(row[1]),
                        float(row[4]),
                        float(row[5])
                        
                        )
                
                global appmagreq

                if star.appmag<appmagreq:
                    xlist.append(star.ra)
                    ylist.append(star.dec)
                    maglist.append(star.appmag)
                    sizelist.append(size)
                    count()
                    imgstar=starformatter(star)
                    # placestar(imgstar,img)

                
                    

                rowcount+=1
    

def appmag_to_size(appmag):
    global maxradius
    global minradius
    coef=  15.417/20 * (math.e ** (-0.425 * appmag))
    # coef 0 to 1

    

    size=coef*maxradius
    if size<minradius:
        size=minradius

    return size
    




lam = np.arange(380., 781., 5)
def starformatter(star:Star):
    global lam,cs,horizontal_shift
    
    dot=stargraphic()


    global cord_mode
    # /"celestial" or "galactic"
    if cord_mode=="celestial":
        cords={"x":star.ra,"y":star.dec}
    elif cord_mode=="galactic":
        cords={"x":star.gal_l,"y":star.gal_b}
    else:
        raise Exception("invalid cordinate mode")
    dot.x= width-int((float(cords["x"]) / 360) * width)  
    dot.x= bounded_shift(dot.x,width*horizontal_shift,(0,width))
    dot.y= int(((float(cords["y"]-90)*-1)/180) * height) 

    
    dot.radius=appmag_to_size(star.appmag)



    

    teff = BPRP_to_teff(star.bprp)

    spec = planck(lam, teff)

    rgb = cs.spec_to_rgb(spec).tolist()

    

    for i in range(3):
        rgb[i] = int(round(rgb[i]*256))
    
    # print(rgb)

    dot.rgb=tuple(rgb)





    
    star_g_items.append(dot)
    return dot

def count():
    global n
    n += 1
    # print(n)

#handles bright stars
def processBS(filepath,img:Image):
    flen=getfilelen(filepath)
    with open(filepath, newline='') as csvfilein:
            reader = csv.reader(csvfilein, delimiter=',',)
            rowcount=0

            # idents,ra,dec,V,B-V,parallax 

            for drow in tqdm(reader,total=flen):
                if rowcount==0:
                    # for i in range(len(drow)):
                    #     print(f"{i} {drow[i]}")
                    rowcount+=1
                    continue
            
                row=drow.copy()

                row[0]=int(row[0])
                
                for i in range(2,15):
                    if row[i] and row[i].lstrip()!="":
                        row[i]=float(row[i])


                #  id
                # 1  designation
                # 2  appmag
                # 3  absmag
                # 4  b-v; interpret as bprp
                # 5  ra
                # 6  dec
                # 7  ly
                # 8  parallax
                # 9  parsec
                # 10  from earth X
                # 11  from earth Y
                # 12  from earth Z
                # 13  galactic l
                # 14  galactic b

                    # float(row[2]),
                    # float(row[4]),
                    # float(row[5]),
                    # float(row[6])

                star=Star(
                        float(row[2]),
                        float(row[4]),
                        float(row[5]),
                        float(row[6]),
                        float(row[13]),
                        float(row[14])
                    )
                
                global appmagreq
                if star.appmag<appmagreq:
                    xlist.append(star.ra)
                    ylist.append(star.dec)
                    maglist.append(star.appmag)
                    sizelist.append(size)
                    count()

                    # imgstar=
                    starformatter(star)
                    
                    # placestar(imgstar,img)

def rgb_to_greyscale(rgb):

    # for avg

    # sum=0
    # for i in rgb:
    #     sum+=i
    # mean=sum//3
    
    # for peak
    mean=max(rgb)

    return (mean,mean,mean)

def BPRP_to_teff(bprp):
    """returns in kelvins"""
    teff = 5040/(0.4929+0.5092*bprp-0.0353*bprp**2)
    return teff           

def createimg():
    global bgcolor
    img = Image.new(mode="RGB",size=(width,height), color=bgcolor )
    return img


def tint_img(src:Image, color):
    """tints input image, src png, color rgb"""
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

n_stars=0

def placestar(imgstar:stargraphic,img:Image, center:bool):
    global n_stars,basic_render
    
    r=imgstar.radius


    
    if basic_render:
        b_render_curr=basic_render
    else:
        # r_thresh=5
        # b_render_curr = (r<r_thresh)
        b_render_curr = False
    
    
    final_rgb=list(imgstar.rgb)
    
    

    if b_render_curr:
    
        if r<1:
            grey_rgb=rgb_to_greyscale(final_rgb)
            if center == True:
                return

            # smoothing
            for i in range(3):
                
                # mean=grey_rgb[i] + (final_rgb[i]-grey_rgb[i])/2

                # adj with prop to r
                
                final_rgb[i] = int(round((r**0.5)*(final_rgb[i])))

    
    else:
        if r<1:

            # smoothing
            for i in range(3):
                
                # adj with prop to r
                final_rgb[i] = int(round(r*final_rgb[i]))
        
        grey_rgb=rgb_to_greyscale(final_rgb)


    final_rgb=tuple(final_rgb)
        
    # percentage of star radius for white center
    p_s_size = 0.6

    if not b_render_curr:
        # colored

        raw_adj=1

        # 2r
        r =  int(2*r) + raw_adj

        top_left_cords  = (imgstar.x-r,imgstar.y-r)


        if not center:
            global star_graphic_original
            star_graphic=star_graphic_original.copy()

            star_graphic = star_graphic.resize((2*r,2*r))
            
            star_graphic=tint_img(star_graphic,final_rgb)


            img.paste(star_graphic, top_left_cords ,star_graphic)

        else:
            n_stars+=1

            # white center


            r_w = round(r* p_s_size)

            white_center=star_graphic_original.copy()

            white_center = white_center.resize((2*r_w,2*r_w))

            white_center=tint_img(white_center,grey_rgb)

            top_left_cords  = (imgstar.x-r_w,imgstar.y-r_w)

            img.paste(white_center, top_left_cords ,white_center)

    else:
        draw = ImageDraw.Draw(img)
        if not center:
            n_stars+=1
            draw.circle((imgstar.x,imgstar.y), radius=imgstar.radius, fill=final_rgb)
        else:
            # inner circle
            
            draw.circle((imgstar.x,imgstar.y), radius=imgstar.radius*p_s_size, fill=rgb_to_greyscale(final_rgb))

        
        
        # how big it shoul dbe, outline
        # draw.circle((imgstar.x,imgstar.y), radius=imgstar.radius, fill=None, outline=(241, 64, 165), width=2)

        # locator
        # 
        # draw.circle((imgstar.x,imgstar.y), radius=imgstar.radius+10, fill=None, outline=imgstar.rgb, width=5)


def saveimg(img):
    # img.save(sys.stdout, "PNG")
    img.show()    
    string=f"exports/Export{tempfile()}.png"
    # string="v1WesternLOW.png"
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

    print("constallations loaded")
    # plt.show()
    plt.close()


#------------------------------------------------------------------------------

def drawline(xlist,ylist,img):

    global draw_cons
    if draw_cons == False:
        return

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

        global txtfontsize,txtfill,antialius
        ImageDraw.ImageDraw.fontmode=antialius
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
    identity, ra_dec = np.loadtxt("csv/iau.coords.txt",usecols=(1,5),delimiter='|',unpack=True,dtype=str)
    # print(ra_dec)
    for i in range(len(identity)):
        identity[i] = identity[i].strip()
    Nstars = len(ra_dec)
    ra = np.zeros(Nstars)
    de = np.zeros(Nstars)
    for i in range(len(ra_dec)):
        ra[i] = float(ra_dec[i].split()[0])
        de[i] = float(ra_dec[i].split()[1])
        
    # Opening JSON file
    f = open('csv/iau.json')

    # returns JSON object as a dictionary
    data = json.load(f)

    # Iterating through the json list need
    for constellation in tqdm(data['constellations']): 
        cross=False
        global cord_mode
        

        n,rasum_l,decsum_l=0,[],[]
        
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
                # print(this_line_ra[star], this_line_de[star])
                this_line_ra[star] /= 15.0  #rn tlra inhours, tlde in degrees


                if cord_mode =="galactic":
                    #needs tobe deg in deg out
                    cord=equatorialtogalactic(this_line_ra[star] * 15,this_line_de[star])
                    this_line_ra[star]=cord.l.deg /15 # needs to be in hours for later comparison
                    this_line_de[star]=cord.b.deg
                    

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
                        rasum_l.append(finalra[j])
                        decsum_l.append(this_line_de[j])

                    
                    ax.plot(finalra[i:i+2], this_line_de[i:i+2], 'g-',alpha=0.5)
                    drawline(finalra[i:i+2],this_line_de[i:i+2],img)
                else:
                    # print(this_line_ra[i:i+2], this_line_de[i:i+2], stars[star-1], stars[star])
                    cross=True
                    ra_new, de_new = wrapped_line(this_line_ra[i:i+2], this_line_de[i:i+2])
                    
                    finalra=ra2deg(ra_new)
                    # finalra=ra_new
                    #condition for edge


                    
                    ax.plot(finalra[0:2], de_new[0:2], 'g-',alpha=0.5)
                    ax.plot(finalra[2:4], de_new[2:4], 'g-',alpha=0.5)

                    drawline(finalra[0:2], de_new[0:2],img)
                    drawline(finalra[2:4], de_new[2:4],img)
                #TODO: get a position
        
        # check if cross boundaries


        # if len(rasum_l)==0
        


        if not cross:

            ramean=((sum(rasum_l)/n))

            decmean= ((sum(decsum_l)/n))

            # print(f"ra {ramean} de {decmean}")
            ralist.append(ramean)
            declist.append(decmean)
        else:
            # print(f"{constellationName} crosses broder")
            

            rasum_l.sort()

            # print(rasum_l)

            ral1,ral2=[],[]
            decl1,decl2=[],[]

            for i in range(len(rasum_l)):
                j=rasum_l[i]

                if j<180:
                    ral1.append(j)
                    decl1.append(decsum_l[i])
                else:
                    ral2.append(j)
                    decl2.append(decsum_l[i])

            # print(cross, ral1,ral2)
            ralist.append(  sum(ral1) / len(ral1) )
            declist.append( sum(decl1) / len(decl1) )


            namelist.append(constellationName)
            ralist.append(sum(ral2) / len(ral2))
            declist.append(sum(decl1) / len(decl1))

            
    
    global consLabel
    if consLabel:
        drawtext(ralist,declist,namelist,img)

    # Close file
    f.close()

def ra2deg(ra:list):
    """converts list of hours cords to degrees"""
    list=ra
    result=[0 for i in range(len(list))]
    for i in range(len(list)):
        result[i]=float(list[i])/24*360
    return result

#================================



def sort_by_radius():
    # orig_list.sort(key=lambda x: x.count, reverse=True)
    global star_g_items
    star_g_items.sort(key=lambda x: x.radius)

    print(f"r extremes {star_g_items[-1].radius}   {star_g_items[0].radius}")
    print([i.radius for i in star_g_items[0:20]])
    print([i.radius for i in star_g_items[-20:]])
    
def place_list_stars(img:Image):
    global star_g_items

    # # place glows
    # print("glows")
    # for imgstar in tqdm(star_g_items):
    #     placestar(imgstar,img,False)

    # # place white centers
    # print("centers")
    # for imgstar in tqdm(star_g_items):
    #     placestar(imgstar,img,True)

    # new
    # print("placing stars")
    for imgstar in tqdm(star_g_items):
        placestar(imgstar,img,False)
        placestar(imgstar,img,True)




#===============================================================================================================

def main():
    print("loading constallations")
    img=createimg()
    plot(img)
    
    print("\nprocessing csv")
    print("gaia catalouge")

    processcsv("csv/million_wgal.csv",img)
    print("amended bright stars")
    processBS("csv/brightstars.csv",img)
    print("csv processeds\n")


    # # data
    # rl=[appmag_to_size(appmag) for appmag in maglist]
    # # plt.hist(maglist,bin=50)
    # # plt.show()
    # # plt.hist(rl,bin=50)
    # # plt.show()
    # plt.scatter(maglist,rl)
    # plt.show()
    
    print("sorting stars")
    sort_by_radius()
    print("stars sorted\n")

    print("placing stars")
    place_list_stars(img)
    print("stars placed\n")


    print(f"{n_stars} objects plotted")

    print(f"{chucked} stars chucked")
    
    
    print("exporting image")
    saveimg(img)








if __name__=="__main__":
    start = time.time()
    main()
    print(time.strftime("%H hours %M minutes %S seconds", time.gmtime(time.time() - start)),f" elapsed")

