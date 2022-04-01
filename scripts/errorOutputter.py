import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

class ErrorOutputter():
    """
    Assembles the completed error lists into analyst level data
    """
    
    def __init__(self):
        """
        Desc:
        Input:
            #track jump stuff
            self.jump_status #T/F
            self.jump_individual #float [E, N]
            self.jump_cumulative #cumulative [E, N]
            self.jump_absolute_cumulative #absolute cumulative [E, N]

            self.drift_status #T/F
            self.drift_individual #float [E, N]
            self.drift_cumulative  #cumulative [E, N]
            self.drift_absolute_cumulative #absolute cumulative [E, N]

            self.error_status #T/F
            self.error_individual #cumulative [E, N]
            self.error_cumulative #cumulative [E, N]
            self.error_absolute_cumulative #absolute cumulative [E, N]
        Output:
        """
        
    def generate_error_dataframe(self):
        """
        Desc:
            assembles all of the data into a dataframe
        Input:
        Output:
            self.jump_df
            self.drift_df
            seld.errors_df
        """
        self.generate_keys()
        
        self.jump_df = pd.DataFrame(self.jump_keys)
        self.drift_df = pd.DataFrame(self.drift_keys)
        self.errors_df = pd.DataFrame(self.error_keys)
        
        #self.new_df = pd.DataFrame(keys)
        #self.final_df = pd.concat([self.data,self.new_df], axis=0, ignore_index=True)
        
    def generate_keys(self):
        """
        Desc:
            Generates keys for all of the 'minor' dataframes
        Input:
        Output:
        """
        self.generate_jump_keys()
        self.generate_drift_keys()
        self.generate_error_keys()
        
    def generate_jump_keys(self):
        """
        Desc:
            Generates the jump error key
        Input:
        Output:
            self.jump_keys
        """
        self.jump_keys = {
                'Jump_Status': self.jump_status, #T/F
                'Jump_Individual_E': self.jump_individual[0][:], #float [E
                'Jump_Individual_N': self.jump_individual[1][:], #float [N]
                'Jump_Cumulative_E': self.jump_cumulative[0][:], #cumulative [E]
                'Jump_Cumulative_N': self.jump_cumulative[1][:], #cumulative [N]
                'Jump_Absolute_Cumulative_E': self.jump_absolute_cumulative[0][:], #absolute cumulative [E]
                'Jump_Absolute_Cumulative_N': self.jump_absolute_cumulative[1][:]} #absolute cumulative [N]

    def generate_drift_keys(self):
        """
        Desc:
            Generates the jump error key
        Input:
        Output:
            self.drift_keys
        """
        self.drift_keys = {
                'Drift_Status': self.drift_status, #T/F
                'Drift_Individual_E': self.drift_individual[0][:], #float [E, N]
                'Drift_Individual_N': self.drift_individual[1][:], #float [E, N]
                'Drift_Cumulative_E': self.drift_cumulative[0][:],  #cumulative [E, N]
                'Drift_Cumulative_N': self.drift_cumulative[1][:],  #cumulative [E, N]
                'Drift_Absolute_Cumulative_E': self.drift_absolute_cumulative[0][:], #absolute cumulative [E, N]
                'Drift_Absolute_Cumulative_N': self.drift_absolute_cumulative[1][:]} #absolute cumulative [E, N]

    def generate_error_keys(self):
        """
        Desc:
            Generates the jump error key
        Input:
        Output:
            self.error_keys
        """
        self.error_keys = {
                'Error_Status': self.error_status, #T/F
                'Error_Individual_E': self.error_individual[0][:], #cumulative [E, N]
                'Error_Individual_N': self.error_individual[1][:], #cumula[0][:]tive [E, N]
                'Error_Cumulative_E': self.error_cumulative[0][:], #cumula[0][:]tive [E, N]
                'Error_Cumulative_N': self.error_cumulative[1][:], #cumulative [E, N]
                'Error_Absolute_Cumulative_E': self.error_absolute_cumulative[0][:], #absolute cumulative [E, N]
                'Error_Absolute_Cumulative_N': self.error_absolute_cumulative[1][:]} #absolute cumulative [E, N]
        
        