import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl


class PositionGenerator():
    """
    This class E and N generates positions based on std
    """
    
    def __init__(self, std=[1,1], mean=[0,0], count = 1000):
        """
        Desc:
        Input:
            std, standard deviation [E, N]
            mean, [E, N]
            count, the number of points to generate
        """
        self.std = std
        self.mean = mean
        self.count = count
        
        #generate base set of points
        self.generate()
    
    def generate(self, count = None):
        """
        Desc:
            Generates the points for future use or to be plotted
            **assumes normal distribution**
        Input:
            self.std
            seld.mean,
            count = self.count, incase the user wants to generate just 1 number -- must always be greater than zero
        """
        if not count == None:
            self.count = count
        self.E = np.random.normal(self.mean[0], self.std[0], self.count)
        self.N = np.random.normal(self.mean[1], self.std[1], self.count)
        
    def plot(self, pick_one = False):
        """
        Desc:
            Plots all E and N points that have been generated on a 2D graph
        Input:
            self.N
            self.E
        """
        #check that there are points and equal lengths
        if self.N.shape == self.E.shape and self.N.shape[0] > 0:
            plt.scatter(self.E, self.N, color = 'b')
            
            if pick_one:
                #then we highlight and save one of the points
                #because its alread random we can just save the first one
                self.one_E = self.E[0]
                self.one_N = self.N[0]
                plt.scatter(self.one_E, self.one_N, color = 'r')
                
class Operator():
    """
    contains vector operations
    """
    
    def __init__(self):
        """"""
        return
        
    def dot(self, v,w):
        x,y,z = v
        X,Y,Z = w
        return x*X + y*Y + z*Z

    def length(self, v):
        x,y,z = v
        return m.sqrt(x*x + y*y + z*z)

    def vector(self, b,e):
        x,y,z = b
        X,Y,Z = e
        return (X-x, Y-y, Z-z)

    def unit(self, v):
        x,y,z = v
        mag = self.length(v)
        return (x/mag, y/mag, z/mag)

    def distance(self, p0,p1):
        return self.length(self.vector(p0,p1))

    def scale(self, v,sc):
        x,y,z = v
        return (x * sc, y * sc, z * sc)

    def add(self, v,w):
        x,y,z = v
        X,Y,Z = w
        return (x+X, y+Y, z+Z)

class Vector(Opperator):
    """
    sets up a vector with a start point and end point
    """
    
    def __init__(self, start, end):
        """
        Desc:
        Input:
            start = (x,y,z)
            end = (x,y,z)
        """
        Operator.__init__(self)
        
        self.start = start
        self.end = end
        
    def pnt2line(self, pnt):
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

        line_vec = self.vector(self.start, self.end)
        pnt_vec = self.vector(self.start, pnt)
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
        self.pnt = pnt
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
        self.lines = [[self.start[:2], self.end[:2]],[self.nearest[:2], self.pnt[:2]]]
        
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
        ax.scatter(self.pnt[0],self.pnt[1], color = 'g', zorder = 2)
        
        #nearest point
        ax.scatter(self.nearest[0],self.nearest[1], zorder = 2)
        
        ax.margins(0.1)