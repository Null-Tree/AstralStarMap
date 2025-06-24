import numpy as np
import sys
import csv
import pyvo as vo
import matplotlib.pyplot as plt
import pandas as pd

def draw_pm_circle(pmra0,pmdec0,rad,colour):
    t = np.linspace(0,2*np.pi,100)
    x = pmra0 + rad*np.sin(t)
    y = pmdec0 + rad*np.cos(t)
    plt.plot(x,y,colour)
    return

def draw_sky_circle(ra0,dec0,rad,colour):
    t = np.linspace(0,2*np.pi,100)
    x = ra0 + rad*np.sin(t)/np.cos(dec0*np.pi/180.0)
    y = dec0 + rad*np.cos(t)
    plt.plot(x,y,colour)
    return

nargs = len(sys.argv) - 1
if nargs == 3:
    sourcename = sys.argv[1]
    srad = float(sys.argv[2])
    gmag_lim = float(sys.argv[3])
else:
    print('Example use: give source name, search radius in arcmin and Gmag limit')
    print('python dr3_fetch.py "PSR B0531+21" 1 22')
    sys.exit()

print('Connecting to SIMBAD TAP')
service = vo.dal.TAPService("https://simbad.u-strasbg.fr/simbad/sim-tap")
command = "SELECT * FROM basic JOIN ident ON oidref = oid WHERE id = '"+str(sourcename)+"'"
print(command)
print('Sending request')
data = service.search(command)
pdf = pd.DataFrame(data)

try:
    ra0 = float(data['ra'])
    dec0 = float(data['dec'])
    pmra0 = float(data['pmra'])
    pmdec0 = float(data['pmdec'])
except:
    print("Error getting RA and DEC of target from SIMBAD")
    sys.exit()

print("======================")
print("Data from Simbad")
print("Coords : ",ra0,dec0)
print("PMs : ",pmra0,pmdec0)
print("PM BIBCODE ",data['pm_bibcode'])
print("======================")

if np.isnan(pmra0):
    pmra0 = 0.0

if np.isnan(pmdec0):
    pmdec0 = 0.0

# source of coords, pms = Marcus from 50 yr timing set    

plt.figure(figsize=(14,10))

def ra2deg(ra):
    ra = ra.split(":")
    radeg = (float(ra[0]) + float(ra[1])/60.0 + float(ra[2])/3600.0)*15.0
    return radeg

def dec2deg(dec):
    sign = +1.0
    if dec[0:1] == "-":
        sign = -1.0
        dec = dec[1:]
    dec = dec.split(":")
    decdeg = sign*(float(dec[0]) + float(dec[1])/60.0 + float(dec[2])/3600.0)
    return decdeg

if sourcename == "PSR B0736-40":
    pmra0 = -36.0
    pmdec0 = 30.0
    ra0 = "07:38:32.319"
    dec0 = "-40:42:40.20"
    ra0 = ra2deg(ra0)
    dec0 = dec2deg(dec0)

    print("======================")
    print("Data from Marcus")
    print("Coords : ",ra0,dec0)
    print("PMs : ",pmra0,pmdec0)
    print("======================")


# generate square region to search around target RA and DEC    
ra_lo = (ra0 - srad/60.0/np.cos(dec0*np.pi/180.0))
ra_hi = (ra0 + srad/60.0/np.cos(dec0*np.pi/180.0))
dec_lo = dec0 - srad/60.0
dec_hi = dec0 + srad/60.0

ra_lo = np.around(ra_lo,4)
ra_hi = np.around(ra_hi,4)
dec_lo = np.around(dec_lo,4)
dec_hi = np.around(dec_hi,4)

# generate command to send to GAIA
command = 'SELECT * FROM gaiadr3.gaia_source\n'
command += 'where ra>'+str(ra_lo)+' and ra<'+str(ra_hi)+' and '
command += 'dec>'+str(dec_lo)+' and dec<'+str(dec_hi)+'\nand '
command += 'phot_g_mean_mag < '+str(gmag_lim)

# print the command
print()
print(command)
print()

# set up the TAP address
service = vo.dal.TAPService("https://gea.esac.esa.int/tap-server/tap")

# make the data request
data = service.search(command)

# convert the dataset to a pandas frame
frame = pd.DataFrame(data)

# write the data set out as a CSV
sourcename = sourcename.replace(' ', '_') 
print("Writing data set to disk as "+sourcename+".csv")
frame.to_csv(sourcename+".csv")

# extract relevant items from the data set
source_id = data['source_id']
ra = data['ra']
dec = data['dec']
pmra = data['pmra']
pmdec = data['pmdec']
parallax = data['parallax']
parallax_error = data['parallax_error']
radial_velocity = data['radial_velocity']
radial_velocity_error = data['radial_velocity_error']
gmag = data['phot_g_mean_mag']
bp_rp = data['bp_rp']
nueffused = data['nu_eff_used_in_astrometry']
psc = data['pseudocolour']
ecl_lat = data['ecl_lat']
soltype = data['astrometric_params_solved']
#gl = data['l']
#gb = data['b']

rv = data['radial_velocity']

if len(rv) == 1:
    print(source_id[0], ra[0], dec[0], gmag[0], bp_rp[0], parallax[0], pmra[0], pmdec[0], rv[0], " SRSC")

alpha_g = 0.8
alpha_b = 0.2

marker_b = 'b.'
marker_b = ' '
marker_g = 'g.'

#plt.figure(figsize=(20,10))

# plot proper motions
plt.subplot(231)
plt.plot(pmra,pmdec,marker_g,alpha=alpha_g) #,markeredgecolor='k')
#plt.xlim(pmra0-xs,pmra0+xs)
#plt.ylim(pmdec0-ys,pmdec0+ys)
plt.xlabel("PMRA [mas/yr]")
plt.ylabel("PMDEC [mas/yr]")
plt.plot(pmra0,pmdec0,'k+',ms=20)

# plot parallaxes versus G magnitude
plt.subplot(133)
plt.plot(parallax,gmag,marker_g,alpha=alpha_g)
plt.xlabel("parallax [mas]")
plt.ylabel("Gmag")
plt.ylim(gmag_lim+0.5,5)
dist = np.sqrt(((ra-ra0)*np.cos(dec0*np.pi/180.0))**2+(dec-dec0)**2) # close enough
mind = list(dist).index(min(dist))
plt.plot(parallax[mind],gmag[mind],'k+',ms=20)

# plot CMD
plt.subplot(132)
plt.plot(bp_rp,gmag,marker_g,alpha=alpha_g)
plt.xlabel("BP-RP")
plt.ylabel("Gmag")
plt.ylim(gmag_lim+0.5,5)
plt.plot(bp_rp[mind],gmag[mind],'k+',ms=20)
plt.title(sourcename)

# sky positions
plt.subplot(234)
plt.plot(ra,dec,marker_g,alpha=alpha_g)
plt.xlabel("RA [deg]")
plt.ylabel("DEC [deg]")
plt.plot(ra0,dec0,'k+',ms=20)

#plt.show()

plt.plot(gmag,radial_velocity,'.')
plt.xlabel("G [mag]")
plt.ylabel("radial velocity [km/s]")

#plt.show()


#sys.exit()


