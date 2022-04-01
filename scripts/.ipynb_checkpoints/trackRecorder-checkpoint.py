import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

class TrackRecorder():
    """
    Records and outputs the simulated path's track
    Sister class to PassGenerator
    """
    
    def __init__(self, out_file = "Output_Tracks.csv"):
        """
        Desc:
        Output:
            self.es, ErrorSimulator()
        Input:
        """
        self.out_file = out_file
    
    def output_tracks(self):
        """
        Desc:
            Creates a csv of the tracks
        Input:
        Output:
        """
        self.prep_tracks()
        
        self.es.generate_keys()
        
        self.true_keys.update(self.real_keys)
        self.true_keys.update(self.es.jump_keys)
        self.true_keys.update(self.es.drift_keys)
        self.true_keys.update(self.es.error_keys)
        
        #for key in self.true_keys:
            #print(f"{key}: {len(self.true_keys[key])}")
                  
        self.output_tracks = pd.DataFrame(self.true_keys)
        
        self.output_tracks.to_csv(self.out_file)
        
    def dataframe_true_track(self):
        """
        Desc:
            Converts the true track to a dataframe
        Input:
        Output:
        """
        self.prep_true_track()
        
        self.true_track_df = pd.DataFrame(self.true_keys)
    
    def prep_tracks(self):
        """
        Desc:
            prepares the true and real track info
        Input:
        Output:
        """
        self.record_true_track()
        
        self.generate_true_keys()
        
        self.record_real_track()
        
        self.generate_real_keys()
        
    def record_true_track(self):
        """
        Desc:
            E, N, E_std, N_std of true track
        Input:
            self.true_passes
        Output:
        """
        self.T_Easting = []
        self.T_Northing = []
        self.T_E_std = []
        self.T_N_std = []
        
        for path in self.true_passes:
            #print(path.segments)
            for segment in path.segments:
                a,b,c,d = segment.out_all()
                self.T_Easting.append(a)
                self.T_Northing.append(b)
                self.T_E_std.append(c)
                self.T_N_std.append(d)
                
    def generate_true_keys(self):
        """
        Desc:
            key for creating the truth track dataframe
        Input:
        Output:
            self.true_keys
        """
        self.true_keys = {
            'True_E' : self.T_Easting,
            'True_N' : self.T_Northing,
            'True_E_std' : self.T_E_std,
            'True_N_std' : self.T_N_std}
        
    def record_real_track(self):
        """
        Desc:
            E, N, E_std, N_std of real track
        Input:
            self.true_passes
        Output:
        """
        self.R_Easting = []
        self.R_Northing = []
        self.R_E_std = []
        self.R_N_std = []
        
        for path in self.real_passes:
            #print(f'{path.segments}')

            for segment in path.segments:
                a,b,c,d = segment.out_all()
                self.R_Easting.append(a)
                self.R_Northing.append(b)
                self.R_E_std.append(c)
                self.R_N_std.append(d)
                
    def generate_real_keys(self):
        """
        Desc:
            key for creating the real track dataframe
        Input:
        Output:
            self.true_keys
        """
        self.real_keys = {
            'Real_E' : self.R_Easting,
            'Real_N' : self.R_Northing,
            'Real_E_std' : self.R_E_std,
            'Real_N_std' : self.R_N_std}