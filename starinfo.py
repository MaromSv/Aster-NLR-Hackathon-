import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns
from data import get_star_data_df

def spectraltypeinfo(type):
    spectraltypeinfo = []
    color = ''
    temperature = ''
    madeof = ''
    if (type == 'O'):
        color += 'blue'
        temperature += '> 30000K'
        madeof += 'Mainly neutral and ionized helium lines and weak hydrogen lines'
    elif (type == 'B'):
        color += 'blue-white'
        temperature +=  '10000 - 30000K'
        madeof += 'Neutral helium lines and strong hydrogen lines'
    elif (type == 'A'):
        color += 'white'
        temperature += '7500 - 10000K'
        madeof += 'Strongest hydrogen lines weak ionized calium and other metal lines'
    elif (type == 'F'):
        color += 'yellow-white'
        temperature += '6000 - 7500K'
        madeof += 'Strong hydrogen, ionized calium and sodium lines and many lines of other ionized and neutral metals'
    elif (type == 'G'):
        color += 'yellow'
        temperature += '5200 - 6000K'
        madeof += 'Weaker hydrogen lines, strong ionized calium and sodium lines and many lines of other ionized and neutral metals'
    elif (type == 'K'):
        color += 'orange'
        temperature += '3700 - 5200K'
        madeof += 'Very weak hydorgen lines, strong ionized calium and sodium lines and many lines of other neutral metals'
    elif (type == 'M'):
        color += 'red'
        temperature += '2400 - 3700K'
        madeof += 'Strong lines of neutral metals and molecular bands of titanium oxide dominate'
    elif (type == 'L'):
        color += 'red'
        temperature += '1300 - 2400K'
        madeof += 'Metal hydride lines and akali metal lines'
    elif (type == 'T'):
        color += 'magenta'
        temperature += '700 - 1300K'
        madeof += 'Methane lines'
    elif (type == 'Y'):
        color += 'infrared'
        temperature += '< 700K'
        madeof += 'Ammonia lines'
    spectraltypeinfo.append(color)
    spectraltypeinfo.append(temperature)
    spectraltypeinfo.append(madeof)
    return spectraltypeinfo

def getvisibility(id):
    df = get_star_data_df()
    df_grouped = df.groupby(['id'])
    luminosity = df_grouped['Vmag'][id]
    visible = df_grouped['BV'][id]
    visibility = luminosity * visible
    return visibility

def getspecifics(id):
    info = {
        'MWtype': 'unknown', 'spectraltype' : 'unknown', 'spectralsubtype' : 'unknown', 'luminosityclass' : 'unknown', 'color' : 'unknown', 
        'temperature' : 'unknown', 'madeof' : 'unknown', 'name' : 'unknown', 'distance' : 'unknown', 'numberofstars' : 1
    }
    df = get_star_data_df()
    df_grouped = df.set_index(['id'])
    spectraltypefull = df_grouped['spectral_type_full'][id]
    specs = dissectspectraltype(spectraltypefull)
    info['MWtype'] = specs[0][0]
    info['spectraltype'] = specs[0][1]
    info['spectralsubtype'] = specs[0][3]
    info['luminosityclass'] = specs[0][4]
    info['color'] = specs[0][2][0]
    info['temperature'] = specs[0][2][1]
    info['madeof'] = specs[0][2][2]
    info['numberofstars'] = len(specs)
    name = df_grouped['name'][id]
    info['name'] = name
    distance = 3.26/(df_grouped['Parallax'][id])
    if (not distance == np.nan):
        distance = 'unknown'
    info['distance'] =  distance

    return info

def dissectspectraltype(spectraltypefull):
    maintypeindex = 0
    maintypes = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    stars = 1
    i = 0
    while i < len(spectraltypefull):
        if (spectraltypefull[i] in maintypes):
            maintypeindex = i
            break
        i = i + 1
    Mounttype = spectraltypefull[0:maintypeindex]
    spectraltype = spectraltypefull[maintypeindex]
    typeinfo = spectraltypeinfo(spectraltype)
    spectraltypefull = spectraltypefull[maintypeindex+1:len(spectraltypefull)]
    Wilson = ''
    if (Mounttype[0] == 's'):
        Wilson = 'sub'
        Mounttype = Mounttype[1:i]
    if (Mounttype[0] == 'g'):
        Wilson = Wilson + 'giant'
    elif (Mounttype[0] == 'd'):
        Wilson = Wilson + 'dwarf' 
    elif (Mounttype[0] == 'c'):
        Wilson = 'supergiant'
    if (Mounttype[len(Mounttype) - 1] == ':'):
        Wilson = Wilson + ' (uncertain)'
    i = 0
    luminosityindex = 0
    while i < len(spectraltypefull):
        if (spectraltypefull[i].isnumeric()):
            i = i + 1
        elif (spectraltypefull[i] in ['.', '-']):
            if(spectraltypefull[i+1].isnumeric()):
                i = i + 2
        elif (spectraltypefull[i] == '+'):
            stars = stars + 1
        luminosityindex = i
        break
    spectralsubclass = spectraltypefull[0:luminosityindex]
    spectraltypefull = spectraltypefull[luminosityindex:len(spectraltypefull) - 1]
    luminosityclasses = ['I', 'V', '-', '/', 'a', 'b']
    end = 0
    i = 0
    while i < len(spectraltypefull):
        if (spectraltypefull[i] in luminosityclasses):
            i = i + 1
        if (spectraltypefull[i] == '+'):
            stars = stars + 1
        end = i
        break
    luminositiyclass = spectraltypefull[0:end]
    multiclass = False
    seperatorindex = 0
    i = 0
    while i < len(luminositiyclass):
        if (luminositiyclass[i] in ['-', '/']):
            multiclass = True
            seperatorindex = i
        i = i + 1
    if (multiclass):
        class1 = romantoclass(luminositiyclass[0:seperatorindex])
        class2 = romantoclass(luminositiyclass[seperatorindex + 1:len(luminositiyclass) - 1])
        if (luminositiyclass[seperatorindex] == '-'):
            luminositiyclass = 'between ' + class1 + ' and ' + class2
        else:
            luminositiyclass = class1 + ' or ' + class2
    else:
        luminositiyclass = romantoclass(luminositiyclass)
    spectraltypefull = spectraltypefull[end:len(spectraltypefull) - 1]
    if (stars == 1):
        i = 0
        while i < len(spectraltypefull):
            if (spectraltypefull[i] == '+'):
                stars = stars + 1
                break
            i = i + 1
    starinfo = []
    starinfo.append(Wilson)
    starinfo.append(spectraltype)
    starinfo.append(typeinfo)
    starinfo.append(spectralsubclass)
    starinfo.append(luminositiyclass)
    specs = []
    specs.append(starinfo)
    if (stars > 1):
        dissectspectraltype(spectraltypefull)
    return specs

def romantoclass(roman):
    luminosityclass = ''
    if (roman == 'V'):
        luminosityclass += 'a main-sequence star'
    elif (roman == 'IV'):
        luminosityclass += 'a subgiant'
    elif (roman == 'III'):
        luminosityclass += 'a normal giant'
    elif (roman == 'II'):
        luminosityclass += 'a bright giant'
    elif (roman == 'I'):
        luminosityclass += 'a supergiant'
    elif (roman == 'Ib'):
        luminosityclass += 'a less luminous supergiant'
    elif (roman == 'Iab'):
        luminosityclass += 'an intermediate-size supergiant'
    elif (roman == 'Ia'):
        luminosityclass += 'a luminous supergiant'
    return luminosityclass

print(getspecifics(1))