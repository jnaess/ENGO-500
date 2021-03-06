import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import pandas as pd
import geopandas as gpd
import base64
import io


class BasePlot():
    """
    Contains Plotter parameters and plot generation functions
    """
    
    def __init__(self, display = False):
        """
        Desc:
        Input:
        Output:
        """
        self.display = display

    def plot_fig(self, x= [], y = [], line_label = [], x_label="x_label", y_label="y_label", title="title", aspect = True, anchor = 1.2, alpha = 1, linewidth = 1, color = False):
        """
        Desc:
        Input:
            x, [[x1s], ... ,[x2s]]
            y, [[y1s], ... [y2s]]
            line_label, ["line1", ... , "line 2"]
            shapes, False or [GeoDataFrame, ... , GeoDataFrame]
            shape_colors, ["#49e37c", ... , "#bd7b5e"]
        Output:
        """
        fig, ax = plt.subplots()
        
        # Colour outside axes
        fig.patch.set_facecolor('xkcd:light grey')

        self.set_parameters(ax, x_label, y_label, title, aspect = aspect)

        for i in range(len(x)):
            if not color:
                ax.plot(x[i],y[i], label = line_label[i], alpha = alpha, linewidth = linewidth)
            else:
                ax.plot(x[i],y[i], label = line_label[i], alpha = alpha, linewidth = linewidth, color = color[i])
        
        
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        
        # Set plot limits
        #plt.xlim(0, 12)
        #plt.ylim(0, 12)
        
        self.set_legend(anchor)
        
        if self.display:
            plt.show() 
    
    def plot_pts(self, x= [], y = [], line_label = [], x_label="x_label", y_label="y_label", title="title", aspect = True, anchor = 1.2, alpha = 1, linewidth = 1, color = False):
        """
        Desc:
        Input:
            x, [[x1s], ... ,[x2s]]
            y, [[y1s], ... [y2s]]
            line_label, ["line1", ... , "line 2"]
            shapes, False or [GeoDataFrame, ... , GeoDataFrame]
            shape_colors, ["#49e37c", ... , "#bd7b5e"]
        Output:
        """
        fig, ax = plt.subplots()
        
        # Colour outside axes
        fig.patch.set_facecolor('xkcd:light grey')

        self.set_parameters(ax, x_label, y_label, title, aspect = aspect)

        for i in range(len(x)):
            if not color:
                ax.scatter(x[i],y[i], label = line_label[i], alpha = alpha)     
                ax.plot(x[i],np.zeros(len(x[i])))
        
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        
        # Set plot limits
        #plt.xlim(0, 12)
        #plt.ylim(0, 12)
        
        self.set_legend(anchor)
        
        if self.display:
            plt.show() 
        
    def plot_gdf(self, shapes = [], shape_colors = [], x_label="x_label", y_label="y_label", title="title", aspect = True):
        """
        Desc:
        Input:
            x, [[x1s], ... ,[x2s]]
            y, [[y1s], ... [y2s]]
            line_label, ["line1", ... , "line 2"]
            shapes, False or [GeoDataFrame, ... , GeoDataFrame]
            shape_colors, ["#49e37c", ... , "#bd7b5e"]
        Output:
        """
        if len(shapes) != len(shape_colors):
            print("color and shape lists are not equal in length")
            return
            
        fig, ax = plt.subplots(figsize = (8,8))

        # Colour outside axes
        fig.patch.set_facecolor('xkcd:light grey')

        self.set_parameters(ax, x_label, y_label, title, aspect = aspect)

        #this one to be appended to
        gdf = pd.concat( shapes, ignore_index=True)
        color_dict = {}
        
        #setup the color dictionary
        for i in range(len(shapes)):
            #map out the colors
            #print(shapes[i])
            color_dict[shapes[i]['title'].to_list()[0]] = shape_colors[i]
            
                
        #plot everything)    
        gdf.plot(ax=ax, 
                column = "title", 
                legend=True, 
                cmap=colors.ListedColormap(list(color_dict.values())),
                legend_kwds={'bbox_to_anchor': (1.23, 1)})
        
        # Set limits
        #plt.xlim(0, 12)
        #plt.ylim(0, 12)
        
        if self.display:
            plt.show()    
        
    def set_parameters(self, ax, x_label="x_label", y_label="y_label", title="title", aspect = True):
        """
        Desc:
            sets the titles for the axis
        Input:
        Output:
        """
        if aspect:
            ax.set_aspect('equal')
        
        # Adding labels
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)
        ax.set_title(title)
        
        # Colour within axes
        ax.set_facecolor("white")
        
        # Axis colours
        ax.spines['bottom'].set_color('black')
        ax.spines['top'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.spines['left'].set_color('black')
        
    def set_legend(self, anchor):
        """
        Desc:
            sets up the legend info
        Input:
        Output:
        """
        legend = plt.legend(frameon = 1, loc = 1, bbox_to_anchor = (anchor, 1))
        frame = legend.get_frame()
        frame.set_facecolor('white')
        frame.set_edgecolor('white')
        frame.set_linewidth(0)