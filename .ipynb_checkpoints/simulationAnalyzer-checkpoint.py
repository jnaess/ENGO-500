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
        
    def double_pass_analysis(self):
        """
        Desc:
        Input:
        Output:
            self.clean_track_plot
            self.track_summary_plot
        """
        self.clean_track_plot = self.plot_a() #just of the x and y lines
        
        self.track_summary_plot = self.plot_e() #all poly layers on top of eachother
