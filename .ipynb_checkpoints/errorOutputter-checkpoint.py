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
                'jump_status': self.jump_status[1:], #T/F
                'jump_individual_e': self.jump_individual[0][1:], #float [E
                'jump_individual_n': self.jump_individual[1][1:], #float [N]
                'jump_cumulative_e': self.jump_cumulative[0][1:], #cumulative [E]
                'jump_cumulative_n': self.jump_cumulative[1][1:], #cumulative [N]
                'jump_absolute_cumulative_e': self.jump_absolute_cumulative[0][1:], #absolute cumulative [E]
                'jump_absolute_cumulative_n': self.jump_absolute_cumulative[1][1:]} #absolute cumulative [N]

    def generate_drift_keys(self):
        """
        Desc:
            Generates the jump error key
        Input:
        Output:
            self.drift_keys
        """
        self.drift_keys = {
                'drift_status': self.drift_status[1:], #T/F
                'drift_individual_e': self.drift_individual[0][1:], #float [E, N]
                'drift_individual_n': self.drift_individual[1][1:], #float [E, N]
                'drift_cumulative_e': self.drift_cumulative[0][1:],  #cumulative [E, N]
                'drift_cumulative_n': self.drift_cumulative[1][1:],  #cumulative [E, N]
                'drift_absolute_cumulative_e': self.drift_absolute_cumulative[0][1:], #absolute cumulative [E, N]
                'drift_absolute_cumulative_n': self.drift_absolute_cumulative[1][1:]} #absolute cumulative [E, N]

    def generate_error_keys(self):
        """
        Desc:
            Generates the jump error key
        Input:
        Output:
            self.error_keys
        """
        self.error_keys = {
                'error_status': self.error_status[1:], #T/F
                'error_individual_e': self.error_individual[0][1:], #cumulative [E, N]
                'error_individual_n': self.error_individual[1][1:], #cumula[0][:]tive [E, N]
                'error_cumulative_e': self.error_cumulative[0][1:], #cumula[0][:]tive [E, N]
                'error_cumulative_n': self.error_cumulative[1][1:], #cumulative [E, N]
                'error_absolute_cumulative_e': self.error_absolute_cumulative[0][1:], #absolute cumulative [E, N]
                'error_absolute_cumulative_n': self.error_absolute_cumulative[1][1:]} #absolute cumulative [E, N]
        
        