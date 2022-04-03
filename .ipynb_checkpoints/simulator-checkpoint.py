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

from polygon import polygon
from point import Coord
from geomTools import GeomTools
from pathGenerator import PathGenerator
from positionGenerator import PositionGenerator
from pathFollower import PathFollower
from errorSimulator import ErrorSimulator
from passGenerator import PassGenerator
from spatialOpps import SpatialOpps

class Simulator(SpatialOpps, PassGenerator):
    """
    Contains and manages the simulation of our data
    """

    def __init__(self, vertices, inProj = 4326, outProj = 3857, to_out = False, interval = 1, tractor_width = 1.5, use_drift = False, use_jump=False, easting_drift_const = .01,
                northing_drift_const = .01):
        """
        Desc:
        Input:
            vertices, [[E,N], ... , [E,N]] must be clockwise!!!
            inProj
            outProj
            to_out, True/False --> it True, then imidiately change coords to the Out projection
        Output:
        """
        SpatialOpps.__init__(self)
        
        self.inProj = inProj
        self.outProj = outProj
        self.to_out = to_out

        
        self.read_in_vertices(vertices)
        
        PassGenerator.__init__(self, vertices = self.vertices, tractor_width = tractor_width, interval = interval, es = ErrorSimulator(use_drift, use_jump, easting_drift_const = easting_drift_const,
                northing_drift_const = northing_drift_const))
        
        self.analyze()

        
    def read_in_vertices(self, vertices):
        """
        Desc:
            Reads in the vertices and converts their points as needed
        Input:
            vertices, [[E,N], ... , [E,N]] must be clockwise!!!
            inProj
            outProj
            to_out, True/False --> it True, then imidiately change coords to the Out projection
        Output:
            self.vertices
        """
        self.vertices = []
        
        for point in vertices:
            self.vertices.append(Coord(point[0],point[1], inProj = self.inProj, outProj = self.outProj, to_out = self.to_out))
        
    def analyze(self):
        """
        Desc:
            Conducts all analyse opperations from start to end
        Input:
            self.true_passes, [PathFollower(), ... , PathFollower()]
            self.real_passes, [PathFollower(), ... , PathFollower()]
            self.tractor_width
        Output:
        """
        self.setup_shapes()
    
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
        
        #generate inner and outer field shapes
        self.inner_gdf = self.gdf_polygon(self.inner)
        self.outer_gdf = self.gdf_polygon(self.outer)
        
        #zero_pass
        self.temp = gpd.overlay(self.T_gdf_poly, self.R_gdf_poly, how='difference')
        self.zero_pass = gpd.overlay(self.inner_gdf, self.temp, how='intersection') #only take real that is inside inner

        #single pass
        self.temp2 = gpd.overlay(self.inner_gdf, self.R_gdf_poly, how="intersection") #only take what was inside inner
        self.single_pass = gpd.overlay(self.R_gdf_poly, self.temp2, how="intersection") #not covered by real pass either
        
        #double pass --> this does NOT account for passes overlapping eachother
        self.temp3 = gpd.overlay(self.R_gdf_poly, self.inner_gdf, how="difference") #only take what was outside inner
        self.double_pass = gpd.overlay(self.temp3, self.T_gdf_poly, how='difference')  #only take waht was not already going to be passed by true path