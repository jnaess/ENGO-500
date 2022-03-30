import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

from opps import Opps
from point import Coord
from ellipse import Ellipse
from errorDetectionComputations import ErrorDetectionComputations
from errorDetectionInitializer import ErrorDetectionInitializer

class ErrorDetector(Opps, ErrorDetectionInitializer):
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
        ErrorDetectionInitializer.__init__(self, data, true_east, true_north, tractor_speed, epoch_frequency, rename_keys, is_static, true_std)

        
    def detect_errors(self):
        """
        Desc:
            Iterated through and computes the drift, pass-to-pass and track jump errors
        Input:
        Output:
        """
        
        self.first = True
        
        for index, row in self.data.iterrows():  
            self.i = index
            self.row = row
            
            #updated for this epochs values
            self.update_epoch()

            if self.first:
                #skip the first row
                self.first = False
                
            else:
                self.compute_errors()
                
                return
                


