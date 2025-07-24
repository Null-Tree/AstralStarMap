import numpy as np
import csv
from tqdm import tqdm


import astropy.units as u
import astropy.time
import astropy.coordinates


def getfilelen(filepath):
    with open(filepath, 'r') as fp:
        for count, line in enumerate(fp):
            pass
    return count+1

print(
getfilelen(r"C:\Users\qixuy\Documents\GitHub\AstralStarMap\add_galactic_lb\outtest.csv"))