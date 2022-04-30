import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from simulator import Simulator
from errorDetector import ErrorDetector
from databaseManager import DatabaseManager
from analyzer import Analyzer
from point import Coord

class Manager(DatabaseManager, Analyzer):
    """
    Contains all simulation and error detection software to execute the primary processes in one centralized location
    """
    
    def __init__(self, 
                 field = [[0,0],[0,10],[10,10],[10,0]],
                 use_drift = True, 
                 use_jump = True, 
                 easting_drift_const = .001,
                 northing_drift_const = .001,
                 mean_jump = Coord(0,0,std = [.05, .05]),
                 jump_occurance_probability = 5,
                 drift_variability = Coord(0,0, std = [.0001, .0001]),
                 easting_jump_const = .2,
                 northing_jump_const = .2,
                 tractor_speed = 1, 
                 epoch_frequency = 1, 
                 rename_keys = ["epoch", "real_e", "real_n", "real_e_std", "real_n_std"], 
                 is_static = False, 
                 true_std = [.1,.1],
                tractor_width = 1.5,
                display = False):
        """
        Desc:
        Input:
        Output
        """
        DatabaseManager.__init__(self)
        Analyzer.__init__(self, display = display)
        
        #simulator stuff
        self.field = field
        self.use_drift = use_drift
        self.use_jump = use_jump
        self.easting_drift_const = easting_drift_const
        self.northing_drift_const = northing_drift_const
        self.mean_jump = mean_jump
        self.jump_occurance_probability = jump_occurance_probability
        self.drift_variability = drift_variability
        self.easting_jump_const = easting_jump_const
        self.northing_jump_const = northing_jump_const
        self.tractor_width = tractor_width
        
        #error detector parameters
        self.tractor_speed = tractor_speed
        self.epoch_frequency = epoch_frequency 
        self.rename_keys = rename_keys
        self.is_static = is_static
        self.true_std = true_std
        
        self.retrieve_sim_data()
        self.initialize_simulator()
        self.initialize_error_detector()
        self.generate_analytics()
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
        #self.field = [[0,0],[0,10],[10,10],[10,0]]
        #self.field = [[0,0],[0,12],[10,12],[10,0]]
        #self.field = [[0,0],[0,100],[100,100],[100,0]]
        #self.field = [[0,0],[-10,10],[0,20],[10,10]]
        #generates simulation tracks
        self.Sim = Simulator(vertices = self.field, 
                             use_drift = self.use_drift,
                                use_jump = self.use_jump,
                                easting_drift_const = self.easting_drift_const,
                                northing_drift_const = self.northing_drift_const,
                                mean_jump = self.mean_jump,
                                jump_occurance_probability = self.jump_occurance_probability,
                                drift_variability = self.drift_variability,
                            easting_jump_const = self.easting_jump_const,
        northing_jump_const = self.northing_jump_const,
                            tractor_width = self.tractor_width)

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

        #run error detector simulation
        self.ED = ErrorDetector(self.df_sim, 
                                tru_E, 
                                tru_N, 
                                rename_keys = self.rename_keys, 
                                true_std = std, 
                                is_static=self.is_static)

        #store error detector values as a dataframe
        self.ED.generate_error_dataframe()

        #store error_detector values
        self.df_err_jump = self.ED.jump_df
        self.df_err_drift = self.ED.drift_df
        self.df_err_errors = self.ED.errors_df
        
        self.df_ED = pd.concat([self.ED.jump_df,self.ED.drift_df, self.ED.errors_df], axis=1)
        
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
        
        