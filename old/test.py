import matplotlib.pyplot as plt
import numpy as np
import csv
import math



def scattar(xlist,ylist,sizelist,color):
    plt.scatter(xlist, ylist, s = sizelist, c=color)
    plt.title("Bright Stars")
    plt.xlabel("Right Ascention (degrees)")
    plt.ylabel("Declination (degrees)")
    plt.xlim(0, 360)
    plt.colorbar(label="Absolute magnitude")

    plt.annotate('larger circle = further star, darker color=brighter star',
    xy = (1.0, -0.2),
    xycoords='axes fraction',
    ha='right',
    va="center",
    fontsize=10)


    plt.show()

def processcsv(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        rowcount=0

        xlist=[]
        ylist=[]
        lylist=[]
        maglist=[]

        # ['designation', 'ra', 'dec', 'parallax', 'phot_g_mean_mag', 'bp_rp']
        for row in reader:
            if (row[1] and row[2] and rowcount != 0):
                if (row[3] and float(row[3])>0):
                    parallax = float(row[3])
                    parsec = 1/(parallax/1000)
                    lightyears=(parsec * 3.26156)
                    appmag = float(row[4])
                    absmag = appmag - (5* (math.log10(parsec/10)))
                    distscale=(lightyears)/60

                    if absmag <= 4.5:
                      xlist.append(float(row[1]))
                      ylist.append(float(row[2]))
                      lylist.append(distscale)
                      maglist.append(absmag)

            rowcount+=1

        return [xlist,ylist,lylist,maglist]


def main():

    info = processcsv('bsstars.csv')
    #x: cords[0] y:cords[1]


    xcords = info[0]
    ycords = info[1]
    dist = info[2]
    color = info[3]
    
    print(dist)


    scattar(xcords,ycords,dist,color)




main()

# below plots stars based on deg and ra, long and lat
# it scales and colors stars based on absolute mangitude (brightness of star) and distance
# to show the galactic plane

