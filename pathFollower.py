import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from opps import Opps
from point import Coord
from vector import Vector
from positionGenerator import PositionGenerator
from errorSimulator import ErrorSimulator

class PathFollower(Vector):
    """
    Follows a desired path in increments and incorporates simulation errors
    """
    
    def __init__(self, start, end, interval = 1, es = ErrorSimulator(), order = 1, plan = True):
        """
        Desc:
        Input
            start, Coord()
            end, Coord()
            interval, interval distance in 'm' to simulate new measurements
            es, the error simulator
            order, the order that the pathfollower is in respect to other line strings
            plan, T/F --> True if the plot is for planning, False if the path is for path routing
            
        Output:
            self.dist, the distance that the path is
            self.vect, the vector to be multiplied by a point to get us to the next segment
            self.increments, the number of increments given the interval length and path length
            self.remainder, the remainder distance to be multipled the unvit vector for the final segment
        """
        Vector.__init__(self, start, end)
        
        self.start = start
        self.end = end
        self.interval = interval
        self.es = es
        self.order = order
        self.plan = plan
        
        self.dist = self.distance(self.start, self.end)
        self.vect = self.unit(self.vector(self.start, self.end))
        
        self.increments = int(self.dist / self.interval + 1)

        if plan:
            #then this is an upper or lower bound track
            self.remainder = self.dist % self.interval
            if self.remainder - self.interval / 2 < 0:
                #then we need to make it equal to less than 0 so that the pass is not incorporated
                self.remainder = self.remainder - self.interval
        else:
            self.remainder = self.dist % self.interval
        
        self.segment()
    
    def __str__(self):
        """
        """
        return f'start: {self.start} | end: {self.end} \
                \n dist: {self.dist} | vect: {self.vect} \
                \n increments: {self.increments} | remainder: {self.remainder}'
    
    def segment(self):
        """
        Desc:
            Breaks the ideal path into a list of points, with the final point filling in the remainder
        Input:
            self.start
            self.increments
            self.order
        Output:
            self.segments, [Coord(), ..., Coord()]
            self.point_order, np.array([1, 2, ... , n])
            self.segment_order, np.array([self.order, ... , self.order])
        """
        #setup lists to be extracted
        self.point_order = np.arange(1,self.increments+1,1)
        self.segment_order = np.ones((self.increments))*self.order
        self.segments = [self.start]
        
        for i in range(1, self.increments):
            #make next error
            self.es.add_error(self.interval)
            
            next_Pnt = Coord(self.segments[i-1].E()+self.vect.E()*self.interval+self.es.E(), 
                        self.segments[i-1].N()+self.vect.N()*self.interval+self.es.N())
            
            self.segments.append(next_Pnt)
            
        if self.remainder > 0:
            #make next error
            self.es.add_error(self.remainder)
            
            next_Pnt = Coord(self.segments[-1].E()+self.vect.E()*self.remainder+self.es.E(), 
                        self.segments[-1].N()+self.vect.N()*self.remainder+self.es.N())
            
            self.segments.append(next_Pnt)
         
        #initialize these variables lat and long
        self.update_e_n()
    
    def update_e_n(self):
        """
        Desc:
            updates the easting and northing numpy array
        Input:
            self.segments
        Output:
            self.e, np.array()
            self.n, np.array()
        """
        self.e = np.empty(self.increments)
        self.n = np.empty(self.increments)
        
        for i in range(self.increments):
            self.e[i] = self.segments[i].E()
            self.n[i] = self.segments[i].N()
            
    def plot(self):
        """
        Desc:
            plots a graph of the points and vector
        Input:
            self.start
            self.nearest
            self.pnt         
        """
        self.update_e_n()
        
        #initialize figure
        fig, ax = pl.subplots()
        
        #all point
        ax.scatter(self.e,self.n)
        
        #start and end point
        ax.scatter([self.start.E(),self.end.E()],[self.start.N(),self.end.N()], color = 'r', zorder = 2)
        
        ax.margins(0.1)