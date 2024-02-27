import numpy as np
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
import os
from astropy import units as u
from astropy.coordinates import SkyCoord
import traceback
from dataclasses import make_dataclass

######### Load data set
ybsc_catalog = None

with open('bsc5.dat', 'r') as fi:
    ybsc_catalog = fi.readlines()

# print(ybsc_catalog[0])

######### Parse the data
YBSC_Entry = make_dataclass("YBSC_Entry", [
    ("id", int),
    ("name", str),
    ("constellation", str),
    ("coord", SkyCoord),
    ("glon", float),
    ("glat", float),
    ("gal_coord", SkyCoord),
    ("Vmag", float),
    ("n_Vmag", str),
    ("u_Vmag", str),
    ("spectral_type", str),
    ("spectral_type_full", str),
    ("n_spectral_type", str),
    ("RI", float),
    ("n_RI", str),
    ("BV", float),
    ("u_BV", str),
    ("UB", float),
    ("u_UB", str),
    ("RadVel", float),
    ("RotVel", float),
    ("Parallax", float),
    ("n_Parallax", str)
])

spectral_types = ["O", "B", "A", "F", "G", "K", "M", "D", "S", "C", "W"]

def parse_float(n):
    try:
        return float(n)
    except ValueError:
        return None

def parse_int(n):
    try:
        return float(n)
    except ValueError:
        return None

def get_star_data_df():
    entries = []
    for i, row in enumerate(ybsc_catalog):
        try:
            star_id = row[0:4]
            name = row[4:14]
            constellation = row[11:14].strip()

            coord_str = f"{row[75:77]} {row[77:79]} {row[79:83]} {row[83]}{row[84:86]} {row[86:88]} {row[88:90]}"
            # print(coord_str)
            coord = SkyCoord(coord_str, unit=(u.hourangle, u.deg), frame='icrs')
            
            glon = parse_float(row[90:96])
            glat = parse_float(row[96:102])
            gal_coord = SkyCoord(l=glon, b=glat, frame='galactic', unit=u.degree)

            mag = parse_float(row[102:107])
            n_mag = row[107]
            u_mag = row[108]

            spectral_type_full = row[127:147].strip()
            spectral_type = spectral_type_full[0]
            n_spectral_type = row[147]
            
            if not np.isin(spectral_type, spectral_types):
                # For cases like gG8
                spectral_type = spectral_type_full[1]
                if not np.isin(spectral_type, spectral_types):
                    continue
            
            # UBV system
            BV = parse_float(row[109:114])
            u_BV = row[114]
            
            UB = parse_float(row[115:120])
            u_UB = row[120]
            
            RI = parse_float(row[121:126])
            n_RI = row[126]
            
            RadVel = parse_int(row[166:170])
            RotVel = parse_int(row[176:179])
            
            n_parallax = row[160]
            parallax = parse_float(row[161:166])
        
            entries.append(YBSC_Entry(
                id=star_id,
                name=name,
                constellation=constellation,
                coord=coord,
                glon=glon,
                glat=glat,
                gal_coord=gal_coord,
                Vmag=mag,
                n_Vmag=n_mag,
                u_Vmag=u_mag,
                spectral_type=spectral_type,
                spectral_type_full=spectral_type_full,
                n_spectral_type=n_spectral_type,
                BV=BV,
                u_BV=u_BV,
                UB=UB,
                u_UB=u_UB,
                RI=RI,
                n_RI=n_RI,
                RadVel=RadVel,
                RotVel=RotVel,
                Parallax=parallax,
                n_Parallax=n_parallax
            ))
        except ValueError as e:
            pass
    #         print(traceback.format_exc())
            # print(f"Skipping row {i+1} Reason: {e}")

    df = pd.DataFrame(entries)

    #Transform the coordinate system
    df["g_coord_l_rad"] = df["gal_coord"].transform(lambda c: c.l.wrap_at('180d').radian)
    df["g_coord_b_rad"] = df["gal_coord"].transform(lambda c: c.b.radian)

    df["coord_ra_deg"] = df["coord"].transform(lambda c: c.ra.degree)
    df["coord_dec_deg"] = df["coord"].transform(lambda c: c.dec.degree)


    return df