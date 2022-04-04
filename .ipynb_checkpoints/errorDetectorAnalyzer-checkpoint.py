import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from plotter import Plotter

class ErrorDetectorAnalyzer():
    """
    Generates ED analysis
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        
    def generate_error_detection_report(self):
        """
        Desc:
        Input:
        Output:
        """
        self.generate_drift_analysis()
        
        self.generate_jump_analysis()
        
        self.generate_overall_analysis()
        
    def generate_drift_analysis(self):
        """
        Desc:
        Input:
        Output:
        """
        #Simulated vs. Detected Cumulating Easting Drift
        self.sim_v_ED_cum_easting_drift_plot = self.plot_g()

        #"Simulated vs. Detected Cumulating Northing Drift"
        self.sim_v_ED_cum_northing_drift_plot = self.plot_h()
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_easting_drift_plot = self.plot_i()
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_northing_drift_plot = self.plot_j()
        
    def generate_jump_analysis(self):
        """
        Desc:
        Input:
        Output:
        """
        #Simulated vs. Detected Cumulating Easting Jumps
        self.sim_v_ED_cum_easting_jump_plot = self.plot_k()

        #"Simulated vs. Detected Cumulating Northing Drift"
        self.sim_v_ED_cum_northing_jump_plot = self.plot_l()
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_easting_jump_plot = self.plot_m()
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_northing_jump_plot = self.plot_n()
        
    def generate_overall_analysis(self):
        """
        Desc:
        Input:
        Output:
        """
        #Simulated vs. Detected Cumulating Easting Jumps
        self.sim_v_ED_cum_easting_all_plot = self.plot_o()

        #"Simulated vs. Detected Cumulating Northing Drift"
        self.sim_v_ED_cum_northing_all_plot = self.plot_p()
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_easting_all_plot = self.plot_q()
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_northing_all_plot = self.plot_r()