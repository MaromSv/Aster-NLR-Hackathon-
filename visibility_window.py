import numpy as np
import pandas as pd
import datetime
import math
import numpy
import ephem
from data import get_star_data_df

df = get_star_data_df()

longitude = 4.84357
lattitude = 52.34523

######Calculate beginning and end of darkness (end and beginning of twilight)#######
twilight = ephem.Observer()
#PyEphem takes and returns only UTC times.
twilight.date = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

#Location of Fredericton, Canada
twilight.lon  = str(longitude)       #Note that lon should be in string format
twilight.lat  = str(lattitude)      #Note that lat should be in string format
twilight.elev = 0
twilight.pressure= 0
twilight.horizon = '-0:34'

twilight.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
end_twilight=twilight.next_setting   (ephem.Sun(), use_center=True) #End civil twilight
twilight.date = twilight.date.datetime() + datetime.timedelta(days=1)
beg_twilight=twilight.previous_rising(ephem.Sun(), use_center=True) #Begin civil twilight

######Convert times to sidereal######
Long = longitude      #Longitude of location in question
LongDeg = int(Long)
LongMin = (Long - int(Long))*60
LongSec = (LongMin - int(LongMin))*60
LongMin = int(LongMin)
LongSec = int(LongSec)

for i in range(2):
    if i==0:
        TD = end_twilight.datetime()
    elif i==1:
        TD = beg_twilight.datetime()

    #split TD into individual variables for month, day, etc. and convert to floats:
    YY = float(TD.year)
    MM = float(TD.month)
    DD = float(TD.day)
    hh = float(TD.hour)
    mm = float(TD.minute)

    #convert mm to fractional time:
    mm = mm/60

    #reformat UTC time as fractional hours:
    UT = hh+mm

    #calculate the Julian date:
    JD = (367*YY) - int((7*(YY+int((MM+9)/12)))/4) + int((275*MM)/9) + DD + 1721013.5 + (UT/24)

    #calculate the Greenwhich mean sidereal time:
    GMST = 18.697374558 + 24.06570982441908*(JD - 2451545)
    GMST = GMST % 24    #use modulo operator to convert to 24 hours
    GMSTmm = (GMST - int(GMST))*60          #convert fraction hours to minutes
    GMSTss = (GMSTmm - int(GMSTmm))*60      #convert fractional minutes to seconds
    GMSThh = int(GMST)
    GMSTmm = int(GMSTmm)
    GMSTss = int(GMSTss)

    #Convert to the local sidereal time by adding the longitude (in hours) from the GMST.
    #(Hours = Degrees/15, Degrees = Hours*15)
    Long = Long/15      #Convert longitude to hours
    LST = GMST+Long     #Fraction LST. If negative we want to add 24...
    if LST < 0:
        LST = LST +24
    LSTmm = (LST - int(LST))*60          #convert fraction hours to minutes
    LSTss = (LSTmm - int(LSTmm))*60      #convert fractional minutes to seconds
    LSThh = int(LST)
    LSTmm = int(LSTmm)
    LSTss = int(LSTss)

    if i==0:
        begin_dark_sid = datetime.time(LSThh, LSTmm, LSTss)
    elif i==1:
        end_dark_sid = datetime.time(LSThh, LSTmm, LSTss)

output = pd.DataFrame(columns=df.columns)
for x in df:
    window = np.arccos(-math.tan(math.radians(df["coord_ra_deg"].iloc(x)))*math.tan(math.radians(52)))/math.pi*24
    lower_limit = df["coord_ra_deg"].iloc(x)/360*24 - window / 2
    upper_limit = df["coord_ra_deg"].iloc(x)/360*24 + window / 2
    if end_dark_sid > begin_dark_sid:
        if lower_limit > begin_dark_sid and lower_limit < end_dark_sid:
            output.loc[len(output.index)] = df.iloc[x]
        elif upper_limit > begin_dark_sid and upper_limit < end_dark_sid:
            output.loc[len(output.index)] = df.iloc[x]
        elif lower_limit < begin_dark_sid and upper_limit > end_dark_sid:
            output.loc[len(output.index)] = df.iloc[x]
        elif upper_limit < lower_limit:
            if lower_limit < end_dark_sid:
                output.loc[len(output.index)] = df.iloc[x]
    elif upper_limit > lower_limit:
        if upper_limit > begin_dark_sid:
            output.loc[len(output.index)] = df.iloc[x]
    elif upper_limit < lower_limit:
        output.loc[len(output.index)] = df.iloc[x]

return output


