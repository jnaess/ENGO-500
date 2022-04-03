import matplotlib.pyplot as plt
import numpy as np

class BasePlot():
    """
    Contains Plotter parameters and plot generation functions
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """

    def plot_fig(self, x= [], y = [], line_label = [], x_label="x_label", y_label="y_label", title="title", shapes = False, shape_colors = [], shape_labels = []):
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

        fig.patch.set_facecolor('xkcd:mint green')

        self.set_parameters(ax, x_label, y_label, title)

        for i in range(len(x)):
            ax.plot(x[i],y[i], label = line_label[i])

        if shapes:
            for i in range(len(shapes)):
                shapes[i].plot(ax=ax, color = shape_colors[i], column = shape_labels[i], legend=True)
        
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        

        self.set_legend()
        
        plt.show()    
        
    def set_parameters(self, ax, x_label="x_label", y_label="y_label", title="title"):
        """
        Desc:
            sets the titles for the axis
        Input:
        Output:
        """
        ax.set_aspect('equal')
        
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)
        ax.set_title(title)

        ax.set_facecolor("yellow")
        
    def set_legend(self):
        """
        Desc:
            sets up the legend info
        Input:
        Output:
        """
        legend = plt.legend(frameon = 1, loc = 1)
        frame = legend.get_frame()
        frame.set_facecolor('purple')
        frame.set_edgecolor('white')
        frame.set_linewidth(0)