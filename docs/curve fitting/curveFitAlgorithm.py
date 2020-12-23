from numpy import arange
from numpy import sin
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
import math


class ErrorStats:

    def __init__(self, y, y_line, x_line):
        self.y = y
        self.y_line = y_line
        self.x_line = x_line
        self.total_error_var = self.total_error()
        self.min_error_var = self.min_error()
        self.max_error_var = self.max_error()
        self.average_error_var = self.average_error()
        self.rmse_var = self.rmse()
    # The Calculations #

    def total_error(self):
        """Calculates the total error"""
        
        total_error_var = 0

        for j in range(self.y.size-1):
            res = self.y[j] - self.y_line[j]
            if res < 0:
                res = res * -1

            total_error_var = total_error_var + res

        return total_error_var

    def min_error(self):
        """Calculates the minimal error"""
        
        res = self.y[0] - self.y_line[0]
        if res < 0:
            res = res * -1

        min_error_var = res

        for j in range(self.y.size-1):
            res = self.y[j] - self.y_line[j]
            if res < 0:
                res = res * -1

            if res < min_error_var:
                min_error_var = res

        return min_error_var

    def max_error(self):
        """Calculates the maximal error"""
        
        max_error_var = 0

        for j in range(self.y.size-1):
            res = self.y[j] - self.y_line[j]
            if res < 0:
                res = res * -1

            if res > max_error_var:
                max_error_var = res

        return max_error_var

    def average_error(self):
        """Calculates the average error"""
        
        average_error_var = self.get_total_error()/self.y.size
        return average_error_var

    def rmse(self):
        rmse_var = mean_squared_error(self.y, self.y_line, squared=False)
        return rmse_var

    # Error Stats Return #
    # Returns the total error, you can assume that this has already been calculated
    def get_total_error(self):
        """
        The total error shows the sum of all the differences between the actual data and the curve fit data.
        """
        return self.total_error_var
    # Returns the minimal error, you can assume that this has already been calculated

    def get_min_error(self):
        """
        The minimum error shows the lowest difference between the actual data and the curve fit data at a certain point in the graph.
        """
        return self.min_error_var
    # Returns the maximal error, you can assume that this has already been calculated

    def get_max_error(self):
        """
        The maximum error shows the highest difference between the actual data and the curve fit data at a certain point in the graph.
        """
        return self.max_error_var
    # Returns the average error, you can assume that this has already been calculated

    def get_average_error(self):
        """
        The average error shows the average difference between the actual data and the curve fit data through the entire graph.
        """
        return self.average_error_var

    def get_rmse(self):
        """
        The average error shows the average difference between the actual data and the curve fit data through the entire graph.
        """
        return self.rmse_var


class Curve_Fit_Algorithm:
    """ This is the base abstract class for every curve fit algorithm\n
        Dont use this class as standalone, instead use one of the algorithmes included in the *curveFitAlgorithm.py*"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_line = x
        self.calculate()
        self.calculate_stats()

    def calculate(self):
        """
        Calculates the curve and the error stats of the curve
        """

        print(" This is the base abstract class for every curve fit algorithm. Dont use this class as standalone, instead use one of the algorithmes included in the *curveFitAlgorithm.py*")
        return False

    def calculate_stats(self):
        """Calculating the error data"""
        
        stats = ErrorStats(self.y, self.y_line, self.x)
        self.total_error = stats.get_total_error()
        self.min_error = stats.get_min_error()
        self.max_error = stats.get_max_error()
        self.average_error = stats.get_average_error()
        self.rmse = stats.get_rmse()
        return True

    # Curve fit lines #
    # Returns the x line of the curve
    def get_x_line(self):
        return self.x_line
    # Returns the y line of the curve

    def get_y_line(self):
        return self.y_line

    # Error Stats #
    def get_rmse(self):
        """Returns rms"""
        
        return self.rmse

    def get_total_error(self):
        """Returns the total error of the curve"""
        
        return self.total_error

    def get_min_error(self):
        """Returns the minimal error of the curve"""
        
        return self.min_error

    def get_max_error(self):
        """Returns the maximal error of the curve"""
        
        return self.max_error

    def get_average_error(self):
        """Returns the average error of the curve"""
        return self.average_error
    
    def get_detail(self):
        """Returns the details about the algorithm"""
        return self.detail


class LinearFit(Curve_Fit_Algorithm):
    """Linear fit algorithm class"""

    def objective(self, x, a, b):

        return a * x + b

    def calculate(self):
        """
        Calculates the curve fit with the linear fit algorithm
        """

        popt, _ = curve_fit(self.objective, self.x, self.y)
        a, b = popt

        self.y_line = self.objective(self.x_line, a, b)

        return True


class FifthDegreePolynomialFit(Curve_Fit_Algorithm):
    """
    Fifth degree fit
    """

    def objective(self, x, a, b, c, d, e, f):
        return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + f

    def calculate(self):
        """
        Calculates the curve fit with the fifth degree polynomial regression algorithm
        """

        popt, _ = curve_fit(self.objective, self.x, self.y)
        a, b, c, d, e, f = popt
        self.y_line = self.objective(self.x_line, a, b, c, d, e, f)

        return True


class NonLinearLeastSquaresFit(Curve_Fit_Algorithm):
    """Non linear least squares fit algorithm class"""

    def objective(self, x, a, b, c):
        return a * sin(b * x) + c

    def calculate(self):
        """
        Calculates the curve fit with the non-linear least squares algorithm
        """
        popt, _ = curve_fit(self.objective, self.x, self.y)
        a, b, c = popt
        self.y_line = self.objective(self.x_line, a, b, c)

        return True


class SineWaveFit(Curve_Fit_Algorithm):
    """Sine wave fit algorithm class"""

    def objective(self, x, a, b, c, d):
        return a * sin(b - x) + c * x**2 + d

    def calculate(self):
        """
        Calculates the curve fit with the sine wave algorithm
        """

        popt, _ = curve_fit(self.objective, self.x, self.y)
        a, b, c, d = popt
        self.y_line = self.objective(self.x_line, a, b, c, d)

        return True


class PolynomialRegressionFit(Curve_Fit_Algorithm):
    """Polynomial regression fit algorithm class"""

    def objective(self, x, a, b, c):
        return a * x + b * (x * x) + c

    def calculate(self):
        """
        Calculates the curve fit with the polynomial regression algorithm
        """

        popt, _ = curve_fit(self.objective, self.x, self.y)
        a, b, c = popt

        self.y_line = self.objective(self.x_line, a, b, c)

        return True
