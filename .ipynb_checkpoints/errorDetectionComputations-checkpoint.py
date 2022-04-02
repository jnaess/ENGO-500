import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

from opps import Opps
from point import Coord
from ellipse import Ellipse
from errorRecorder import ErrorRecorder

class ErrorDetectionComputations(ErrorRecorder):
    """
    Encapsulates many of the error flag and record functionalities
    """
    
    def __init__(self):
        """
        """
        ErrorRecorder.__init__(self)
    
    def update_epoch(self):
        """
        Desc:
            Updates the current epoch values for running evaluations
        Input:
            index, of the values sent in
            row, of the current dataframe 
        Output:
        """  
            
        
        if self.first:
            self.first_epoch()
            
        elif self.is_static:
            self.static_epoch()
            self.compute_errors()
            
        else:
            self.dynamic_epoch()
            self.compute_errors()
        
    
    def first_epoch(self):
        """
        Desc:
            Opperations for updating the first Epoch
        Input:
        Output:
        """
        #setup the initial coords
        #of the "real" locations
        self.prev = Coord(0,0) 
        self.curr = Ellipse(self.row["easting"], self.row["northing"], std = [self.row["east_sig"], self.row["north_sig"]])

            #update epochs
        self.prev_Epoch = 0
        self.curr_Epoch = self.row["epoch"]
        
        if self.is_static:
            #of the true locations
            self.prev_True = self.true_coord()
            self.curr_True = self.prev_True
        else:
            self.curr_True = self.true_coord()
        
        
    def static_epoch(self):
        """
        Desc:
            Opperation to update a static epoch
        Input
        Output:
        """
        #of the true locations
        self.prev_True = self.curr_True
        self.curr_True = self.true_coord()
        
                    #update "real" positions
        self.prev = self.curr
        self.curr = Ellipse(self.row["easting"], self.row["northing"], std = [self.row["east_sig"], self.row["north_sig"]])
                
            #epdate epochs
        self.prev_Epoch = self.curr_Epoch
        self.curr_Epoch = self.row["epoch"]
            
            #previous real and current real
        self.dist_to_prev = self.distance(self.prev, self.curr) #float
            
            #current real and current true
        self.dist_to_true = self.distance(self.curr_True, self.curr) #float
            
            #current vector to true
        self.curr_vector_to_true = self.vector(self.curr_True, self.curr) #Coord()
            
            #previous vector to true
        self.prev_vector_to_true = self.vector(self.curr_True, self.prev) #Coord()
            
            #change in error *this is what gets recorded*
        self.error_change = Coord(self.curr_vector_to_true.E() - self.prev_vector_to_true.E(),
                                     self.curr_vector_to_true.N() - self.prev_vector_to_true.N()) #Coord()
        
        
    def dynamic_epoch(self):
        """
        Desc:
            Opperation to update a static epoch
        Input
        Output:
        """
        #of the true locations
        self.prev_True = self.curr_True
        self.curr_True = self.true_coord(self.i)
        
        #update "real" positions
        self.prev = self.curr
        self.curr = Ellipse(self.row["easting"], self.row["northing"], std = [self.row["east_sig"], self.row["north_sig"]])
                
            #epdate epochs
        self.prev_Epoch = self.curr_Epoch
        self.curr_Epoch = self.row["epoch"]
            
            #previous real and current real
        self.dist_to_prev = self.distance(self.prev, self.curr) #float
            
            #current real and current true
        self.dist_to_true = self.distance(self.curr_True, self.curr) #float
            
            #current vector to true
        self.curr_vector_to_true = self.vector(self.curr_True, self.curr) #Coord()
            
            #previous vector to true
        self.prev_vector_to_true = self.vector(self.prev_True, self.prev) #Coord()
            
            #change in error *this is what gets recorded*
        self.error_change = Coord(self.curr_vector_to_true.E() - self.prev_vector_to_true.E(),
                                     self.curr_vector_to_true.N() - self.prev_vector_to_true.N()) #Coord()    
        
    def compute_errors(self):
        """
        Desc:
            Checks for and computes errors
        Input:
            self.prev
            self.curr
        Output:
            self.track_jump
            self.blunder
        """    
        self.flag_errors()

        self.record_errors()
