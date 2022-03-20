import math as m
import numpy as np

from point import Point
from setup import Base

class Opps(Base):
    """
    contains vector operations
    """
    
    def __init__(self):
        """"""
        Base.__init__(self)
        
        return
        
    def dot(self, v,w):
        """
        Desc:
        Input:
            v, Point()
            w, Point()
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
            v, Point()
        Output:
            returns --> float value
        """
        x,y,z = v.threeD()
        
        return m.sqrt(x*x + y*y + z*z)

    def vector(self, b,e):
        """
        Desc:
        Input:
            b, Point()
            e, Point()
        Output:
            returns --> Point()
        """
        x,y,z = b.threeD()
        X,Y,Z = e.threeD()
        
        return Point(X-x, Y-y, Z-z)

    def unit(self, v):
        """
        Desc:
        Input:
            v, Point()
        Output:
            returns --> Point()
        """
        x,y,z = v.threeD()
        mag = self.length(v)
        
        return Point(x/mag, y/mag, z/mag)

    def distance(self, p0, p1):
        """
        Desc:
        Input:
            p0, Point()
            p1, Point()
        Output:
            returns --> float value
        """
        return self.length(self.vector(p0,p1))

    def scale(self, v,sc):
        """
        Desc:
        Input:
            v, Point()
            sc, scale (float value)
        Output:
            returns --> Point()
        """
        x,y,z = v.threeD()
        
        return Point(x * sc, y * sc, z * sc)

    def add(self, v,w):
        """
        Desc:
        Input:
            v, Point()
            w, Point()
        Output:
            returns --> Point()
        """
        x,y,z = v.threeD()
        X,Y,Z = w.threeD()
        
        return Point(x+X, y+Y, z+Z)