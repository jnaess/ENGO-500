from point import Point

import numpy as np
import math as m

class Polygon():
    """
    Sets up a polygon and maintains rules to ensure functionality
    """
    
    def __init__(self, vertices = [Point(0,0), Point(0,10), Point(10,10), Point(10,0)]):
        """
        Desc:
        Input:
            vertices, a list of Points in **clockwise** --> I think...
        Output:
        """
        self.vertices = vertices
    
    def is_on_right_side(self, pnt, xy0, xy1):
        """
        Desc:
            checked whether the point is on the left or right of the line segment
        Source:
            https://stackoverflow.com/questions/63527698/determine-if-points-are-within-a-rotated-rectangle-standard-python-2-7-library
        Input:
            pnt, Point() to be checked
            xy0, Point()
            xy1, Point()
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
            pnt, Point() of the desired point to be checked
        Output:
            True/False --> True if point lies inside the polygon
        """
        num_vert = len(self.vertices)
        is_right = [self.is_on_right_side(pnt, self.vertices[i], self.vertices[(i + 1) % num_vert]) for i in range(num_vert)]
        all_left = not any(is_right)
        all_right = all(is_right)
        
        return all_left or all_right
    
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

        return [Point(a2[0],a2[1]), Point(a2[0],a2[1])]