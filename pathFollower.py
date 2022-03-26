import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from setup import Base
from opps import Opps
from point import Point
from vector import Vector
from positionGenerator import PositionGenerator

class PathFollower(Vector):
    """
    Follows a desired path in increments and incorporates simulation errors
    """
    
    def __init__(self, start, end, interval = 1, pg = PositionGenerator()):
        """
        Desc:
        Input
            start, Point()
            end, Point()
            interval, interval distance in 'm' to simulate new measurements
            pg, PositionGenerator() for the drift error in error per meter travelled by the tractor
            
        Output:
            self.dist, the distance that the path is
            self.vect, the vector to be multiplied by a point to get us to the next segment
            self.increments, the number of increments given the interval length and path length
            self.remainder, the remainder distance to be multipled the unvit vector for the final segment
            self.erros = [Point(), ... , Point()] errors in order of how they happened for plotting purposes
            self.total_error, Point() of the cumulative error
        """
        Vector.__init__(self, start, end)
        
        self.start = start
        self.end = end
        self.interval = interval
        self.pg = pg
        self.errors = []
        self.total_error = Point(0,0)
        
        self.dist = self.distance(self.start, self.end)
        self.vect = self.unit(self.vector(self.start, self.end))
        self.increments = int(self.dist / self.interval)
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
        Output:
            self.segments, [Point(), ..., Point()]
        """
        
        self.segments = [self.start]
        
        for i in range(self.increments):
            next_Pnt = Point(self.segments[i].E()+self.vect.E()*self.interval+self.add_error(i, 'E'), 
                        self.segments[i].N()+self.vect.N()*self.interval+self.add_error(i, 'N'), 
                        self.segments[i].H()+self.vect.H()*self.interval+self.add_error(i, 'H'))
            
            self.segments.append(next_Pnt)
            
        if self.remainder > 0:
            next_Pnt = Point(self.segments[-1].E()+self.vect.E()*self.remainder+self.add_error(-1, 'E'), 
                        self.segments[-1].N()+self.vect.N()*self.remainder+self.add_error(-1, 'N'), 
                        self.segments[-1].H()+self.vect.H()*self.remainder+self.add_error(-1, 'H'))
            
            self.segments.append(next_Pnt)
    
    def add_error(self, i, direction = "E"):
        """
        Desc:
            returns the error to be added either E, N, or H | default value is 0
        Input:
            direction 'E', 'N', 'H'
            isInterval: True/False to add either interval or remainder amounts
            self.vect
            self.interval
        Output:
            retunr --> float | default 0
        """        
        #generate new statistical random error
        self.pg.generate_one()
        
        e = 0
        n = 0
        
        if i == -1:          
            #then this is a remainder generator
            #add errors to our counters
            e = self.remainder*self.pg.unique_pnt.E()
            n = self.remainder*self.pg.unique_pnt.N()
            
        else:
            #add errors to our counters
            e = self.interval*self.pg.unique_pnt.E()
            n = self.interval*self.pg.unique_pnt.N()
        
        self.errors.append(Point(e,n))

        self.total_error.e = self.total_error.E()+e
        self.total_error.n = self.total_error.N()+n
            
        if direction == 'E':
            #NOT self.vect.E()*self.interval*self.delta.E() because error is relative to distance travelled, not relative to eartern distance travelled
            return self.errors[-1].E()
        
        elif direction == "N":
            return self.errors[-1].N()
        
        elif direction == "H":
            #not used in out simulation
            return 0
        
        return 0
        
    def plot(self):
        """
        Desc:
            plots a graph of the points and vector
        Input:
            self.start
            self.nearest
            self.pnt         
        """
        E = []
        N = []
        
        for pnt in self.segments:
            E.append(pnt.E())
            N.append(pnt.N())
        
        #initialize figure
        fig, ax = pl.subplots()
        
        #all point
        ax.scatter(E,N)
        
        #start and end point
        ax.scatter([self.start.E(),self.end.E()],[self.start.N(),self.end.N()], color = 'r', zorder = 2)
        
        ax.margins(0.1)