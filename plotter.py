import matplotlib.pyplot as plt
import numpy as np

from basePlot import BasePlot

class Plotter(BasePlot):
    """
    Generates the plots for our reports
    Sister class to Manager
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        BasePlot.__init__(self)
        
        #attempted path versus real path plot
        #---> self.plot_a()
        
        #zero pass plot
        #---> self.plot_b()
        
        #one pass plot
        
        #double pass plot
        
        #position drift plot
        
    def plot_a(self):
        """
        Desc:
        Input:
            self.df_sim
        Output:
        """
        self.plot_fig(x = [self.df_sim.true_e.to_list(),self.df_sim.real_e.to_list()],
                      y = [self.df_sim.true_n.to_list(),self.df_sim.real_n.to_list()], 
                      line_label = ["True", "Real"],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "True Track")
        
    def plot_b(self):
        """
        Desc:
        Input:
            self.Sim.gdf_pt
        Output:
        """
        self.plot_gdf(shapes = [self.Sim.zero_pass],
                      shape_colors = ['red'],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "Zero Pass")
        
    def plot_c(self):
        """
        Desc:
        Input:
            self.Sim.gdf_pt
        Output:
        """
        self.plot_gdf(shapes = [self.Sim.single_pass, self.Sim.zero_pass],
                      shape_colors = ['orange', '#915ebd'],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "True Track")
