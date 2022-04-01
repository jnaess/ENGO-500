import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
import math as m

from point import Coord

class Ellipse(Coord):
    """
    Contains the dimensions of an ellipse and has respective functions
    """
    
    def __init__(self, e, n, std = [1,1], angle = 0):
        """
        Desc:
        Input:
            e, easting of the center of the point
            n, northing of the center of the point
            std, [e,n] of the std of the point
            angle = 0, degree rotation of the error ellipse
        Output:
        """
        Coord.__init__(self, e, n, std=std)
        
        self.angle = angle
        
        # The ellipse
        self.g_ell_width = self.std[0]*2
        self.g_ell_height = self.std[1]*2

        self.cos_angle = np.cos(np.radians(180.-self.angle))
        self.sin_angle = np.sin(np.radians(180.-self.angle))
        
    def in_error_ellipse(self, test_coord, std_out = 1):
        """
        Desc:
        Source:
            https://stackoverflow.com/questions/37031356/check-if-points-are-inside-ellipse-faster-than-contains-point-method
        Input:
            std_out --> float of the number of std away from center to check
            self.E
            self.N
            self.angle [e,n]
            self.std, rotation of the error ellipse degrees
            test_coord, Coord() or [Coord(), ... , Coord()] for the point(s) to be tested
        Output:
            self.test_point
        """
        if type(test_coord) == type(Ellipse(0,0)) or type(test_coord) == type(Coord(0,0)):
            # it is only one test points
            self.x = np.array([test_coord.E()])
            self.y = np.array([test_coord.N()])
            
        else:
            #then its an array of points
            print("multiple points have not yet been incorporated, please update Ellipse.in_error_ellipse() function")
            return -1
           
        self.xc = self.x - self.E()
        self.yc = self.y - self.N()
        
        self.xct = self.xc * self.cos_angle - self.yc * self.sin_angle
        self.yct = self.xc * self.sin_angle + self.yc * self.cos_angle 

        self.rad_cc = (self.xct**2/(self.g_ell_width/2.)**2) + (self.yct**2/(self.g_ell_height/2.)**2)
        
        #for 3 times the error ellipse
        if self.rad_cc <= std_out*1.:
            #inside circle
            return True
        elif self.rad_cc > .1:
            return False #track jump error
        
        else: return True #not a track jump level
          
    def plot_ellipse_pnt(self):
        """
        Desc:
            Plots the ellipse and the point that it was being tested from
        Input:
            self.in_error_ellipse()
        Output:
        """
        fig,ax = plt.subplots(1)
        ax.set_aspect('equal')

        #add our error ellipse
        g_ellipse = patches.Ellipse(self.twoD(), 
                                    self.g_ell_width, 
                                    self.g_ell_height, 
                                    angle=self.angle, 
                                    fill=False, 
                                    edgecolor='b', 
                                    linewidth=2)
        
        ax.add_patch(g_ellipse)

        # Set the colors. Black if outside the ellipse, green if inside
        colors_array = np.array(['r'] * len(self.rad_cc))
        colors_array[np.where(self.rad_cc <= 1.)[0]] = 'green'

        ax.scatter(self.x, self.y,
                   c=colors_array,
                   linewidths=0.3)

        plt.show()