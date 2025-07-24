






expected_rows=3000000




#######################
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







def main(infilepath,outfilepath):
    rowcount=0

    with open(outfilepath, "w") as f:
            f.write("ra,dec,phot_g_mean_mag,bp_rp,gal_l,gal_b\n")


    with open(infilepath, newline='') as csvfilein:
        reader = csv.reader(csvfilein, delimiter=',',)
        # ra,dec,phot_g_mean_mag,bp_rp

        with open(outfilepath, "a") as fout:
            # f.write(str(content)+end)


            print("progress:")
            for drow in tqdm(reader,total=expected_rows):
                # print(drow)
                if rowcount == 0:
                     rowcount+=1
                     continue
                
                # if True:
                # if rowcount % 100000 ==0:
                #      print(rowcount)

                cord=drow[0:2]
                
                if not cord[0] or not cord[0]:
                #   ignore
                    continue
                
                ra=float(cord[0])
                dec=float(cord[1])

                gcord = equatorialtogalactic(ra,dec)
                gl=gcord.l.deg
                gb=gcord.b.deg

                fstr=""
                if len(drow)!=4:
                     print("error")
                     print(drow)
                     continue
                for item in drow:
                     fstr+=str(item)
                     fstr+=", "
                
                fstr+=f"{gl}, {gb}"

                fstr+="\n"
                fout.write(fstr)

                rowcount+=1


main(r"add_galactic_lb\csv\million.csv",r"add_galactic_lb\outtest.csv")
                 