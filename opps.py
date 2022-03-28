import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl

from point import Coord

class Opps():
    """
    contains vector operations
    """
    
    def __init__(self):
        """"""
        
        return
        
    def dot(self, v,w):
        """
        Desc:
        Input:
            v, Coord()
            w, Coord()
        Output:
            returns --> float value
        """
        x,y,z = v.threeD()
        X,Y,Z = w.threeD()
        
        return x*X + y*Y + z*Z

    def length(self, v):
        """
        Desc:
        Input:
            v, Coord()
        Output:
            returns --> float value
        """
        x,y,z = v.threeD()
        
        return m.sqrt(x*x + y*y + z*z)

    def vector(self, b,e):
        """
        Desc:
            e-->b
        Input:
            b, Coord() start
            e, Coord() end
        Output:
            returns --> Coord() but is actually just a store of a vector (slopes and direction)
        """
        x,y,z = b.threeD()
        X,Y,Z = e.threeD()
        
        return Coord(X-x, Y-y, Z-z)

    def unit(self, v):
        """
        Desc:
        Input:
            v, Coord()
        Output:
            returns --> Coord()
        """
        x,y,z = v.threeD()
        mag = self.length(v)
        
        return Coord(x/mag, y/mag, z/mag)

    def distance(self, p0, p1):
        """
        Desc:
        Input:
            p0, Coord()
            p1, Coord()
        Output:
            returns --> float value
        """
        return self.length(self.vector(p0,p1))

    def scale(self, v,sc):
        """
        Desc:
        Input:
            v, Coord()
            sc, scale (float value)
        Output:
            returns --> Coord()
        """
        x,y,z = v.threeD()
        
        return Coord(x * sc, y * sc, z * sc)

    def add(self, v,w):
        """
        Desc:
        Input:
            v, Coord()
            w, Coord()
        Output:
            returns --> Coord()
        """
        x,y,z = v.threeD()
        X,Y,Z = w.threeD()
        
        return Coord(x+X, y+Y, z+Z)