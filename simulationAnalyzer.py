import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from plotter import Plotter

class SimulationAnalyzer():
    """
    Generates ED analysis
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        
    def generate_simulation_report(self):
        """
        Desc:
        Input:
        Output:
        """
        self.zero_pass_analysis()
        
        self.single_pass_analysis()
        
        self.double_pass_analysis()
        
        self.track_summary_analysis()
        
        self.general_sim_analysis()
        
    def general_sim_analysis(self):
        """
        Desc:
        Input:
        Output:
        """
        self.sim_jumps = sum(self.df_sim.jump_status.to_list())
        self.sim_drifts = sum(self.df_sim.drift_status.to_list())
        self.sim_errors = sum(self.df_sim.error_status.to_list())
        
        
        self.sim_err_cum_n = self.df_sim.error_cumulative_n.to_list()[-1]
        self.sim_err_cum_e = self.df_sim.error_cumulative_e.to_list()[-1]
        self.sim_drift_cum_n = self.df_sim.drift_cumulative_n.to_list()[-1]
        self.sim_drift_cum_e = self.df_sim.drift_cumulative_e.to_list()[-1]
        self.sim_jump_cum_n = self.df_sim.jump_cumulative_n.to_list()[-1]
        self.sim_jump_cum_e = self.df_sim.jump_cumulative_e.to_list()[-1]
        
        self.pass_to_pass_sim_n = self.sim_err_cum_n/(self.df_sim.index.to_list()[-1]+1)*15*60
        self.pass_to_pass_sim_e = self.sim_err_cum_e/(self.df_sim.index.to_list()[-1]+1)*15*60
        
    def zero_pass_analysis(self):
        """
        Desc:
        Input:
        Output:
            self.zero_pass_plot
            self.zero_pass_area
        """
        self.zero_pass_plot = self.plot_b()
        
        self.zero_pass_area = sum(self.Sim.zero_pass.area)
        
    def single_pass_analysis(self):
        """
        Desc:
        Input:
        Output:
            self.single_pass_plot
            self.single_pass_area
        """
        self.single_pass_plot = self.plot_c()
        
        self.single_pass_area = sum(self.Sim.single_pass.area)
        
    def double_pass_analysis(self):
        """
        Desc:
        Input:
        Output:
            self.double_pass_plot
            self.double_pass_area
        """
        self.double_pass_plot = self.plot_d()
        
        self.double_pass_area = sum(self.Sim.double_pass.area)
        
    def track_summary_analysis(self):
        """
        Desc:
        Input:
        Output:
            self.clean_track_plot
            self.track_summary_plot
        """
        self.clean_track_plot = self.plot_a() #just of the x and y lines
        
        self.track_summary_plot = self.plot_e() #all poly layers on top of eachother
