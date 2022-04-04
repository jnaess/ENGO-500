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
        
    def plot_g(self):
        """
        Desc:
            #cumulative dift comparison easting
            #true drift versus detected drift
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.drift_cumulative_e.to_list(),
                           self.df_ED.drift_cumulative_e.to_list()], 
                      line_label = ["Simulated \nCumulative \nEasting Drift", 
                                    "Detected \nCumulative \nEasting Drift"],
                      x_label = "Epoch", 
                      y_label = "Cumulative Drift (m)", 
                      title = "Simulated vs. Detected Cumulating Easting Drift",
                     aspect = False,
                     anchor = 1.25)
        
        return self.convert_to_png()
    
    def plot_h(self):
        """
        Desc:
            #cumulative dift comparison northing
            #true drift versus detected drift
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.drift_cumulative_n.to_list(),
                           self.df_ED.drift_cumulative_n.to_list()], 
                      line_label = ["Simulated \nCumulative \nNorthing Drift", 
                                    "Detected \nCumulative \nNorthing Drift"],
                      x_label = "Epoch", 
                      y_label = "Cumulative Drift (m)", 
                      title = "Simulated vs. Detected Cumulating Northing Drift",
                     aspect = False,
                     anchor = 1.25)
        
        return self.convert_to_png()
    
    def plot_i(self):
        """
        Desc:
            #individual dift comparison easting
            #true drift versus detected drift
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.drift_individual_e.to_list(),
                           self.df_ED.drift_individual_e.to_list()], 
                      line_label = ["Simulated \nIndividual \nEasting Drifts", 
                                    "Detected \nIndividual \nEasting Drifts"],
                      x_label = "Epoch", 
                      y_label = "Drift (m)", 
                      title = "Simulated vs. Detected Individual Easting Drifts",
                     aspect = False,
                     anchor = 1.25,
                        alpha = .8)
        
        return self.convert_to_png()
    
    def plot_j(self):
        """
        Desc:
            #individual dift comparison easting
            #true drift versus detected drift
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.drift_individual_n.to_list(),
                           self.df_ED.drift_individual_n.to_list()], 
                      line_label = ["Simulated \nIndividual \nNorthing Drifts", 
                                    "Detected \nIndividual \nNorthing Drifts"],
                      x_label = "Epoch", 
                      y_label = "Drift (m)", 
                      title = "Simulated vs. Detected Individual Northing Drifts",
                     aspect = False,
                     anchor = 1.25,
                        alpha = .8)
        
        return self.convert_to_png()
    
    def plot_k(self):
        """
        Desc:
            #cumulative dift comparison easting
            #true drift versus detected drift
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.jump_cumulative_e.to_list(),
                           self.df_ED.jump_cumulative_e.to_list()], 
                      line_label = ["Simulated \nCumulative \nEasting Jumps", 
                                    "Detected \nCumulative \nEasting Jumps"],
                      x_label = "Epoch", 
                      y_label = "Cumulative Jump (m)", 
                      title = "Simulated vs. Detected Cumulating Easting Jumps",
                     aspect = False,
                     anchor = 1.3)
        
        return self.convert_to_png()
    
    def plot_l(self):
        """
        Desc:
            #cumulative jump comparison northing
            #true jump versus detected drift
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.jump_cumulative_n.to_list(),
                           self.df_ED.jump_cumulative_n.to_list()], 
                      line_label = ["Simulated \nCumulative \nNorthing Jumps", 
                                    "Detected \nCumulative \nNorthing Jumps"],
                      x_label = "Epoch", 
                      y_label = "Cumulative Jump (m)", 
                      title = "Simulated vs. Detected Cumulating Northing Jumps",
                     aspect = False,
                     anchor = 1.3)
        
        return self.convert_to_png()
    
    def plot_m(self):
        """
        Desc:
            #individual jump comparison easting
            #true jump versus detected jumps
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.jump_individual_e.to_list(),
                           self.df_ED.jump_individual_e.to_list()], 
                      line_label = ["Simulated \nIndividual \nEasting Jumps", 
                                    "Detected \nIndividual \nEasting Jumps"],
                      x_label = "Epoch", 
                      y_label = "Jumps (m)",
                      title = "Simulated vs. Detected Individual Easting Jumps",
                     aspect = False,
                     anchor = 1.3,
                        alpha = .8)
        
        return self.convert_to_png()
    
    def plot_n(self):
        """
        Desc:
            #individualjump comparison easting
            #true drift versus detected jump
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.jump_individual_n.to_list(),
                           self.df_ED.jump_individual_n.to_list()], 
                      line_label = ["Simulated \nIndividual \nNorthing Jumps", 
                                    "Detected \nIndividual \nNorthing Jumps"],
                      x_label = "Epoch", 
                      y_label = "Jumps (m)", 
                      title = "Simulated vs. Detected Individual Northing Jumps",
                     aspect = False,
                     anchor = 1.3,
                        alpha = .8)
        
        return self.convert_to_png()
    
    def plot_o(self):
        """
        Desc:
            #individual jump comparison easting
            #true jump versus detected jumps
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.error_cumulative_e.to_list(),
                           self.df_ED.error_cumulative_e.to_list()], 
                      line_label = ["Simulated \nCumulative \nEasting Errors", 
                                    "Detected \nCumulative \nEasting Errors"],
                      x_label = "Epoch", 
                      y_label = "Errors (m)",
                      title = "Simulated vs. Detected Cumulative Easting Errors",
                     aspect = False,
                     anchor = 1.3,
                        alpha = .8)
        
        return self.convert_to_png()
    
    def plot_p(self):
        """
        Desc:
            #individualjump comparison easting
            #true drift versus detected jump
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.error_cumulative_n.to_list(),
                           self.df_ED.error_cumulative_n.to_list()], 
                      line_label = ["Simulated \nCumulative \nNorthing Errors", 
                                    "Detected \nCumulative \nNorthing Errors"],
                      x_label = "Epoch", 
                      y_label = "Errors (m)", 
                      title = "Simulated vs. Detected Cumulative Northing Errors",
                     aspect = False,
                     anchor = 1.3,
                        alpha = .8)
        
        return self.convert_to_png()
    
    def plot_q(self):
        """
        Desc:
            #individual jump comparison easting
            #true jump versus detected jumps
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.error_individual_e.to_list(),
                           self.df_ED.error_individual_e.to_list()], 
                      line_label = ["Simulated \nIndividual \nEasting Errors", 
                                    "Detected \nIndividual \nEasting Errors"],
                      x_label = "Epoch", 
                      y_label = "Errors (m)",
                      title = "Simulated vs. Detected Individual Easting Errors",
                     aspect = False,
                     anchor = 1.3,
                        alpha = .8)
        
        return self.convert_to_png()
    
    def plot_r(self):
        """
        Desc:
            #individualjump comparison easting
            #true drift versus detected jump
        Input:
        Output:
        """
        self.plot_fig(x = [self.df_sim.index.to_list(),
                           self.df_ED.index.to_list()],
                      y = [self.df_sim.error_individual_n.to_list(),
                           self.df_ED.error_individual_n.to_list()], 
                      line_label = ["Simulated \nIndividual \nNorthing Errors", 
                                    "Detected \nIndividual \nNorthing Errors"],
                      x_label = "Epoch", 
                      y_label = "Errors (m)", 
                      title = "Simulated vs. Detected Individual Northing Errors",
                     aspect = False,
                     anchor = 1.3,
                        alpha = .8)
        
        return self.convert_to_png()