import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point 
from shapely.geometry import LineString
from shapely.geometry import Polygon
import numpy as np
import math as m
from matplotlib import collections  as mc
import pylab as pl

class ShapeInitializer():
    """
    Helps cleanly initialize the simulator's shapes
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        
    
    def setup_shapes(self):
        """
        Desc:
            Generates all base shapefiles for our analytics
        Input:
            self.true_passes, [PathFollower(), ... , PathFollower()]
            self.real_passes, [PathFollower(), ... , PathFollower()]
            self.tractor_width
        Output:
        """
        #generate true pass shapefiles
        self.T_gdf_pt, self.T_gdf_line, self.T_gdf_poly = self.setup_gdf(self.true_passes, self.tractor_width)
        
        #generate real pass shapefiles
        self.R_gdf_pt, self.R_gdf_line, self.R_gdf_poly = self.setup_gdf(self.real_passes, self.tractor_width)
        
        #set up those files as the plottable ones with labels
        self.init_base()
        
        #generate inner and outer field shapes
        self.init_fields()
        
        #zero_pass
        self.init_zero_pass()
        
        #single pass
        self.init_single_pass()
        
        #double pass --> this does NOT account for passes overlapping eachother
        self.init_double_pass()
        
        
    def init_zero_pass(self):
        """
        Desc:
        Input:
        Output:
        """
        self.temp = gpd.overlay(self.T_gdf_poly, self.R_gdf_poly, how='difference')
        self.zero_pass = gpd.overlay(self.inner_gdf, self.temp, how='intersection') #only take real that is inside inner
        self.zero_pass = self.add_title(self.zero_pass, "Zero Pass")
        
    def init_single_pass(self):
        """
        Desc:
        Input:
        Output:
        """
        #single pass
        #self.temp2 = gpd.overlay(self.inner_gdf, self.R_gdf_poly, how="intersection") #only take what was inside inner
        #self.single_pass = gpd.overlay(self.R_gdf_poly, self.temp2, how="intersection") #not covered by real pass either
        self.single_pass = gpd.overlay(self.R_gdf_poly, self.T_gdf_poly, how="intersection") #any overlap of true and real path
        self.single_pass = self.add_title(self.single_pass, "Single Pass")
        
    def init_double_pass(self):
        """
        Desc:
        Input:
        Output:
        """
        #double pass --> this does NOT account for passes overlapping eachother
        self.temp3 = gpd.overlay(self.R_gdf_poly, self.inner_gdf, how="difference") #only take what was outside inner
        self.double_pass = gpd.overlay(self.temp3, self.T_gdf_poly, how='difference')  #only take waht was not already going to be passed by true path
        self.double_pass = self.add_title(self.double_pass, "Double Pass")
        
    def init_fields(self):
        """
        Desc:
        Input:
        Output:
        """
        #generate inner and outer field shapes
        #inner
        self.inner_gdf = self.gdf_polygon(self.inner)
        self.inner_gdf = self.add_title(self.inner_gdf, "Autonomous\nPortion of Field")
        #outer
        self.outer_gdf = self.gdf_polygon(self.outer)
        self.outer_gdf = self.add_title(self.outer_gdf, "Full Field")
        
    def init_base(self):
        """
        Desc:
        Input:
        Output:
        """      
        
        #generate true pass shapefiles
        self.planned_pt = self.add_title(self.T_gdf_pt, "Planned Locations")
        self.planned_path = self.add_title(self.T_gdf_line, "Planned Path")
        self.planned_track = self.add_title(self.T_gdf_poly, "Planned Track")
        
        #generate real pass shapefiles
        self.actual_pt = self.add_title(self.R_gdf_pt, "Actual Locations")
        self.actual_path = self.add_title(self.R_gdf_line, "Actual Path")
        self.actual_track = self.add_title(self.R_gdf_poly, "Actual Track")