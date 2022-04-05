import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from polygon import polygon
from point import Coord
from opps import Opps
from geomTools import GeomTools
from pathGenerator import PathGenerator
from positionGenerator import PositionGenerator
from pathFollower import PathFollower
from errorSimulator import ErrorSimulator
from trackRecorder import TrackRecorder

class PassGenerator(PathGenerator, TrackRecorder):
    """
    Generates all start and end points of the paths, 
    then uses PathFollower to generate center points and direction vectors of each segment
    """
    
    def __init__(self, interval = 2.2, vertices = [Coord(0,0), Coord(10,0), Coord(10,10), Coord(0,10)], tractor_width = 1.5, es = ErrorSimulator()):
        """
        Desc:
        Input:
            interval, interval distance in 'm' to simulate distance between new measurements
        Output:
        """
        PathGenerator.__init__(self, vertices, tractor_width)
        TrackRecorder.__init__(self)
        
        self.interval = interval
        
        self.es = es
        
        self.passes()
        
    def true_pass_points(self):
        """
        Desc:
            sets up the 'true' pass points
        Input:
        Output:
            self.lower_start, Coord()
            self.upper_start, Coord
            self.lower, PathFollower() of the lower inner rectangle true pass points
            self.upper, PathFollower() of the upper inner rectangle true pass points
        """
        self.pg_true = PositionGenerator(mean = Coord(0,0, truth = True))
        
        #slightly off of a and b because of 1/2 of the width of a tractor used up
        self.lower_start = Coord(self.a.E()+self.vec_a.E()*(self.tractor_width/2),
                           self.a.N()+self.vec_a.N()*(self.tractor_width/2))
        
        self.upper_start = Coord(self.b.E()+self.vec_a.E()*(self.tractor_width/2),
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
        
        #set path follower distance variable
        PathFollower.dist = self.distance(self.lower.segments[0],self.upper.segments[0])
        
    def passes(self):
        """
        Desc:
            sets up all passes
        Input:
        Output:
            self.true_passes, [PathFollower(), ... , PathFollower()]
            self.real_passes --> incomplete
            self.pass_count --> int, number of passes
        """        
        self.true_pass_points()
        
        self.true_passes = []
        
        #not yet added to functionality
        self.real_passes = []
        
        self.order = 1
        
        if len(self.lower.segments) == len(self.upper.segments):
            #then probalby a rectangle as we wanted
            self.pass_count = len(self.lower.segments)
            
            upward = True
                                
            for i in range(self.pass_count):
                #set up real start and end points via adding the current total error
                #added to both because of thinking tractor is currently in correct position and aiming to same vector as if it was
                real_lower = Coord(self.lower.segments[i].E()+self.es.total_error.E(),
                                       self.lower.segments[i].N()+self.es.total_error.N())
                real_upper = Coord(self.upper.segments[i].E()+self.es.total_error.E(),
                                       self.upper.segments[i].N()+self.es.total_error.N())
                 
                    
                #for the true distance when mapping out real path    
                distance = 7
                if upward:
                    #will we use errors?
                    self.es.is_real = False
                    
                    #tuth pass
                    #then go from bottom to top
                    self.true_passes.append(PathFollower(self.lower.segments[i],
                                                         self.upper.segments[i], 
                                                         interval = self.interval,
                                                        es = self.es,
                                                        order = self.order,
                                                        plan = False,
                                                        real = self.es.is_real))
                    
                    
                    #will we use errors?
                    self.es.is_real = True
                    #real pass
                    #then go from bottom to top
                    self.real_passes.append(PathFollower(real_lower,
                                                         real_upper, 
                                                         interval = self.interval,
                                                        es = self.es,
                                                        order = self.order,
                                                        plan = False,
                                                        real = self.es.is_real))
                    
                else:
                    #will we use errors?
                    self.es.is_real = False
                    #truth pass
                    #then go from top to bottom
                    self.true_passes.append(PathFollower(self.upper.segments[i], 
                                                         self.lower.segments[i], 
                                                         interval = self.interval,
                                                        es = self.es,
                                                        order = self.order,
                                                        plan = False,
                                                        real = self.es.is_real))
                    
                    #will we use errors?
                    self.es.is_real = True
                    #real pass
                    #then go from bottom to top
                    self.real_passes.append(PathFollower(real_upper, 
                                                         real_lower, 
                                                         interval = self.interval,
                                                        es = self.es,
                                                        order = self.order,
                                                        plan = False,
                                                        real = self.es.is_real))
                #increment order
                self.order = self.order + 1
                
                #switch direction
                upward = not upward
                