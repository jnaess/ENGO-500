import numpy as np
from pyproj import Proj, transform
import pandas as pd
from gnss_headers import GNSS_Headers
        
        
class Data(GNSS_Headers):
    """
    Contains the NovAtel data in an easy to use format
    """
    
    def __init__(self, file_name = "Rooftop_Position_Logs.ASC"):
        """
        Desc:
            Sets up the object
        Input:
        Output:
        """
        GNSS_Headers.__init__(self)
        
        self.file_name = file_name
        
        self.read_in()
        self.setup_df()
        
    def clean_and_split(self, line):
        """returns only the valuable (not header stuff)"""
        return line.strip("\n").strip("#").split(";")[1].split(",")
    
    def read_in(self):
        """
        Desc:
            reads in from the ASC file
        Input:
            self.file_name
        Output:
            self.rtk_data, numpy array
            self.ppp_data, numpy array
            self.psr_data, numpy array
        """
        self.rtk_data = []
        self.ppp_data = []
        self.psr_data = []

        with open(self.file_name, 'r') as f:
            count = 0
            for line in f:
                data = self.clean_and_split(line)

                if count%3 == 0:
                    #then rtk
                    self.rtk_data.append(data)
                elif count%3 == 1:
                    #then ppp
                    self.ppp_data.append(data)
                else:
                    #then psr
                    self.psr_data.append(data)

                count = count + 1
                
        self.rtk_data = np.array(self.rtk_data)
        self.ppp_data = np.array(self.ppp_data)
        self.psr_data = np.array(self.psr_data)
        
    def setup_df(self):
        """
        Desc:
            Sets up the dataframes for the 3 datatypes
        Input:
            self.rtk_data
            self.rtk_cols
            self.ppp_data
            self.ppp_cols
            self.psr_data
            self.psr_cols
        Output:
            self.rtk, DataFrame
            self.ppp, DataFrame
            self.psr, DataFrame
        """
        self.rtk = pd.DataFrame(self.rtk_data, columns=self.rtk_cols)
        self.ppp = pd.DataFrame(self.ppp_data, columns=self.ppp_cols)
        self.psr = pd.DataFrame(self.psr_data, columns=self.psr_cols)
        
    def convert(self, lat, lon, in_proj = "epsg:3780", out_proj = "epsg:32611"):
        """
        Desc:
            will return a list of converted coordinates
        Input:
            lat, [] list
            lon, [] list
            in_proj, string of the espg coordinate system that the input coordinates are in
            out_prooj, string of the espg coord system that the coordinates will be output/returned to
        Output:
            returns --> [lat],[lon]
        """
        #reset indeces
        lat = list(lat)
        lon = list(lon)
        
        new_lat = []
        new_lon = []
        
        if len(lat) == len(lon) and len(lat) > 0:
            #then these are conditions that we can convert in
            inProj = Proj(init=in_proj)
            outProj = Proj(init=out_proj)
            
            for i in range(len(lat)):
                x,y = transform(inProj,outProj,lon[i],lat[i])
                #print(f"{x}, {y}")
                new_lat.append(x)
                new_lon.append(y)

        return new_lat, new_lon