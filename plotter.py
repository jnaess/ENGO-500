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
        self.plot_fig(shapes = [self.Sim.single_pass],
                      shape_colors = ['#915ebd'],
                      shape_labels = ["Single Pass"],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "True Track")
