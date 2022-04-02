import psycopg2
from sqlalchemy import create_engine
import pandas as pd

from queryManager import QueryManager

class DatabaseManager(QueryManager):
    """
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Ouput:
        """
        QueryManager.__init__(self)
        
        self.initialize_key_values()
        
    def initialize_key_values(self):
        """
        Desc:
            sets up the login into for the database
        Input
        Output:
        """
        #connect to server and send data
        self.server = 'ec2-52-3-60-53.compute-1.amazonaws.com' 
        self.database = 'd3kr6lkene46qr' 
        self.username = 'mnonspcirnraqg' 
        self.password = '7919dd02f614cb83509e2889ec281800889dec45fb24c57db99d632e678f5626' 
        self.engine = create_engine(f'postgresql+psycopg2://{self.username}:{self.password}@{self.server}/{self.database}')
        