import numpy as np
import sys
import csv
import pyvo as vo
import matplotlib.pyplot as plt
import pandas as pd

# generate command to send to GAIA
command = 'SELECT * FROM gaiadr3.gaia_source\n'
command += 'WHERE phot_g_mean_mag < 7'

# set up the TAP address
service = vo.dal.TAPService("https://gea.esac.esa.int/tap-server/tap")

# make the data request
data = service.search(command)

# convert the dataset to a pandas frame
frame = pd.DataFrame(data)

# write the data set out as a CSV
sourcename = "name"
print("Writing data set to disk as "+sourcename+".csv")
frame.to_csv(sourcename+".csv")

