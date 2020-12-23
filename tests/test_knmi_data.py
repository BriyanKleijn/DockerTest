import unittest
import datetime as dt

# For information about running tests see testplan
import sys
sys.path.append('./weather_predictions/')
sys.path.append('./data/weather_data_knmi/')

import knmi


class TestKnmi(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.begin_date = dt.datetime(2020, 11, 11, 11)
        self.end_date = dt.datetime(2020, 11, 12, 19)
        self.data = knmi.get_knmi_data(begin_date=self.begin_date, end_date=self.end_date)

    def test_get_knmi_data_first_entry_matches_start_date(self):
        # Arrange
        excepted = self.begin_date

        # Act
        first_row = self.data.iloc[0]
        actual = dt.datetime.strptime(str(int(first_row['YYYYMMDD'])), '%Y%m%d') + dt.timedelta(hours=first_row['HH'])

        # Assert
        self.assertEqual(excepted, actual)

    def test_get_knmi_data_last_entry_matches_end_date(self):
        # Arrange
        excepted = self.end_date

        # Act
        last_row = self.data.iloc[-1]
        actual = dt.datetime.strptime(str(int(last_row['YYYYMMDD'])), '%Y%m%d') + dt.timedelta(hours=last_row['HH'])

        # Assert
        self.assertEqual(excepted, actual)

    def test_get_knmi_data_correct_columns_are_available(self):
        # Arrange
        expected = ['STN', 'YYYYMMDD', 'HH', 'FF', 'T', 'Q']

        # Act
        actual = self.data.columns.to_list()

        # Assert
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
