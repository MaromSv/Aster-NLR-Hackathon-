import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns
from data import get_data_fast

df = get_data_fast()
print(df.set_index(['id'])['spectral_type_full'][31:36])

def getinfo(winnerids):
    df = get_data_fast()
    names = []
    distances = []
    spectraltypes = []
    i = 0
    while i < len(winnerids):
        starid = winnerids[i]
        df_grouped = df.set_index(['id'])
        name = df_grouped['name'][starid]
        names.append(name)
        distance = 3.26/(df_grouped['Parallax'][starid])
        distances.append(distance)
        spectraltype = df_grouped['spectral_type'][starid]
        spectraltypes.append(spectraltype)
        i = i + 1
    return names, distances, spectraltypes

def spectraltypeinfo(type):
    spectraltypeinfo = []
    if (type == 'O'):
        color = 'blue'
        temperature = '> 30000'
        madeof = 'Mainly neutral and ionized helium lines and weak hydrogen lines'
    elif (type == 'B'):
        color = 'blue-white'
        temperature =  '10000 - 30000'
        madeof = 'Neutral helium lines and strong hydrogen lines'
    elif (type == 'A'):
        color = 'white'
        temperature = '7500 - 10000'
        madeof = 'Strongest hydrogen lines weak ionized calium and other metal lines'
    elif (type == 'F'):
        color = 'yellow-white'
        temperature = '6000 - 7500'
        madeof = 'Strong hydrogen, ionized calium and sodium lines and many lines of other ionized and neutral metals'
    elif (type == 'G'):
        color = 'yellow'
        temperature = '5200 - 6000'
        madeof = 'Weaker hydrogen lines, strong ionized calium and sodium lines and many lines of other ionized and neutral metals'
    elif (type == 'K'):
        color = 'orange'
        temperature = '3700 - 5200'
        madeof = 'Very weak hydorgen lines, strong ionized calium and sodium lines and many lines of other neutral metals'
    elif (type == 'M'):
        color = 'red'
        temperature = '2400 - 3700'
        madeof = 'Strong lines of neutral metals and molecular bands of titanium oxide dominate'
    elif (type == 'L'):
        color = 'red'
        temperature = '1300 - 2400'
        madeof = 'Metal hydride lines and akali metal lines'
    elif (type == 'T'):
        color = 'magenta'
        temperature = '700 - 1300'
        madeof = 'Methane lines'
    elif (type == 'Y'):
        color = 'infrared'
        temperature = '< 700'
        madeof = 'Ammonia lines'
    spectraltypeinfo.append(color, temperature, madeof)
    return spectraltypeinfo

def getvisibility(id):
    df = get_data_fast()
    df_grouped = df.groupby(['id'])
    luminosity = df_grouped['Vmag'][id]
    visible = df_grouped['BV'][id]
    visibility = luminosity * visible
    return visibility

