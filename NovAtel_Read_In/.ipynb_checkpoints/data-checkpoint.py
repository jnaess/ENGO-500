import numpy as np
from pyproj import Proj, transform, Transformer
from pyproj.transformer import TransformerGroup
import pandas as pd
from gnss_headers import GNSS_Headers
import sys
from tqdm import tqdm
        
        
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
                device = line.split(",")[0]
                data = self.clean_and_split(line)

                if device == '#RTKPOSA':
                    #then rtk
                    self.rtk_data.append(data)
                elif device == '#PPPPOSA':
                    #then ppp
                    self.ppp_data.append(data)
                elif device == '#PSRPOSA':
                    #then psr
                    self.psr_data.append(data)
                else:
                    print(device)
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
        self.rtk = self.clean(pd.DataFrame(self.rtk_data, columns=self.rtk_cols))
        
        self.ppp = self.clean(pd.DataFrame(self.ppp_data, columns=self.ppp_cols))        
        
        self.psr = self.clean(pd.DataFrame(self.psr_data, columns=self.psr_cols))
        
        
    def fake_append(self):
        """
        Desc:
            adds the filler zeros fro Jonah
        Input:
        Output:
        """
        rows = self.rtk.shape[0]
        fake = np.zeros(rows)
        self.rtk["new_lat"] = fake
        self.rtk["new_lon"] = fake

        rows = self.ppp.shape[0]
        fake = np.zeros(rows)
        self.ppp["new_lat"] = fake
        self.ppp["new_lon"] = fake
        
        rows = self.psr.shape[0]
        fake = np.zeros(rows)
        self.psr["new_lat"] = fake
        self.psr["new_lon"] = fake
        
    def convert_append(self):
        """
        Desc:
            adds the converted coords
        Input:
        Output:
        """
        lat, lon = self.convert(self.rtk["lat"],self.rtk["lon"])
        self.rtk["new_lat"] = lat
        self.rtk["new_lon"] = lon
        
        lat, lon = self.convert(self.ppp["lat"],self.ppp["lon"])
        self.ppp["new_lat"] = lat
        self.ppp["new_lon"] = lon
        
        lat, lon = self.convert(self.psr["lat"],self.psr["lon"])
        self.psr["new_lat"] = lat
        self.psr["new_lon"] = lon
        
    
    def clean(self, df):
        """
        Desc:
            cleans the dataframes 
        Input:
            dataframe to be cleaned
        Output:
        """
        #remove all insuficient obs
        df = df.drop(df[df.sol_status == "INSUFFICIENT_OBS"].index)
        
        return df
        
    def convert(self, lat, lon, in_proj = "epsg:3780", out_proj = "epsg:2955"):
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
        lat = np.array(lat)
        lon = np.array(lon)
        
        new_lat = np.empty(len(lat))
        new_lon = np.empty(len(lon))
        
        if len(lat) == len(lon) and len(lat) > 0:
            #then these are conditions that we can convert in
            #inProj = Proj(init=in_proj)
            #outProj = Proj(init=out_proj)
            

            
            transformer = Transformer.from_crs(in_proj,out_proj)
            xy = transformer.transform(lat,lon)

            new_lat = xy[0]
            new_lon = xy[1]
            
            """
            with tqdm(total=len(lat), file=sys.stdout) as pbar:
                for i in range(len(lat)):
                    x,y = transformer.transformer[0].transform(lon[i],lat[i])
                    
                    new_lat[i] = x
                    new_lon[i] = y
                      
                    pbar.set_description("converted: %d" % (1+i))
                    pbar.update(1)"""

        return new_lat, new_lon
    
    def add_to_csv(self):
        """
        Desc:
            converts the three dataframes to a csv file
        Input:
            self.rtk,
            self.ppp,
            self.psr
        Output:
        """
        self.rtk.to_csv("rtk.csv")
        self.ppp.to_csv("ppp.csv")
        self.psr.to_csv("psr.csv")