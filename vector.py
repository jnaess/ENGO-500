import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from opps import Opps
from point import Point

class Vector(Opps):
    """
    sets up a vector with a start point and end point
    """
    
    def __init__(self, start = Point(5,0,0), end = Point(5,10,0)):
        """
        Desc:
        Input:
            start = (x,y,z)
            end = (x,y,z)
        """
        Opps.__init__(self)
        
        self.start = start
        self.end = end
        
    def pnt2line(self, pnt = Point(6,4,0)):
        """
        Desc:
            Finds the nearest point on the vector line that is perpendicular to the desired line.
            Returns both the distance between those two poitns and the newly found points cooridinates
        Source:
            https://stackoverflow.com/questions/27161533/find-the-shortest-distance-between-a-point-and-line-segments-not-line
        Input:
            pnt: of the desired point to find a shortest distance to
            self.start
            self.end
        Output:
            self.pnt, input point
            self.dist, distance to the input point
            self.nearest, point on the current vector that is nearest to the input point
            returns --> (distance, (x, y, z))
        """
        self.pnt = pnt
        
        line_vec = self.vector(self.start, self.end)
        pnt_vec = self.vector(self.start, self.pnt)
        line_len = self.length(line_vec)
        line_unitvec = self.unit(line_vec)
        pnt_vec_scaled = self.scale(pnt_vec, 1.0/line_len)
        t = self.dot(line_unitvec, pnt_vec_scaled)    
        if t < 0.0:
            t = 0.0
        elif t > 1.0:
            t = 1.0
        nearest = self.scale(line_vec, t)
        dist = self.distance(nearest, pnt_vec)
        nearest = self.add(nearest, self.start)
        
        #store variables for future use
        
        self.dist = dist
        self.nearest = nearest
        return (dist, nearest)
    
    def prepare_lines(self):
        """
        Desc:
            initializes the line and colour variables to be put into the collection
        Input:
            self.start
            self.nearest
            self.pnt
        Output:
            self.lines
            self.c
            self.l_style
        """
        #2 is because to 3 we would be including Z points which we assume to be zero
        self.lines = [[self.start.twoD(), self.end.twoD()],[self.nearest.twoD(), self.pnt.twoD()]]
        
        #colouration for lines
        self.c = np.array([(1, 0, 1, 1),(0, 0, 1, .5)])
        
        #line styles
        self.l_style = ['solid', 'dashed']
        
        
    def plot_pnt2line(self):
        """
        Desc:
            plots a graph of the points and vector
        Input:
            self.start
            self.nearest
            self.pnt         
        """
        #set up line collection
        self.prepare_lines()
        lc = mc.LineCollection(self.lines, colors=self.c, linewidths=2, linestyles = self.l_style)
        
        #initialize figure
        fig, ax = pl.subplots()
        
        #add lines
        ax.add_collection(lc)
        
        #input point
        ax.scatter(self.pnt.E(),self.pnt.N(), color = 'g', zorder = 2)
        
        #nearest point
        ax.scatter(self.nearest.E(),self.nearest.N(), zorder = 2)
        
        ax.margins(0.1)