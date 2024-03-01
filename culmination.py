import datetime
import math
import numpy
import ephem

#from algorithm import stars
stars = [278.3470833333333, 278.2079166666667, 278.83874999999995, 278.75999999999993]
longitude = 4.84357
lattitude = 52.34523

def degrees_to_radians(x):
    radians = math.radians(x)
    return radians

def average_angle(angles):
    # angles measured in radians
    x_sum = numpy.sum([math.sin(x) for x in angles])
    y_sum = numpy.sum([math.cos(x) for x in angles])
    x_mean = x_sum / float(len(angles))
    y_mean = y_sum / float(len(angles))
    return numpy.arctan2(x_mean, y_mean)

def radians_to_time_of_day(x):
    # radians are measured clockwise from north and represent time in a 24-hour circle
    seconds_from_midnight = int(float(x) / (2.0 * math.pi) * 24.0 * 60.0 * 60.0)
    if seconds_from_midnight < 0:
        seconds_from_midnight = seconds_from_midnight + 24 * 3600
    hour = seconds_from_midnight // 3600
    minute = (seconds_from_midnight % 3600) // 60
    second = seconds_from_midnight % 60
    return datetime.time(hour, minute, second)

def average_times_of_day(x):
    # input datetime.datetime array and output datetime.time value
    angles = [degrees_to_radians(y) for y in x]
    avg_angle = average_angle(angles)
    return radians_to_time_of_day(avg_angle)

const_avg_time = average_times_of_day(stars)

Long = longitude      #Longitude of location in question
LongDeg = int(Long)
LongMin = (Long - int(Long))*60
LongSec = (LongMin - int(LongMin))*60
LongMin = int(LongMin)
LongSec = int(LongSec)

TD = datetime.datetime.utcnow()

while True:
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
    local_sid_time = datetime.time(LSThh, LSTmm, LSTss)
    time_to_culmination = datetime.datetime.combine(datetime.date.min, const_avg_time) - datetime.datetime.combine(datetime.date.min, local_sid_time)
    culmination_time = TD.replace(microsecond=0, second=0) + time_to_culmination

    twilight = ephem.Observer()

    #PyEphem takes and returns only UTC times.
    twilight.date = culmination_time.replace(hour=12, minute=0, second=0)

    #Location of Fredericton, Canada
    twilight.lon  = str(longitude)       #Note that lon should be in string format
    twilight.lat  = str(lattitude)      #Note that lat should be in string format
    twilight.elev = 0
    twilight.pressure= 0
    twilight.horizon = '-0:34'

    twilight.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
    beg_twilight=twilight.previous_rising(ephem.Sun(), use_center=True) #Begin civil twilight
    end_twilight=twilight.next_setting   (ephem.Sun(), use_center=True) #End civil twilight

    if culmination_time < end_twilight.datetime() and culmination_time > beg_twilight.datetime():
        TD = TD + datetime.timedelta(days=1)
    else:
        break
print("The constellation will be visible on its culmination at", culmination_time, "UTC,", beg_twilight.datetime() - culmination_time, "before twilight.")