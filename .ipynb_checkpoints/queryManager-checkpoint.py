import psycopg2
from sqlalchemy import create_engine
import pandas as pd

class QueryManager():
    """
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
    
    def select_all(self, con, table = "simulations"):
        """
        Desc:
            selects all rows from a column
        Input:
        Output:
        """
        return pd.read_sql_query(f'''SELECT * FROM {table} ''', con)
    
    def simulations_all(self, con, table = "simulations"):
        """
        Desc:
            querry to reteive all rows from the simulations table
        Input:
            con, connection to database
            table, table name to retrieve from
        Output:
        """
        return pd.read_sql_query(f'''SELECT
                        jump_status,
                        jump_individual_e,
                        jump_individual_n,
                        jump_cumulative_e,
                        jump_cumulative_n,
                        jump_absolute_cumulative_e,
                        jump_absolute_cumulative_n,
                        sim_id,
                        epoch
                        FROM {table} ''', con)
    
    def jump_all(self, table = "error_detector_jumps"):
        """
        Desc:
        Input:
        Output
        """
        return f'''SELECT
                        jump_status,
                        jump_individual_e,
                        jump_individual_n,
                        jump_cumulative_e,
                        jump_cumulative_n,
                        jump_absolute_cumulative_e,
                        jump_absolute_cumulative_n,
                        sim_id,
                        epoch
                        FROM {table} '''
    
    def drift_all(self, table = "error_detector_drifts"):
        """
        Desc:
        Input:
        Output
        """
        return f'''SELECT
                        drift_status,
                        drift_individual_e,
                        drift_individual_n,
                        drift_cumulative_e,
                        drift_cumulative_n,
                        drift_absolute_cumulative_e,
                        drift_absolute_cumulative_n,
                        sim_id,
                        epoch
                        FROM {table} '''
    
    def error_all(self, table = "error_detector_jumps"):
        """
        Desc:
        Input:
        Output
        """
        return f'''SELECT
                        error_status,
                        error_individual_e,
                        error_individual_n,
                        error_cumulative_e,
                        error_cumulative_n,
                        error_absolute_cumulative_e,
                        error_absolute_cumulative_n,
                        sim_id,
                        epoch
                        FROM {table} '''