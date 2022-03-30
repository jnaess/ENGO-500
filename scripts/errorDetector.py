import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

from opps import Opps
from point import Coord
from ellipse import Ellipse
from errorDetectionComputations import ErrorDetectionComputations

class ErrorDetector(Opps, ErrorDetectionComputations):
    """
    Desc:
        Detects errors from either a static or movind dataset
    """
    
    def __init__(self, data, true_east, true_north, tractor_speed = 1, epoch_frequency = 1, rename_keys = ["Unnamed: 0", "new_lat", "new_lon", "lat σ", "lon σ"], is_static = True, true_std = [1,1]):
        """
        Desc:
        Input:
             data, dataframe of the data to be read in
             T_E, either a single value or a list of true values corresponding to each epoch (east)
             T_N, either a single value or a list of true values corresponding to each epoch(north)
             true_std = [E, N]
             tractor_speed = 1,  (m/sec)
             epoch_frequency = 1 (sec/epoch)
             rename_keys, columns to rename so that we have [Epoch, Easting, Northing] {"Unnamed: 0": "Epoch", "new_lat": "Easting", "new_lon":"Northing"}
             is_static = True
        Output:
            self.true_coord = Ellipse(true_east, true_north) --> to be updated for the expected truth at each epoch of a kinetic error detection
        """
        Opps.__init__(self)
        ErrorDetectionComputations.__init__(self)
        
        self.old_df = data
        self.true_east = true_east
        self.true_north = true_north
        self.true_coord = Ellipse(true_east, true_north, std = true_std)
        
        #for picking between kinematic and static error detection techniques
        self.is_static = is_static
        
        self.rename_keys = rename_keys
        self.test_values = ["Epoch", "Easting", "Northing", "East_Sig", "North_Sig"]
        
        #generate the correct dataframe that we will use
        self.clean_data()
        
    def clean_data(self):
        """
        Desc:
        Input:
            self.old_df
            self.rename_to
        Output
            self.names = {"Unnamed: 0": "Epoch", "new_lat": "Easting", "new_lon":"Northing"}
        """
        #map out column names to change
        self.names = {self.rename_keys[i]: self.test_values[i] for i in range(len(self.rename_keys))}
        
        #change column values
        self.data = self.old_df.rename(columns=self.names)[self.test_values]
        
    def detect_errors(self):
        """
        Desc:
            Iterated through and computes the drift, pass-to-pass and track jump errors
        Input:
        Output:
        """
        
        self.first = True
        
        for index, row in self.data.iterrows():  
            
            #updated for this epochs values
            self.update_epoch(index, row)

            if self.first:
                #skip the first row
                self.first = False
                
            else:
                self.compute_errors()
                
                return
                
    def update_epoch(self, index, row):
        """
        Desc:
            Updates the current epoch values for running evaluations
        Input:
            index, of the values sent in
            row, of the current dataframe 
        Output:
        """
        if self.first:
            #setup the initial coords
            #of the "real" locations
            self.prev = Coord(0,0) 
            self.curr = Ellipse(row["Easting"], row["Northing"], std = [row["East_Sig"],row["North_Sig"]])

            #update epochs
            self.prev_Epoch = 0
            self.curr_Epoch = row["Epoch"]

            #of the true locations
            self.prev_True = self.true_coord
            self.curr_True = self.true_coord
        
        if self.is_static:
            #update "real" positions
            self.prev = self.curr
            self.curr = Ellipse(row["Easting"], row["Northing"], std = [row["East_Sig"], row["North_Sig"]])
                
            #epdate epochs
            self.prev_Epoch = self.curr_Epoch
            self.curr_Epoch = row["Epoch"]
            
            #previous real and current real
            self.dist_to_prev = self.distance(self.prev, self.curr)
            
            #current real and current true
            self.dist_to_true = self.distance(self.curr_True, self.curr)
            
            #vector to true
            self.curr_vector_to_true = self.vector(self.curr_True, self.curr)
            
                
                
        print(index)
        print(row)
        return
