# imports
#import requests
import pandas as pd
import datetime as dt
import io
from functools import lru_cache
from math import sin, cos, sqrt, atan2, radians

# variables
_url = r'http://projects.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi'
# All headers are neccesary to load the data correctly
_headerline = [i.strip() for i in "STN,YYYYMMDD,   HH,   DD,   FH,   FF,   FX,    T, T10N,   TD,   SQ,    Q,   DR,   RH,    P,   VV,    N,    U,   WW,   IX,    M,    R,    S,    O,    Y".split(',')]

# methods


@lru_cache(maxsize=32)
def _get_raw_knmi_data(begin_date: dt.datetime, end_date: dt.datetime) -> str:
    """Function to download the raw KNMI data out of the API"""

    # Create the post package
    data = {
        'byear': begin_date.year,
        'bmonth': begin_date.month,
        'bday': begin_date.day,
        'eyear': end_date.year,
        'emonth': end_date.month,
        'eday': end_date.day,
        'WIND': 'FF',
        'TEMP': 'T',
        'SUNR': 'Q'
    }

    # Do the actual post
    res = requests.post(_url, data=data)

    # Raise for errors
    res.raise_for_status()

    # Get rid of whitespaces, confuses Pandas
    text = res.text.replace(' ', '')

    return text


def get_knmi_data(begin_date: dt.datetime, end_date: dt.datetime) -> pd.DataFrame:
    """
    Function that downloads the KNMI data and converts it to a Pandas dataframe
    """
    starttime = begin_date.hour
    endtime = end_date.hour
    if (starttime == 0):
        begin_date = begin_date - dt.timedelta(hours=1)
        starttime = 24
    if (endtime == 0):
        end_date = end_date - dt.timedelta(hours=1)
        endtime = 24

    text = _get_raw_knmi_data(begin_date, end_date)

    df = pd.read_csv(io.StringIO(text), comment="#", names=_headerline)

    # Drop columns that are not used
    df.drop(columns=['DD', 'FH', 'FX', 'T10N', 'TD', 'SQ', 'DR', 'RH', 'P', 'VV', 'N', 'U', 'WW', 'IX', 'M', 'R', 'S', 'O', 'Y'], inplace=True, axis=1)

    # Only select what is needed
    start_date_int = int(f'{begin_date.year}{begin_date.month:02d}{begin_date.day:02d}')
    end_date_int = int(f'{end_date.year}{end_date.month:02d}{end_date.day:02d}')
    df = df.loc[((df['YYYYMMDD'] > start_date_int) & (df['YYYYMMDD'] < end_date_int)) | ((df['YYYYMMDD'] == start_date_int)
                                                                                         & (df['HH'] >= starttime)) | ((df['YYYYMMDD'] == end_date_int) & (df['HH'] <= endtime))]

    # Convert to usable values
    df['T'] = df['T'] / 10
    df['FF'] = df['FF'] / 10

    return df


def _get_stationinfo() -> pd.DataFrame:
    headerline = [i.strip() for i in "STN, LON(east), LAT(north), ALT(m), NAME".split(',')]

    with open('../data/weather_data_knmi/stations.txt', 'r') as f:
        txt = f.read()

    txt = txt.replace(' ', '')

    return pd.read_csv(io.StringIO(txt), comment="#", names=headerline).set_index('STN')


def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_closest_stations(lon: float, lat: float, N: int = 3) -> pd.DataFrame:
    """
    Function that gets N nearest stations given a longitude (lon) and latitude (lat)
    """
    df = _get_stationinfo()

    # Convert LAT(north) and LON(east) to float.
    df['LAT(north)'] = pd.to_numeric(df['LAT(north)'], downcast='float')
    df['LON(east)'] = pd.to_numeric(df['LON(east)'], downcast='float')

    # Calculate distance to stations from given coordinates.
    df['distance'] = df.apply(lambda row: _calculate_distance(lat, lon, row['LAT(north)'], row['LON(east)']), axis=1)
    df.sort_values('distance', inplace=True)

    return df.head(N)
