import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from plotter import Plotter
from errorDetectorAnalyzer import ErrorDetectorAnalyzer
from simulationAnalyzer import SimulationAnalyzer

class Analyzer(Plotter, ErrorDetectorAnalyzer, SimulationAnalyzer):
    """
    Developes the analysis for auto reporting
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        Plotter.__init__(self)
        ErrorDetectorAnalyzer.__init__(self)
        SimulationAnalyzer.__init__(self)
        
        
    def generate_analytics(self):
        """
        Desc:
            Generated all variables with values for the auto reporting
        Input:
        Output:
        """
        self.generate_simulation_report()
        
        self.generate_error_detection_report()
        
        self.sim_err_comparison()
        
    def sim_err_comparison(self):
        """
        Desc:
        Input:
        Output:
        """
        #jump drift error
        self.sim_detected = [round(self.sim_jumps,4),
                             round(self.sim_drifts,4),
                             round(self.sim_errors,4)]
        
        self.ed_detected = [round(self.ed_jumps,4),
                             round(self.ed_drifts,4),
                             round(self.ed_errors,4)]
        
        self.sim_cum_count_e = [round(self.sim_jump_cum_e,4),
                                round(self.sim_drift_cum_e,4),
                               round(self.sim_err_cum_e,4)]
        
        self.sim_cum_count_n = [round(self.sim_jump_cum_n,4),
                                round(self.sim_drift_cum_n,4),
                               round(self.sim_err_cum_n,4)]
        
        self.ed_cum_count_e = [round(self.ed_jump_cum_e,4),
                              round(self.ed_drift_cum_e,4),
                              round(self.ed_err_cum_e,4)]
        
        self.ed_cum_count_n = [round(self.ed_jump_cum_n,4),
                               round(self.ed_drift_cum_n,4),
                              round(self.ed_err_cum_n,4)]
        
        self.ed_detection_accuracy = [round(self.ed_jumps/self.sim_jumps*100, 2),
                                      round(self.ed_drifts/self.sim_drifts*100, 2),
                                      round(self.ed_errors/self.sim_errors*100, 2)]
        
        self.ed_cumulative_accuracy_e = [round(self.ed_jump_cum_e/self.sim_jump_cum_e*100, 2),
                                         round(self.ed_drift_cum_e/self.sim_drift_cum_e*100, 2),
                                         round(self.ed_err_cum_e/self.sim_err_cum_e*100, 2)]
        
        self.ed_cumulative_accuracy_n = [round(self.ed_jump_cum_n/self.sim_jump_cum_n*100, 2),
                                         round(self.ed_drift_cum_n/self.sim_drift_cum_n*100, 2),
                                         round(self.ed_err_cum_n/self.sim_err_cum_n*100, 2)]
        
        # easting northing
        self.ed_pass_to_pass_accuracy = [round(self.pass_to_pass_ed_e/self.pass_to_pass_sim_e*100, 2),
                                         round(self.pass_to_pass_ed_n/self.pass_to_pass_sim_n*100, 2)]
                                         