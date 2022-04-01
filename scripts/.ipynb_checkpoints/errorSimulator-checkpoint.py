import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from polygon import polygon
from point import Coord
from geomTools import GeomTools
from positionGenerator import PositionGenerator
from errorDocumentor import ErrorDocumentor

class ErrorSimulator(ErrorDocumentor):
    """
    Simulates the error which is incorporated in pathFollower
    """
    
    def __init__(self, drift_on = False, jump_on = False):
        """
        Desc:
        Input:
        Output:
            self.errors = [Coord(), ... , Coord()] errors within each interval (drift and jump added together)
            self.drift_errors = [Coord(), ... , Coord()]
            self.jump_errors = [Coord(), ... , Coord()]
            self.total_error, Coord() of the cumulative error
            self.is_real = False, whether or not this is a "Real and error filled" or "True point" --> which does not record errors because they're always zero
            self.drift_on = False, whether or not to generate a drift error
            self.jump_on = False, whether or not to generate a jump error
            self.easting_drift_const
            self.northing_drift_const
        """
        ErrorDocumentor.__init__(self)
        
        self.jump_happened = False
        self.is_real = False
        self.drift_on = drift_on
        self.jump_on = jump_on
        
        
        self.easting_drift_const = .1 #average drift per meter
        self.northing_drift_const = .1 #average drift per meter
        
        self.total_error = Coord(0,0)
        self.errors = []
        self.drift_errors = []
        self.jump_errors = []
        
        self.pg = PositionGenerator()

    def update_PG(self, pg):
        """
        Desc:
            Updated the error simulator's PositionGenerator for the next add_error
        Input:
            pg, PositionGenerator() for the drift error in error per meter travelled by the tractor
        Output:
        """
        self.pg=pg
        
    def add_error(self, interval, start = False):
        """
        Desc:
            returns the error to be added either E, N, or H | default value is 0
        Input:
            interval, float --> the distance that the error is being multiplied by (calculated to be 1m --> then scaled by interval distance)
            pg, PositionGenerator() for the drift error in error per meter travelled by the tractor
        Output:
            return --> float | default 0
        """   
        if start:
            #then it is real and needs an error to be added
            
            self.drift_e = 0
            self.drift_n = 0
            
            self.jump_e = 0
            self.jump_n = 0

            #record total epoch error
            self.errors.append(Coord(self.drift_e+self.jump_e,self.drift_n+self.jump_n))

            self.total_error.e = self.total_error.E()+self.drift_e+self.jump_e
            self.total_error.n = self.total_error.N()+self.drift_n+self.jump_n
            
            self.record_errors()
            
        elif self.is_real:
            """
            TODO:
                Cut increments if the next point excedes the outerfield
            """
            #then it is real and needs an error to be added
            
            #generate drift error
            self.add_drift_error(interval)
            
            #generate jump error
            self.add_jump_error(interval)

            #record total epoch error
            self.errors.append(Coord(self.drift_e+self.jump_e,self.drift_n+self.jump_n))

            self.total_error.e = self.total_error.E()+self.drift_e+self.jump_e
            self.total_error.n = self.total_error.N()+self.drift_n+self.jump_n
            
            self.record_errors()
            
    def add_drift_error(self, interval):
        """
        Desc:
            Generated self.e and self.n drift error in relative to interval length
        Input:
            interval, float --> the distance that the error is being multiplied by (calculated to be 1m --> then scaled by interval distance)
            pg, PositionGenerator() for the drift error in error per meter travelled by the tractor
        Output:
            self.drift_e --> current easting drift error
            self.drift_n --> current northing drift error
        """
        if self.drift_on:
            #generate new statistical random error
            self.pg.generate_one()

            #generate drift error
            self.drift_e = interval*self.pg.unique_pnt.E()*self.easting_drift_const
            self.drift_n = interval*self.pg.unique_pnt.N()*self.northing_drift_const
            
        else:
            #then the error for this is zero
            #generate drift error
            self.drift_e = 0
            self.drift_n = 0
            
        #record drift error
        self.drift_errors.append(Coord(self.drift_e,self.drift_n))
        
    def add_jump_error(self, interval):
        """
        Desc:
            ***INCOMPLETE**
            Generated self.e and self.n jump error in relative to interval length
        Input:
            interval, float --> the distance that the error is being multiplied by (calculated to be 1m --> then scaled by interval distance) **maybe?? for jupm error...**
            pg, PositionGenerator() for the drift error in error per meter travelled by the tractor
        Output:
            self.jump_e --> current easting drift error
            self.jump_n --> current northing drift error
        """
        if self.jump_on:
            #set to zero because probability is not get included
            self.jump_e = 0
            self.jump_n = 0
            
            if abs(self.jump_e) > 0 or abs(self.jump_n) > 0:
                self.jump_happened = True
            else:
                self.jump_happened = False
        else:
            #then the error for this is zero
            #generate jump error
            self.jump_e = 0
            self.jump_n = 0
        
        #record jump error
        self.jump_errors.append(Coord(self.jump_e,self.jump_n))
        
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
