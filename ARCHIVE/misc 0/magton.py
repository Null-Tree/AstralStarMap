
import matplotlib.pyplot as plt
import numpy as np
import csv
import math



def scattar(absmag,number):
    plt.scatter(absmag, number)
    plt.title("abs mag to number of stars")
    plt.xlabel("abs mag")
    plt.ylabel("number")

    plt.show()

def processcsv(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        rowcount=0

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

                    maglist.append(absmag)

            rowcount+=1

        return maglist


def getcount(mags):
    maglist=mags
    min=round( min(maglist) )
    max=round(max(maglist) )
    dict={}
    for i in range(min,max+1,0.5):
        dict[i]=0

    for mag in maglist:
        n = round(mag*2)/2
        dict[i]+=1
    return dict

def dicttolist(dict):
    xlist=[]
    ylist=[]
    for key in dict:
        xlist.append(key)
        ylist.append(dict[key])
    return [xlist,ylist]

def main():

    maglist= processcsv('bsstars.csv')
    info=getcount(maglist)
    absmag=info[0]
    n=info[1]
    scattar(absmag,n)




main()

# below plots stars based on deg and ra, long and lat
# it scales and colors stars based on absolute mangitude (brightness of star) and distance
# to show the galactic plane

