from point import Coord
from geomTools import GeomTools

import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

class Polygon(GeomTools):
    """
    Sets up a polygon and maintains rules to ensure functionality
    """
    
    def __init__(self, vertices = [Coord(0,0), Coord(0,10), Coord(10,10), Coord(10,0)]):
        """
        Desc:
        Input:
            vertices, a list of Coords in **clockwise**
        Output:
            self.pnt, Coord() to be evaluated
        """
        GeomTools.__init__(self)
        
        self.vertices = vertices
        self.pnt = False #until a point is made
    
    def is_on_right_side(self, pnt, xy0, xy1):
        """
        Desc:
            checked whether the point is on the left or right of the line segment
        Source:
            https://stackoverflow.com/questions/63527698/determine-if-points-are-within-a-rotated-rectangle-standard-python-2-7-library
        Input:
            pnt, Coord() to be checked
            xy0, Coord()
            xy1, Coord()
        Output:
            True is on right side, False if on left side
        """
        x0, y0 = xy0.twoD()
        x1, y1 = xy1.twoD()
        a = float(y1 - y0)
        b = float(x0 - x1)
        c = - a*x0 - b*y0
        
        return a*pnt.E() + b*pnt.N() + c >= 0

    def test_point(self, pnt):
        """
        Desc:
            tests whether or not a point is within the polygon
        Source:
            https://stackoverflow.com/questions/63527698/determine-if-points-are-within-a-rotated-rectangle-standard-python-2-7-library
        Input:
            self.vertices
            pnt, Coord() of the desired point to be checked
        Output:
            True/False --> True if point lies inside the polygon
        """
        self.pnt = pnt
        
        num_vert = len(self.vertices)
        is_right = [self.is_on_right_side(self.pnt, self.vertices[i], self.vertices[(i + 1) % num_vert]) for i in range(num_vert)]
        all_left = not any(is_right)
        all_right = all(is_right)
        
        #new member vairable for pnt
        self.pnt.IsInside = all_left or all_right
        
        return self.pnt.IsInside
    
    def prepare_lines(self):
        """
        Desc:
            initializes the line and colour variables to be put into the collection
        Input:
            self.lines [Coord(), Coord(), ....]
        Output:
            self.lines
        """
        #preps to be formatted for graphing
        self.lines = []
        
        for i in range(len(self.vertices)-1):
            line = [self.vertices[i].twoD(),self.vertices[i+1].twoD()]
            self.lines.append(line)
            
        #add last one
        line = [self.vertices[-1].twoD(),self.vertices[0].twoD()]
        self.lines.append(line)
        
    def plot(self):
        """
        Desc:
            plots a graph of the point and vectors
        Input:
            self.start
            self.nearest
            self.pnt         
        """
        #set up line collection
        self.prepare_lines()
        lc = mc.LineCollection(self.lines)
        
        #initialize figure
        fig, ax = pl.subplots()
        
        #add lines
        ax.add_collection(lc)
        
        if self.pnt:
            if self.pnt.IsInside:
                #then it is inside
                ax.scatter(self.pnt.E(),self.pnt.N(), color = 'g', zorder = 2)
            else:
                #then it is outside
                ax.scatter(self.pnt.E(),self.pnt.N(), color = 'r', zorder = 2)
        
        ax.margins(0.1)