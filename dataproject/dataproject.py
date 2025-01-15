
import matplotlib.pyplot as plt
import numpy as np
import csv
import sqlite3
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
    






def equatorialtogalactic(ra,dec): 
    coord = astropy.coordinates.TETE(
    ra=ra * u.deg,
    dec=dec * u.deg,
    obstime=astropy.time.Time("2023-04-12"))

    coord = coord.transform_to(astropy.coordinates.Galactic())
    return coord


def loadstars(infilepath,outputfile):
        with open(infilepath, newline='') as csvfilein:
            reader = csv.reader(csvfilein, delimiter=',',)

            rowcount=0
            with open(outputfile, 'w', newline='') as csvfileout:
                writer=csv.writer(csvfileout, delimiter=',')

               #  print("start")
               #  print(csvfilein,csvfileout)

                writer.writerow(["id","designation",'appmag','absmag','bprp','ra','dec','ly','parallax','parsec','from earth X','from earth Y','from earth Z','galactic l','galactic b'])  #header


                # designation0,source_id1,ra2,dec3,parallax4,phot_g_mean_mag5,bp_rp6,radial_velocity7
                for row in reader:

                    if (row[2] and row[3] and rowcount != 0):    #validation
                        newstar=GaiaStar()
                        
                        if row[4]:
                             newstar.parallax = abs(float(row[4]))
                        else:
                             newstar.parallax = 100
                        
                        if row[5]:
                             newstar.appmag = float(row[5])
                        else:
                             newstar.appmag= 8
                        
                        if row[6]:
                             newstar.bprp= float(row[6])
                        else:
                             newstar.bprp= 0
                        
                        if float(newstar.appmag)>=8:
                             continue
                        
                        
                        newstar.ra= float(row[2])
                        newstar.dec= float(row[3])
                        
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
                    #     print(list)
                        
                    rowcount+=1

                    
                                    
                        
                
    

def main():
    loadstars('csv/gaia.csv','csv/visstars8.csv')
    print("done")

main()



# id,designation,appmag,absmag,bprp,ra,dec,ly,parallax,parsec,from earth X,from earth Y,from earth Z,galactic l,galactic b
# 2,,10.000008327879812,5.936236418643353,2.7318716,326.9649713590381,14.82578261853893,211.9238104545164,15.390248,64.97621090966176,,,,70.23747741054275,-28.70093539563574
