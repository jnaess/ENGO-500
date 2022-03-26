import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from polygon import Polygon
from point import Point
from geomTools import GeomTools
from positionGenerator import PositionGenerator

class ErrorSimulator():
    """
    Simulates the error which is incorporated in pathFollower
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
            self.erros = [Point(), ... , Point()] errors in order of how they happened for plotting purposes
            self.total_error, Point() of the cumulative error
        """
        self.is_real = False
        self.errors = []
        self.total_error = Point(0,0)

    def update_PG(self, pg):
        """
        Desc:
            Updated the error simulator's PositionGenerator for the next add_error
        Input:
            pg, PositionGenerator() for the drift error in error per meter travelled by the tractor
        Output:
        """
        self.pg=pg
        
    def add_error(self, interval):
        """
        Desc:
            returns the error to be added either E, N, or H | default value is 0
        Input:
            interval, float --> the distance that the error is being multiplied by
            pg, PositionGenerator() for the drift error in error per meter travelled by the tractor
        Output:
            return --> float | default 0
        """        
        if self.is_real:
            print("is real!")
            #then it is real and needs an error to be added
            
            #generate new statistical random error
            self.pg.generate_one()

            e = interval*self.pg.unique_pnt.E()
            n = interval*self.pg.unique_pnt.N()

            self.errors.append(Point(e,n))

            self.total_error.e = self.total_error.E()+e
            self.total_error.n = self.total_error.N()+n
        
    def E(self):
        """
        Desc:
            if self.is_real = True --> returns the most previous easting error
            otherwise returns 0 because it is a true point that doesn't have an error
        Input:
        Output:
            returns --> Easting error --> float
        """
        if self.is_real:
            #then has an error and therefore the error has been generated
            return self.errors[-1].E()
        else:
            return 0
        
    def N(self):
        """
        Desc:
            if self.is_real = True --> returns the most previous northing error
            otherwise returns 0 because it is a true point that doesn't have an error
        Input:
        Output:
            returns --> northing error --> float
        """
        if self.is_real:
            #then has an error and therefore the error has been generated
            return self.errors[-1].N()
        else:
            return 0
