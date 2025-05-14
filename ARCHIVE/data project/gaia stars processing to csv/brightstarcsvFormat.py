
import matplotlib.pyplot as plt
import numpy as np
import csv
import sqlite3
import string
import math

from tkinter import * 
from PIL import Image,ImageDraw  #Pillow library
import scipy.ndimage as ndi

import astropy.units as u
import astropy.time
import astropy.coordinates

from dataclasses import dataclass

@dataclass         
class GaiaStar:
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
    



# idents,ra,dec,V,B-V,parallax  
# id,designation,appmag,absmag,bprp,ra,dec,ly,parallax,parsec,from earth X,from earth Y,from earth Z,galactic l,galactic b

def equatorialtogalactic(ra,dec): 
    coord = astropy.coordinates.TETE(
    ra=ra * u.deg,
    dec=dec * u.deg,
    obstime=astropy.time.Time("2023-04-12"))

    coord = coord.transform_to(astropy.coordinates.Galactic())
    return coord

def dms2dd(dms:str,mode:str):
     prefix=''
     
     if mode=="dec":
        prefix=dms[0]
        dms=dms[1:]

     list=dms.split(":")

     degrees= float(list[0]) + (float(list[1]) /60 )+ (float(list[2]) / (60**2))
     
     if mode == "ra":
         degrees=degrees/24*360


     if prefix == "-":
         degrees=-degrees
     return degrees


def loadstars(infilepath,outputfile):
        with open(infilepath, newline='') as csvfilein:
            reader = csv.reader(csvfilein, delimiter=',',)

            rowcount=0
            with open(outputfile, 'w', newline='') as csvfileout:
                writer=csv.writer(csvfileout, delimiter=',')

                print("start")
                print(csvfilein,csvfileout)

                writer.writerow(["id","designation",'appmag','absmag','b-v; interpret as bprp','ra','dec','ly','parallax','parsec','from earth X','from earth Y','from earth Z','galactic l','galactic b'])  #header


                #idents0,1ra,2dec,3V,4B-V,5parallax 
                for row in reader:
                    print("-------------")
                    if (rowcount != 0):    #validation

                        newstar=GaiaStar()
                        newstar.ra= dms2dd(row[1],"ra")
                        newstar.dec=dms2dd(row[2],"dec")
                        newstar.bprp=row[4]
                        newstar.parallax = float(row[5])
                        newstar.appmag = float(row[3])
                        
                        newstar.designation=row[0]
                        
                        
                        galacticcoord = equatorialtogalactic(newstar.ra,newstar.dec)  #convert to galactic
                        newstar.galacticl=galacticcoord.l.deg
                        newstar.galacticb=galacticcoord.b.deg


                        newstar.parsec = 1/(newstar.parallax/1000)
                        newstar.ly=(newstar.parsec * 3.26156)

                        
                        appmag = newstar.appmag
                        newstar.absmag = appmag - (5* (math.log10(newstar.parsec/10)))

                        ra= newstar.ra
                        dec= newstar.dec
                        
                        pa= newstar.parsec

                        newstar.eX= pa * math.cos(math.radians(dec)) * math.cos(math.radians(ra))
                        newstar.eY= pa * math.cos(math.radians(dec)) * math.sin(math.radians(ra))
                        newstar.eZ=pa * math.sin(math.radians(dec))
                        newstar.id=rowcount

                        # ["id","designation",'appmag','absmag','bprp','ra','dec','ly','parallax','parsec','from earth X','from earth Y','from earth Z','galactic l','galactic b']
                        list=[newstar.id,newstar.designation,newstar.appmag,newstar.absmag,newstar.bprp,newstar.ra,newstar.dec,newstar.ly,newstar.parallax,newstar.parsec,newstar.eX,newstar.eY,newstar.eZ,newstar.galacticl,newstar.galacticb]
                        
                        writer.writerow(list)
                        print(list)
                        
                    rowcount+=1
                    print("-------------")

                    
                  

def main():
    loadstars('csv/brightstarsraw.csv','csv/brightstars.csv')
    print("done")

main()