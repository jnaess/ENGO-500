import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

from opps import Opps
from point import Coord
from ellipse import Ellipse
from errorDetectionComputations import ErrorDetectionComputations

class ErrorDetectionInitializer(ErrorDetectionComputations):
    """
    Assist with initializing and incrementing errors
    """
    
    def __init__(self, data, true_east, true_north, tractor_speed = 1, epoch_frequency = 1, rename_keys = ["Unnamed: 0", "new_lat", "new_lon", "lat σ", "lon σ"], is_static = True, true_std = [1,1]):
        """
        Desc:
        Input:
        Output:
        """
        ErrorDetectionComputations.__init__(self)
        
        self.old_df = data
        self.true_east = true_east
        self.true_north = true_north
        self.true_std = true_std
        #self.true_coord = Ellipse(true_east, true_north, std = true_std)
        self.truth_i = 0 #increment for which coord we are refering to as truth
        
        self.initialize_arrays()
        
        #for picking between kinematic and static error detection techniques
        self.is_static = is_static
        
        self.rename_keys = rename_keys
        self.test_values = ["epoch", "easting", "northing", "east_sig", "north_sig"]
        
        #generate the correct dataframe that we will use
        self.clean_data()
    
    def true_coord(self, i=0):
        """
        Desc:
            Updated the 'true' coord
        Input:
        Output:
        """
        if self.is_static:
            return Ellipse(self.true_east[i], self.true_north[i], std = self.true_std)
        else:
            #then it is expecting a list for each truth
            self.truth_i = self.truth_i + 1
            return Ellipse(self.true_east[i], self.true_north[i], std = [self.true_std[0][i],self.true_std[1][i]])
        
        
    def initialize_arrays(self):
        """
        Desc:
            Initializes the numpy arrays for storage of error values
        Input:
            self.old_df
        Output:
        """
        #columns for data
        self.rows = len(self.old_df.index)
        
        #track jump stuff
        self.jump_status = np.empty(self.rows) #T/F
        self.jump_individual = np.zeros((self.rows,2)) #float [E, N]
        self.jump_cumulative = np.zeros((self.rows,2)) #cumulative [E, N]
        self.jump_absolute_cumulative = np.zeros((self.rows,2)) #absolute cumulative [E, N]
        
        self.drift_status = np.empty(self.rows) #T/F
        self.drift_individual = np.zeros((self.rows,2)) #float [E, N]
        self.drift_cumulative = np.zeros((self.rows,2)) #cumulative [E, N]
        self.drift_absolute_cumulative = np.zeros((self.rows,2)) #absolute cumulative [E, N]
        
        self.error_status = np.empty(self.rows) #T/F
        self.error_individual = np.zeros((self.rows,2)) #cumulative [E, N]
        self.error_cumulative = np.zeros((self.rows,2)) #cumulative [E, N]
        self.error_absolute_cumulative = np.zeros((self.rows,2)) #absolute cumulative [E, N]
        
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