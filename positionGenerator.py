import numpy as np
import matplotlib.pyplot as plt

from setup import Base
from point import Point

class PositionGenerator(Base):
    """
    This class E and N generates positions based on std
    """
    
    def __init__(self, mean=Point(0,0), count = 1000):
        """
        Desc:
        Input:
            std, standard deviation [E, N]
            mean, [E, N]
            count, the number of points to generate
        """
        Base.__init__(self)
        
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
            self.mean,
            count = self.count, incase the user wants to generate just 1 number -- must always be greater than zero
        Output:
            self.E_pnts, numpy array of easting coordinates
            self.N_pnts, numpy array of northing coords
        """
        if not count == None:
            self.count = count
        self.E_pnts = np.random.normal(self.mean.E(), self.mean.std[0], self.count)
        self.N_pnts = np.random.normal(self.mean.N(), self.mean.std[1], self.count)
        
    def plot(self, pick_one = False):
        """
        Desc:
            Plots all E and N points that have been generated on a 2D graph
        Input:
            self.N
            self.E
        Output:
            self.unique_pnt, Point() object of the first of the generated E and N coordinates
        """
        #check that there are points and equal lengths
        if self.N_pnts.shape == self.E_pnts.shape and self.N_pnts.shape[0] > 0:
            plt.scatter(self.E_pnts, self.N_pnts, color = 'b')
            
            if pick_one:
                #then we highlight and save one of the points
                #because its alread random we can just save the first one
                self.unique_pnt = Point(self.E_pnts[0],self.N_pnts[0])
                plt.scatter(self.unique_pnt.E(), self.unique_pnt.N(), color = 'r')