import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from plotter import Plotter
from errorDetectorAnalyzer import ErrorDetectorAnalyzer
from simulationAnalyzer import SimulationAnalyzer

class Analyzer(Plotter, ErrorDetectorAnalyzer, SimulationAnalyzer):
    """
    Developes the analysis for auto reporting
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        Plotter.__init__(self)
        ErrorDetectorAnalyzer.__init__(self)
        SimulationAnalyzer.__init__(self)
        
        
    def generate_analytics(self):
        """
        Desc:
            Generated all variables with values for the auto reporting
        Input:
        Output:
        """
        self.generate_simulation_report()
        
        self.generate_error_detection_report()