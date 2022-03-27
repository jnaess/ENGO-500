import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from polygon import Polygon
from point import Point
from geomTools import GeomTools
from pathGenerator import PathGenerator
from positionGenerator import PositionGenerator
from pathFollower import PathFollower
from errorSimulator import ErrorSimulator

class PassGenerator(PathGenerator):
    """
    Generates all start and end points of the paths, 
    then uses PathFollower to generate center points and direction vectors of each segment
    """
    
    def __init__(self, interval = 1, vertices = [Point(0,0), Point(10,0), Point(10,10), Point(0,10)], tractor_width = 1.5):
        """
        Desc:
        Input:
            interval, interval distance in 'm' to simulate distance between new measurements
        Output:
        """
        PathGenerator.__init__(self, vertices, tractor_width)
                    
        self.interval = interval
        
        self.es = ErrorSimulator()
        
        self.passes()
        
    def true_pass_points(self):
        """
        Desc:
            sets up the 'true' pass points
        Input:
        Output:
            self.lower_start, Point()
            self.upper_start, Point
            self.lower, PathFollower() of the lower inner rectangle true pass points
            self.upper, PathFollower() of the upper inner rectangle true pass points
        """
        self.pg_true = PositionGenerator(mean = Point(0,0, truth = True))
        
        #slightly off of a and b because of 1/2 of the width of a tractor used up
        self.lower_start = Point(self.a.E()+self.vec_a.E()*(self.tractor_width/2),
                           self.a.N()+self.vec_a.N()*(self.tractor_width/2))
        
        self.upper_start = Point(self.b.E()+self.vec_a.E()*(self.tractor_width/2),
                           self.b.N()+self.vec_a.N()*(self.tractor_width/2))
        
        self.es.is_real = False
        
        #these are where the tractor will end or start passes on the south side of the field
        self.lower = PathFollower(start = self.lower_start, 
                                  end = self.d, 
                                  interval = self.tractor_width,
                                 es = self.es)
        
        #these are where the tractor will end or start passes on the north side of the field
        self.upper = PathFollower(start = self.upper_start, 
                                  end = self.c, 
                                  interval = self.tractor_width,
                                     es = self.es)
        
    def passes(self):
        """
        Desc:
            sets up all passes
        Input:
        Output:
            self.true_passes
            self.real_passes --> incomplete
        """        
        self.true_pass_points()
        
        self.true_passes = []
        
        #not yet added to functionality
        self.real_passes = []
        
        if len(self.lower.segments) == len(self.upper.segments):
            #then probalby a rectangle as we wanted
            
            upward = True
            for i in range(len(self.lower.segments)):
                if upward:
                    self.es.is_real = False
                    #then go from bottom to top
                    self.true_passes.append(PathFollower(self.lower.segments[i],
                                                         self.upper.segments[i], 
                                                         interval = self.interval,
                                                        es = self.es))
                    
                else:
                    self.es.is_real = False
                    #then go from top to bottom
                    self.true_passes.append(PathFollower(self.upper.segments[i], 
                                                         self.lower.segments[i], 
                                                         interval = self.interval,
                                                        es = self.es))
                #switch direction
                upward = not upward