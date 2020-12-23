# imports
import requests
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import scipy.optimize
import io
import numpy as np
import datetime

# workaround for importing classes
import sys
sys.path.append('./weather_predictions/')
import knmi


class weather_estimates:
    """
    Class that is used to estimate weather given coordinates and a timeslot.
    """

    def __init__(self, lon: float, lat: float, start_date: datetime, end_date: datetime = None):
        """
        Initialize class and get data from KNMI api
        """
        self.nearest_stations = knmi.get_closest_stations(lon, lat, N=3)
        if (end_date == None):
            end_date = start_date + datetime.timedelta(days=1)

        if (start_date > end_date):
            raise Exception("Start date is higher than ending date")
        self.lon = lon
        self.lat = lat
        self.start_date = start_date
        self.end_date = end_date
        self.data = knmi.get_knmi_data(start_date, end_date)

    def get_temperature(self) -> pd.DataFrame:
        """
        Function that estimates the temperature in a given location within a given timeslot using KNMI data and the lon, lat, start_time and end_time of the class. 
        Returns a dataframe with a temperature in °C at the given timestamp.  
        """
        # Dictionary used to store dates and temps
        dictionary = {}

        def f_linear(X, a, b, c):
            return a * X[:, 0] + b * X[:, 1] + c

        start_date = self.start_date
        end_date = self.end_date

        # Calculate an estimate temperature for every hour
        while start_date <= end_date:
            hour = None
            used_date = None

            # Parse date to compareable values
            if (start_date.hour == 0):
                used_date = start_date - datetime.timedelta(hours=1)
                hour = 24
            else:
                used_date = start_date
                hour = used_date.hour

            date_string = f'{used_date.year}{used_date.month:02d}{used_date.day:02d}'
            # Select data that will be used to calculate temperature
            df_datehour = self.data[((self.data['HH'] == hour)) & (
                self.data['YYYYMMDD'] == int(date_string))].set_index('STN')
            df_for_fit = self.nearest_stations.join(df_datehour, how='inner')

            # Get values that are needed in order to calculate temperature
            x = df_for_fit[['LON(east)', 'LAT(north)']].values
            y = df_for_fit['T'].values

            if (y.size == 0):
                raise Exception(
                    f"No temperatures are available for date: {used_date}")

            # Fit curve and calculate temperature
            popt, pcov = scipy.optimize.curve_fit(f_linear, x, y)

            # Add time and temperature to dictionary
            temperature = f_linear(
                np.array([[self.lon, self.lat]]), popt[0], popt[1], popt[2])[0]
            dictionary[start_date] = temperature

            start_date = start_date + datetime.timedelta(hours=1)

        # Convert dictionary to dataframe and return the result
        return pd.DataFrame.from_dict(
            dictionary, orient='index', columns=['temperature'])

    def get_wind_speed(self) -> pd.DataFrame:
        """
        Function that estimates the wind speed in a given location within a given timeslot using KNMI data and the lon, lat, start_time and end_time of the class.
        Returns a dataframe with an average wind speed of the last 10 minutes in m/s of the timestamp.
        """
        # Dictionary used to store dates and temps
        dictionary = {}

        def f_linear(X, a, b, c):
            return a * X[:, 0] + b * X[:, 1] + c

        start_date = self.start_date
        end_date = self.end_date

        # Calculate an estimate temperature for every hour
        while start_date <= end_date:
            hour = None
            used_date = None

            # Parse date to compareable values
            if (start_date.hour == 0):
                used_date = start_date - datetime.timedelta(hours=1)
                hour = 24
            else:
                used_date = start_date
                hour = used_date.hour

            date_string = f'{used_date.year}{used_date.month:02d}{used_date.day:02d}'

            # Select data that will be used to calculate temperature
            df_datehour = self.data[((self.data['HH'] == hour)) & (
                self.data['YYYYMMDD'] == int(date_string))].set_index('STN')
            df_for_fit = self.nearest_stations.join(df_datehour, how='inner')

            # Get values that are needed in order to calculate temperature
            x = df_for_fit[['LON(east)', 'LAT(north)']].values
            y = df_for_fit['FF'].values

            if (y.size == 0):
                raise Exception(
                    f"No temperatures are available for date: {used_date}")

            # Fit curve and calculate temperature
            popt, pcov = scipy.optimize.curve_fit(f_linear, x, y)

            # Add time and wind speed to dictionary
            wind_speed = f_linear(
                np.array([[self.lon, self.lat]]), popt[0], popt[1], popt[2])[0]
            dictionary[start_date] = wind_speed

            start_date = start_date + datetime.timedelta(hours=1)

        # Convert dictionary to dataframe and return the result
        return pd.DataFrame.from_dict(
            dictionary, orient='index', columns=['wind_speed'])

    def get_horizontal_irradiation(self) -> pd.DataFrame:
        """
        Function that estimates the horizontal irradiation in a given location within a given timeslot using KNMI data and the lon, lat, start_time and end_time of the class.
        Returns a dataframe with the global irradiation in W/m² per hour slot.
        """
        # Dictionary used to store dates and temps
        dictionary = {}

        def f_linear(X, a, b, c):
            return a * X[:, 0] + b * X[:, 1] + c

        start_date = self.start_date
        end_date = self.end_date

        # Calculate an estimate horizontal irradiation for every hour
        while start_date <= end_date:
            hour = None
            used_date = None

            # Parse date to compareable values
            if (start_date.hour == 0):
                used_date = start_date - datetime.timedelta(hours=1)
                hour = 24
            else:
                used_date = start_date
                hour = used_date.hour

            date_string = f'{used_date.year}{used_date.month:02d}{used_date.day:02d}'

            # Select data that will be used to calculate temperature
            df_datehour = self.data[((self.data['HH'] == hour)) & (
                self.data['YYYYMMDD'] == int(date_string))].set_index('STN')
            df_for_fit = self.nearest_stations.join(df_datehour, how='inner')

            # Get values that are needed in order to calculate temperature
            x = df_for_fit[['LON(east)', 'LAT(north)']].values
            y = df_for_fit['Q'].values

            if (y.size == 0):
                raise Exception(
                    f"No temperatures are available for date: {used_date}")

            # Fit curve and calculate temperature
            popt, pcov = scipy.optimize.curve_fit(f_linear, x, y)

            # Add time and wind speed to dictionary
            irradiation = f_linear(
                np.array([[self.lon, self.lat]]), popt[0], popt[1], popt[2])[0]
            # Irradiation is converted from J/cm² to W/m² and rounded to 5 digits
            dictionary[start_date] = round(irradiation * (25 / 9), 5)

            start_date = start_date + datetime.timedelta(hours=1)

        # Convert dictionary to dataframe and return the result
        return pd.DataFrame.from_dict(dictionary, orient='index', columns=[
            'horizontal_irradiation'])
