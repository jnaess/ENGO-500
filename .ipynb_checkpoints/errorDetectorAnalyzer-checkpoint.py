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
        
        self.general_ED_analysis()
        
    def general_ED_analysis(self):
        """
        Desc:
        Input:
        Output:
        """
        self.ed_jumps = sum(self.df_ED.jump_status.to_list())
        self.ed_drifts = sum(self.df_ED.drift_status.to_list())
        self.ed_errors = sum(self.df_ED.error_status.to_list())
        
        
        self.ed_err_cum_n = self.df_ED.error_cumulative_n.to_list()[-1]
        self.ed_err_cum_e = self.df_ED.error_cumulative_e.to_list()[-1]
        self.ed_drift_cum_n = self.df_ED.drift_cumulative_n.to_list()[-1]
        self.ed_drift_cum_e = self.df_ED.drift_cumulative_e.to_list()[-1]
        self.ed_jump_cum_n = self.df_ED.jump_cumulative_n.to_list()[-1]
        self.ed_jump_cum_e = self.df_ED.jump_cumulative_e.to_list()[-1]
        
        self.pass_to_pass_ed_n = self.ed_err_cum_n/(self.df_ED.index.to_list()[-1]+1)*15*60
        self.pass_to_pass_ed_e = self.ed_err_cum_e/(self.df_ED.index.to_list()[-1]+1)*15*60
        
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
        
        #"Simulated vs. Detected Individual Difference Easting Drifts"
        self.sim_v_ED_diff_easting_drift_plot = self.plot_s()
        
        #"Simulated vs. Detected Individual Difference Easting Drifts"
        self.sim_v_ED_diff_northing_drift_plot = self.plot_t()
        
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
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_easting_jump_plot = self.plot_u()
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_northing_jump_plot = self.plot_v()
        
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
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_easting_all_plot = self.plot_w()
        
        #"Simulated vs. Detected Individual Easting Drifts"
        self.sim_v_ED_idv_northing_all_plot = self.plot_x()