from errorFlagger import ErrorFlagger

class ErrorRecorder(ErrorFlagger):
    """
    Inherits the Error Recorder functionality
    Adds functionality to record errors
    """
    
    def __init__(self):
        """
        """
        ErrorFlagger.__init__(self)
        
    def record_errors(self):
        """
        Desc:
            Flags all of the errors in the desired order
        Input:
        Output:
        """
        #print("recording errors")
        #record drift | total drift (absolute value) | record cumulative drift
        self.record_drift()
        
        #record jump
        self.record_jump()
        
        #record error
        self.record_error()
                    
    def record_drift(self):
        """
        Desc:
            checks variables and records drifts for that epoch
        Input:
            self.drift
        Output:
        """
        #print("recording drift")
        #print(f"drift_status shape: {self.drift_status[self.i]}")
        #print(f"drift_status a: {self.drift_status[self.i]}")
        
        if self.drift:
            #then there was a drift error
            self.drift_status[self.i] = True
            
            self.drift_individual[self.i,0] = self.error_change.E()  #easting
            self.drift_individual[self.i,1] = self.error_change.N()  #northing
            
            self.drift_cumulative[self.i,0] = self.drift_cumulative[self.i-1, 0] + self.error_change.E()  #easting
            self.drift_cumulative[self.i,1] = self.drift_cumulative[self.i-1, 1] + self.error_change.N()  #northing
            
            self.drift_absolute_cumulative[self.i,0] = self.drift_absolute_cumulative[self.i-1, 0] + abs(self.error_change.E())  #easting
            self.drift_absolute_cumulative[self.i,1] = self.drift_absolute_cumulative[self.i-1, 1] + abs(self.error_change.N())  #northing
        else:
            #then there was no drift and cumulative values remain the same
            self.drift_status[self.i] = False
            
            self.drift_cumulative[self.i,0] = self.drift_cumulative[self.i-1, 0]
            self.drift_cumulative[self.i,1] = self.drift_cumulative[self.i-1, 1]
            
            self.drift_absolute_cumulative[self.i,0] = self.drift_absolute_cumulative[self.i-1, 0]
            self.drift_absolute_cumulative[self.i,1] = self.drift_absolute_cumulative[self.i-1, 1]
            
        #print(f"drift_status c: {self.drift_status[self.i]}")
            
    def record_jump(self):
        """
        Desc:
            checks for jump and records it
        Input:
            self.track_jump
        Output:
        """
        #print("recording jump")
        if self.track_jump:
            #then there was a jump error
            self.jump_status[self.i] = True
            
            self.jump_individual[self.i,0] = self.error_change.E()  #easting
            self.jump_individual[self.i,1] = self.error_change.N()  #northing
            
            self.jump_cumulative[self.i,0] = self.jump_cumulative[self.i-1, 0] + self.error_change.E()  #easting
            self.jump_cumulative[self.i,1] = self.jump_cumulative[self.i-1, 1] + self.error_change.N()  #northing
            
            self.jump_absolute_cumulative[self.i,0] = self.jump_absolute_cumulative[self.i-1, 0] + abs(self.error_change.E())  #easting
            self.jump_absolute_cumulative[self.i,1] = self.jump_absolute_cumulative[self.i-1, 1] + abs(self.error_change.N())  #northing
        else:
            #then there was not a jump error
            self.jump_status[self.i] = False
            
            self.jump_cumulative[self.i,0] = self.jump_cumulative[self.i-1, 0]  #easting
            self.jump_cumulative[self.i,1] = self.jump_cumulative[self.i-1, 1] #northing
            
            self.jump_absolute_cumulative[self.i,0] = self.jump_absolute_cumulative[self.i-1, 0]  #easting
            self.jump_absolute_cumulative[self.i,1] = self.jump_absolute_cumulative[self.i-1, 1]  #northing
            
    def record_error(self):
        """
        Desc:
            checks for an error and records it --> good for the cumulative stuff
        Input:
            self.track_jump
            self.drift
        Output:
        """
        #print("recording err")
        if self.track_jump or self.drift:
            #confirm that there was an error
            self.error_status[self.i] = True
        else:
            self.error_status[self.i] = False
            
        #add errors (doesn't matter if they're zero)
        self.error_individual[self.i,0] = self.jump_individual[self.i,0] + self.drift_individual[self.i,0] #easting
        self.error_individual[self.i,1] = self.jump_individual[self.i,1] + self.drift_individual[self.i,1]  #northing
        
        self.error_cumulative[self.i,0] = self.jump_cumulative[self.i,0] + self.drift_cumulative[self.i,0] #easting
        self.error_cumulative[self.i,1] = self.jump_cumulative[self.i,1] + self.drift_cumulative[self.i,1]  #northing
        
        self.error_cumulative[self.i,0] = self.jump_absolute_cumulative[self.i,0] + self.drift_absolute_cumulative[self.i,0] #easting
        self.error_cumulative[self.i,1] = self.jump_absolute_cumulative[self.i,1] + self.drift_absolute_cumulative[self.i,1]  #northing