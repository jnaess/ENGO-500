from setup import Base

class Point():
    """
    Class contains all parameters to convert between coordinates and store coordiante values
    """
    
    def __init__(self, e, n, h = 0, std = [1,1], inProj = "E_N", outProj = "E_N"):
        """
        Desc:
        Input:
            E, easting or longitude
            N, northing or latitude
            H, height -- default 0
            std, the precision in easting, northing which will be used for point generation
            inProj, projection type being input, E_N if more for testing
            outProj, project output type if already known: can be modified
        Output:
        """
        Base.__init__(self)
        
        self.e = e
        self.n = n
        self.h = h
        self.std = std
        self.inProj = inProj
        self.outProj = outProj
    
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