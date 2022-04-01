import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point 
from shapely.geometry import LineString
from shapely.geometry import Polygon
import numpy as np

from point import Coord

class SpatialOpps():
    """
    Executes spatial opperations
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        
        return
    
    def setup_gdf(self, passes, tractor_width):
        """
        Desc:
            Sets up the point, linestring, polygon dataframes from the passes
        Input:
            self.passes, [PathFollower(), ... , PathFollower()]
            self.tractor_width --> to generate buffer
        Output:
        """
        myid = np.empty((0))
        myorder = np.empty((0))
        lat = np.empty((0))
        long = np.empty((0))
        for path in passes:
            
            myid = np.concatenate((myid,path.segment_order))
            myorder = np.concatenate((myorder,path.point_order))
            
            #should probably check that it is this way and not the opposite
            lat = np.concatenate((lat,path.e))
            long = np.concatenate((long,path.n))
            
        df = pd.DataFrame(list(zip(myid, myorder, lat, long)), columns =['myid', 'myorder', 'lat', 'long']) 
        gdf_pt = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['long'], df['lat']))
        #display(gdf_pt)
        gdf_line = gdf_pt.sort_values(by=['myorder']).groupby(['myid'])['geometry'].apply(lambda x: LineString(x.tolist()))
        gdf_line = gpd.GeoDataFrame(gdf_line, geometry='geometry')
        #gdf_line.crs = "EPSG:4326"
        #display(gdf_line)
        ax = gdf_line.plot();
        ax.set_aspect('equal')
        #ax.set_xticklabels(ax.get_xticklabels(), rotation=90);
        gdf_poly = gdf_line
        gdf_poly['geometry'] = gdf_line.geometry.buffer(tractor_width/2,cap_style=2)
        #display(gdf_poly)
        #gdf_poly.plot()
        
        return gdf_pt, gdf_line, gdf_poly
    
    def gdf_polygon(self, poly, color='#20873f'):
        """
        Desc:
            Returns the polygon geopandasdataframe of the vertices input
        Input:
            poly, polygon()
            color, colour for the polygon to show up as
                '#20873f' --> dark green
                '#24bf53' --> light green
        Output:
        """
        lat = poly.e
        lon = poly.n

        gdf = gpd.GeoDataFrame()
        gdf['lat'] = lat
        gdf['lon'] = lon

        polygon_geom = Polygon(zip(lon, lat))
        gdf_poly = gpd.GeoDataFrame(index=[0], geometry=[polygon_geom]) 
        
        #add colour
        gdf_poly['color'] = [color]
        
        return gdf_poly
    
    