from point import Point

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