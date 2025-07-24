import numpy as np
import csv
from tqdm import tqdm


import astropy.units as u
import astropy.time
import astropy.coordinates


def equatorialtogalactic(ra,dec): 
    coord = astropy.coordinates.TETE(
    ra=ra * u.deg,
    dec=dec * u.deg,
    obstime=astropy.time.Time("2023-04-12"))

    coord = coord.transform_to(astropy.coordinates.Galactic())
    return coord


cord=equatorialtogalactic(186.649584           , -63.099094)

print(cord.l.deg)
print(cord.b.deg)