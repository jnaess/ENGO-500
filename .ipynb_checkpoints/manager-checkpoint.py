import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from simulator import Simulator
from errorDetector import ErrorDetector
from databaseManager import DatabaseManager
from plotter import Plotter

class Manager(DatabaseManager, Plotter):
    """
    Contains all simulation and error detection software to execute the primary processes in one centralized location
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output
        """
        DatabaseManager.__init__(self)
        Plotter.__init__(self)
        
        self.retrieve_sim_data()
        self.initialize_simulator()
        self.initialize_error_detector()
        #self.push_data()
    
    def retrieve_sim_data(self, sim_id = -1):
        """
        Desc:
            Retieves data from the 'simulations' table for the specified simulation
        Input:
        Output:
        """
        con = self.engine.connect()

        self.sim_df= pd.DataFrame(self.select_all(con=con, table = 'simulations'))
        
        if sim_id == -1:
            #set simulation number for reference
            self.sim_id = self.sim_df.id.max()
        else:
            self.sim_id = sim_id
            
        con.close()
        
    def initialize_simulator(self):
        """
        Desc:
            sets up the simulator that will be used
        Input:
            sim_id
        Output:
            self.sim
        """
        #simulation id for accessing data from database
        sim_id = 2

        #coordinates
        self.field = [[0,0],[0,10],[10,10],[10,0]]

        #generates simulation tracks
        self.Sim = Simulator(self.field, use_drift=True, easting_drift_const = .01, northing_drift_const = .01)

        #generates dataframe of values
        self.Sim.generate_output_tracks()
        
        #stores dataframe of values in a variable
        self.df_sim = self.Sim.output_tracks
        
    def initialize_error_detector(self):
        """
        Desc:
            sets up the error detector
        Input:
        Output:
        """
        #convert index to epochs
        self.df_sim["epoch"] = list(self.df_sim.index.values)

        #get key values as lists to be passed in
        std = [self.df_sim['true_e_std'].to_list(),self.df_sim['true_n_std'].to_list()]
        tru_N = self.df_sim['true_n'].to_list()
        tru_E = self.df_sim['true_e'].to_list()
        rename_keys = ["epoch", "real_e", "real_n", "real_e_std", "real_n_std"]

        #run error detector simulation
        self.ED = ErrorDetector(self.df_sim, tru_E, tru_N, rename_keys = rename_keys, true_std = std, is_static=False)

        #store error detector values as a dataframe
        self.ED.generate_error_dataframe()

        #store error_detector values
        self.df_err_jump = self.ED.jump_df
        self.df_err_drift = self.ED.drift_df
        self.df_err_errors = self.ED.errors_df
        
    def push_data(self):
        """
        Desc:
            pushes the set up datframes into the database
        Input:
        Output:
        """
        con = self.engine.connect()

        self.df_err_jump["sim_id"] = np.ones(len(self.df_err_jump.index))*self.sim_id
        self.df_err_jump["epoch"] = list(self.df_err_jump.index.values)

        self.df_err_jump["jump_status"] = self.df_err_jump["jump_status"].astype('bool')

        self.df_err_jump.to_sql('error_detector_jumps', con=con, if_exists='append', index=False)
        
        con.close()
        
        