import numpy as np
import matplotlib.pyplot as plt
import math as m
from matplotlib import collections  as mc
plt.style.use('seaborn-whitegrid')
import pylab as pl
import pyproj

class Point():
    """
    Class contains all parameters to convert between coordinates and store coordiante values
    """
    
    def __init__(self, e, n, h = 0, std = [.01,.01], inProj = "E_N", outProj = "E_N", name = "N/A", truth=False, to_out=False):
        """
        Desc:
        Input:
            E, easting or longitude
            N, northing or latitude
            H, height -- default 0
            std, the precision in easting, northing which will be used for point generation
            inProj, projection type being input, E_N if more for testing
            outProj, project output type if already known: can be modified
            truth, True/False as to wether or not this point is considered a true point
            to_out, True/False --> it True, then imidiately change coords to the Out projection
        Output:
            self.current_proj, string of the current projection
        """
        
        self.e = e
        self.n = n
        self.h = h
        self.std = std
        
        self.currentProj = inProj
        
        self.inProj = inProj
        self.outProj = outProj
        self.name = name
        self.truth = truth
        
        if to_out:
            self.curr_to_out()
    
    def __repr__(self):
        """
        Desc:
        Input:
        Output:
        """
        return str([self.E(), self.N()])
        
    def H(self):
        """
        Desc:
            returns height point
            this function is made for future projection checking
        Output:
            return --> self.H
        """
        return self.h
    
    def E(self):
        """
        Desc:
            returns Easting point
            this function is made for future projection checking
        Output:
            return --> self.E
        """
        return self.e
    
    def N(self):
        """
        Desc:
            returns Northing point
            this function is made for future projection checking
        Output:
            return --> self.N
        """
        return self.n
    
    def twoD(self):
        """
        Desc:
            returns [E, N] of the point
        Input: none
        Output
            return --> [self.E, self.N]
        """
        return [self.E(), self.N()]
    
    def threeD(self):
        """
        Desc:
            returns [E, N, H] of the point
        Input: none
        Output
            return --> [self.E(), self.N(), self.H()]
        """
        return [self.E(), self.N(), self.H()]
    
    def curr_to_out(self):
        """
        Desc:
            converts points from current_proj to outproj
        Input:
            self.in_proj
            self.out_proj
        Output:
            self.E --> updated
            self.N --> updated
        """
        if self.currentProj != self.outProj:
            #then they are different so we can convert
            
            proj = pyproj.Transformer.from_crs(self.currentProj, self.outProj, always_xy=True)

            self.e,self.n = proj.transform(self.e,self.n)
