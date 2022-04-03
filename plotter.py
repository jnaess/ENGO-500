import matplotlib.pyplot as plt
import numpy as np

from basePlot import BasePlot
import base64
import io

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
        #self.plot_a()
        
        #zero pass plot
        #self.plot_b()
        
        #one pass plot
        #self.plot_c()
        
        #double pass plot
        #self.plot_d()
        
        #track summary plot
        #self.plot_e #should add "track jump" points labelled
        
        
        
    def convert_to_png(self):
        """
        Desc:
        Input
        Output:
        """
        data = io.BytesIO()
        plt.savefig(data, format='png', bbox_inches="tight")
        plt.close()
        
        encoded_img_data = base64.b64encode(data.getvalue())
        
        return encoded_img_data.decode('UTF-8')
    
    def plot_a(self):
        """
        Desc:
            #attempted path versus real path plot
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.true_e.to_list(),
                           self.df_sim.real_e.to_list()],
                      y = [self.df_sim.true_n.to_list(),
                           self.df_sim.real_n.to_list()], 
                      line_label = ["True", "Real"],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "True Track")
        
        return self.convert_to_png()
                
        
    def plot_b(self):
        """
        Desc:
            #zero pass plot
        Input:
        Output:
        """
        self.plot_gdf(shapes = [self.Sim.zero_pass],
                      shape_colors = ['darkgray'],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "Zero Pass")
        
        return self.convert_to_png()
        
    def plot_c(self):
        """
        Desc:
            #one pass plot
        Input:
        Output:
        """
        self.plot_gdf(shapes = [self.Sim.single_pass],
                      shape_colors = ['limegreen'],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "Single Pass")
        
        return self.convert_to_png()

        
    def plot_d(self):
        """
        Desc:
        Input:
            #double pass plot
        Output:
        """
        self.plot_gdf(shapes = [self.Sim.double_pass],
                      shape_colors = ['orangered'],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "Double Pass")
        
        return self.convert_to_png()

    def plot_e(self):
        """
        Desc:
        Input:
            #track summary plot
        Output:
        """
        self.plot_gdf(shapes = [self.Sim.outer_gdf,
                                #self.Sim.inner_gdf, 
                                self.Sim.zero_pass,
                                self.Sim.single_pass,
                                self.Sim.double_pass],
                      shape_colors = ['orangered',
                                     #'red',
                                     'palegoldenrod',
                                     'limegreen',
                                     'darkgray'],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "Track Summary")
        
        return self.convert_to_png()

        
    #----------- JE below here-----------
    
    def plot_f(self):
        """
        Desc:
        Input:
            #jump labelling
        Output:
        """
        self.plot_gdf(shapes = [#self.Sim.outer_gdf,
                                #self.Sim.planned_track,
                                self.Sim.T_gdf_line],
                                #self.Sim.actual_path,
                                #self.Sim.planned_pt,
                                #self.Sim.actual_pt],
                      shape_colors = ['#915ebd'],
                                     #'red',
                                     #'blue',
                                     #'green',
                                     #'purple',
                                     #'pink'],
                      x_label = "Easting", 
                      y_label = "Northing", 
                      title = "Track Jump Summary")