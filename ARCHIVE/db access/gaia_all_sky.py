import numpy as np
import sys
import csv
import pyvo as vo
import matplotlib.pyplot as plt
import pandas as pd

# generate command to send to GAIA
command = 'SELECT '

command+="designation,source_id,ra,dec,parallax,phot_g_mean_mag,bp_rp,radial_velocity"
command+=' FROM gaiadr3.gaia_source\n'
command += 'WHERE phot_g_mean_mag < 8'

# set up the TAP address
service = vo.dal.TAPService("https://gea.esac.esa.int/tap-server/tap")

# make the data request
data: vo.dal.tap.TAPResults = service.search(command)
print(data.fieldnames)


# convert the dataset to a pandas frame
frame = pd.DataFrame(data,columns=['designation','source_id','ra','dec','parallax','phot_g_mean_mag','bp_rp','radial_velocity'])
# write the data set out as a CSV
sourcename = "newCat8"
print("Writing data set to disk as "+sourcename+".csv")
frame.to_csv(sourcename+".csv",index=False)

