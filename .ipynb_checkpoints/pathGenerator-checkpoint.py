import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from polygon import Polygon
from point import Point
from geomTools import GeomTools

class PathGenerator(Polygon):
    """
    Generates the path based on the given polygon
    
    Inherits the polygon functionality to also build upon and reuse those same functions
    """
    def __init__(self, vertices = [Point(0,0), Point(10,0), Point(10,10), Point(0,10)], tractor_width = 1.5):
        """
        Desc:
        Input:
            
            vertices, a list of Points in **clockwise**
            tractor_width (m)
        Output:
        
        """
        Polygon.__init__(self, vertices)
        
        self.tractor_width = tractor_width
        
        self.setup_outer_poly()
        self.setup_inner_poly()
    
    def __repr__(self):
        """
        Desc:
            Default output of the labelled points and lines
        """
        print(f"_____Printing Path Generator Variables____\
                \n Key Variables \
                \n Tractor Width: {self.tractor_width} \
                \n\n Key Points \
                \n self.low_left: {self.low_left}   {self.vertices[self.low_left]}\
                \n self.top_left: {self.top_left}   {self.vertices[self.top_left]}\
                \n self.low_right: {self.low_right}   {self.vertices[self.low_right]}\
                \n self.top_right: {self.top_right}   {self.vertices[self.top_right]}\
                \n")
        
        
        return "complete"
    
    def setup_outer_poly(self):
        """
        Desc:
            Sets up the outper polygon
        Input:
        Output:
            self.outer, Polygon() of outer rectangle
        """
        self.label_corners()
        
        #must be enter clockwise
        self.outer = Polygon(vertices = [self.vertices[self.low_left],
                                         self.vertices[self.top_left],
                                         self.vertices[self.top_right],
                                         self.vertices[self.low_right]])
        
    def setup_inner_poly(self):
        """
        Desc:
            sets up the internal rectangle that the tractor will follow
        Input:
        Output:
            
        """        
        self.find_temp_b()
        
        self.label_inner_polygon()
        
    def label_corners(self):
        """
        Desc:
            labels the left low corner. Assumes only 4 points in the polygon
        Input:
            self.vertices
        Output:
            self.low_left, int --> 1
            self.top_left, int --> 2
            self.low_right, int --> 3
            self.top_right
        """
        self.low_left = 0

        for i in range(len(self.vertices)):
            pnt = self.vertices[i]
            
            #must be lowest (northing)
            if self.vertices[self.low_left].N() > pnt.N():
                self.low_left = i
                
            #must be left most of equally low (lower easting trumps)
            elif self.vertices[self.low_left].N() == pnt.N() and self.vertices[self.low_left].E() > pnt.E():
                self.low_left = i
            
        #assign topLeft and bottom right
        if self.low_left > 0 and self.low_left < len(self.vertices)-1:
            print("a")
            #middle indice value
            self.top_left = self.low_left - 1
            self.low_right = self.low_left + 1
            
        #assign topLeft and bottom right
        elif self.low_left == 0:
            print("b")
            #middle indice value
            self.top_left = len(self.vertices)-1
            self.low_right = self.low_left + 1
            
        #assign topLeft and bottom right
        elif self.low_left == len(self.vertices)-1:
            print("c")
            #middle indice value
            self.top_left = self.low_left - 1
            self.low_right = 0
            
        self.top_right = self.low_left - 2
    
    def orthog(self, start, end):
        """
        Desc:
            returns a vector that is orgthogonal (perpendicular to the input line segment)
        Input:
            start, Point() of regular line segment
            end, Point()
        Output:
        """
        #make a unit vector
        temp = self.unit(self.vector(start,end))
        
        #switch these two around
        return Point(temp.N(), temp.E())
    
    def find_temp_b(self):
        """
        Desc:
            finds the loewr left of the smaller rectangle
        Input:
            self.low_left, int --> 1
            self.top_left, int --> 2
            self.low_right, int --> 3
            self.tractor_width
        Output:
            self.dist_a, float
            self.vec_a, unit vector contained in a Point()
            self.temp_a, Point()
            self.dist_b, float
            self.vec_b, unit vector contained in a Point()
            self.temp_b, Point()
        """
        #1 to 3
        self.dist_a = self.distance(self.vertices[self.low_left],self.vertices[self.low_right])
        self.vec_a = self.unit(self.vector(self.vertices[self.low_left], self.vertices[self.low_right]))
        
        self.temp_a = Point(self.vertices[self.low_left].E()+self.vec_a.E()*self.tractor_width,
                           self.vertices[self.low_left].N()+self.vec_a.N()*self.tractor_width)
        
        #1 to 2
        self.dist_b = self.distance(self.vertices[self.low_left],self.vertices[self.top_left])
        self.vec_b = self.unit(self.vector(self.vertices[self.low_left],self.vertices[self.top_left]))
        
        self.temp_b = Point(self.temp_a.E()+self.vec_b.E()*self.tractor_width,
                             self.temp_a.N()+self.vec_b.N()*self.tractor_width)
        
    def label_inner_polygon(self):
        """
        Desc:
            Sets up the inner polygon with corners a, b, c, d
        Input:
            self.temp_b
            self.dist_a
            self.dist_b
        Output:
            self.inner, Polygon() the inner polygon
            self.a, Point()
            self.b, Point()
            self.c, Point()
            self.d, Point()
        """        
        self.a = Point(self.temp_b.E(), self.temp_b.N())
        
        self.b = Point(self.temp_b.E()+self.vec_b.E()*(self.dist_b-2*self.tractor_width),
                           self.temp_b.N()+self.vec_b.N()*(self.dist_b-2*self.tractor_width))
        
        self.c = Point(self.b.E()+self.vec_a.E()*(self.dist_a-2*self.tractor_width),
                           self.b.N()+self.vec_a.N()*(self.dist_a-2*self.tractor_width))
        
        self.d = Point(self.temp_b.E()+self.vec_a.E()*(self.dist_a-2*self.tractor_width),
                           self.temp_b.N()+self.vec_a.N()*(self.dist_a-2*self.tractor_width))
        
        #must be entered clockwise
        self.inner = Polygon(vertices = [self.a,self.b,self.c,self.d])