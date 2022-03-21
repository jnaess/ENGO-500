from point import Point
from opps import Opps

import numpy as np
import math as m

class GeomTools(Opps):
    """
    Contains functions to ain in geometry functions"""
    
    def __init__(self):
        """
        Desc:
        """
        Opps.__init__(self)
        return
        
    def get_intersect(self, a1 = Point(0,0), a2 = Point (3,3), b1 = Point(0,3), b2 = Point(2,0)):
        """ 
        Desc:
            Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
        Source:
            https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
        Input:
            a1: Point() a point on the first line
            a2: Point() another point on the first line
            b1: Point() a point on the second line
            b2: Point() another point on the second line
        Output:
            
        """
        s = np.vstack([a1.twoD(),a2.twoD(),b1.twoD(),b2.twoD()])        # s for stacked
        h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
        l1 = np.cross(h[0], h[1])           # get first line
        l2 = np.cross(h[2], h[3])           # get second line
        x, y, z = np.cross(l1, l2)          # point of intersection
        if z == 0:                          # lines are parallel
            return (float('inf'), float('inf'))
        return (x/z, y/z)
    
    def new_par_line(self, a = Point(0,0), b = Point (3,3), offset = 2):
        """
        Desc:
            creates a parallel line a set distance from the input line
        Input:
            a, Point()
            b, Point()
            offset, the distance to offset the line by
        Output:
            [Point(), Point()] of the new parallel line segment
        """
        L = m.sqrt((a.E()-b.E())**2+(a.N()-b.N())**2)

        offset = 10

        a2 = []
        b2 = []
        #// This is the second line
        a2.append(a.E() + offset * (b.N()-a.N()) / L)
        b2.append(b.E() + offset * (b.N()-a.N()) / L)

        a2.append(a.N() + offset * (a.E()-b.E()) / L)
        b2.append(b.N() + offset * (a.E()-b.E()) / L)

        return [Point(a2[0],a2[1]), Point(b2[0],b2[1])]
    