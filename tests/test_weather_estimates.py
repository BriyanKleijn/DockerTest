import unittest
import datetime as dt

import sys
sys.path.append('./weather_predictions/')
sys.path.append('./data/weather_data_knmi/')

from weather_estimates import weather_estimates as we
import knmi


class WeatherEstimateTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.lon_heino = 6.261719951959382
        self.lat_heino = 52.433870304890775
        self.start_date = dt.datetime(2020, 1, 1, 0)
        self.end_date = dt.datetime(2020, 1, 2, 0)
        self.estimate = we(lon=self.lon_heino, lat=self.lat_heino, start_date=self.start_date, end_date=self.end_date)


    # def test_get_temperature_calculate_heino(self):
    #     # Arrange
    #     df_stations = knmi.get_closest_stations(lon=self.lon_heino, lat=self.lat_heino, N=6)
    #     df_stations_without_heino = df_stations.loc[df_stations['NAME'] != 'HEINO']
    #     self.estimate.nearest_stations = df_stations_without_heino
    #     expected = self.estimate.data.loc[(self.estimate.data['STN'] == 27)]['T']
    #     print(expected)
    #     # # Act
    #     actual = self.estimate.get_temperature()['temperature']
    #     print(actual)
    #     # # Assert
    #     self.assertAlmostEqual(True, True)
if __name__ == '__main__':
    unittest.main()
