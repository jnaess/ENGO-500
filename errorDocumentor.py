from errorOutputter import ErrorOutputter

class ErrorDocumentor(ErrorOutputter):
    """
    Inherits the Error Recorder functionality
    Adds functionality to record errors
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        ErrorOutputter.__init__(self)
        
        self.drift_status= [False] #T/F
        self.drift_individual = [[0],[0]] #[E,N]
        self.drift_cumulative = [[0],[0]] #[E,N]
        self.drift_absolute_cumulative = [[0],[0]]#[E,N]
        
        self.jump_status = [False]
        self.jump_individual = [[0],[0]]#[E,N]
        self.jump_cumulative = [[0],[0]]#[E,N]
        self.jump_absolute_cumulative = [[0],[0]]#[E,N]
                    
        #add errors (doesn't matter if they're zero)
        self.error_status = [False]
        self.error_individual = [[0],[0]]#[E,N]
        self.error_cumulative = [[0],[0]]#[E,N]
        self.error_absolute_cumulative = [[0],[0]]#[E,N]
        
            
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
            self.drift_on
        Output:
        """

        self.drift_status.append(self.drift_on) 
        
        self.drift_individual[0].append(self.drift_e)  #[e,n]  
        self.drift_individual[1].append(self.drift_n)  #[e,n]  
        
        self.drift_cumulative[0].append(self.drift_cumulative[0][-1]+self.drift_e)
        self.drift_cumulative[1].append(self.drift_cumulative[1][-1]+self.drift_n)
        
        self.drift_absolute_cumulative[0].append(self.drift_absolute_cumulative[0][-1]+abs(self.drift_e))
        self.drift_absolute_cumulative[1].append(self.drift_absolute_cumulative[1][-1]+abs(self.drift_n))

            
    def record_jump(self):
        """
        Desc:
            checks for jump and records it
        Input:
            self.jump_happened
            self.jump_e
            self.jump_n
        Output:
        """
        
        self.jump_status.append(self.jump_happened) #T/F
        
        self.jump_individual[0].append(self.jump_e)  #[e,n] 
        self.jump_individual[1].append(self.jump_n)  #[e,n] 
        
        self.jump_cumulative[0].append(self.jump_cumulative[0][-1]+self.jump_e)
        self.jump_cumulative[1].append(self.jump_cumulative[1][-1]+self.jump_n)
        
        self.jump_absolute_cumulative[0].append(self.jump_absolute_cumulative[0][-1]+abs(self.jump_e))
        self.jump_absolute_cumulative[1].append(self.jump_absolute_cumulative[1][-1]+abs(self.jump_n))
        
            
    def record_error(self):
        """
        Desc:
            checks for an error and records it --> good for the cumulative stuff
        Input:
            self.jump_happened
            self.drift_on
        Output:
        """
        #print("recording err")
        if self.jump_happened or self.drift_on:
            #confirm that there was an error
            self.error_status.append(True)
        else:
            self.error_status.append(False)
        
        #add errors (doesn't matter if they're zero)
        self.error_individual[0].append(self.jump_individual[0][-1] + self.drift_individual[0][-1]) #easting
        self.error_individual[1].append(self.jump_individual[1][-1] + self.drift_individual[-1][-1])  #northing
        
        self.error_cumulative[0].append(self.jump_cumulative[0][-1] + self.drift_cumulative[0][-1]) #easting
        self.error_cumulative[1].append(self.jump_cumulative[1][-1] + self.drift_cumulative[-1][-1])  #northing
        
        self.error_absolute_cumulative[0].append(self.jump_absolute_cumulative[0][-1] + self.drift_absolute_cumulative[0][-1]) #easting
        self.error_absolute_cumulative[1].append(self.jump_absolute_cumulative[1][-1] + self.drift_absolute_cumulative[1][-1])  #northing