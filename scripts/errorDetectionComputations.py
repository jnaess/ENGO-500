class ErrorDetectionComputations():
    """
    Encapsulates many of the error Dectactor opperations
    """
    
    def __init__(self):
        """
        """
        return
        
    
    def compute_errors(self):
        """
        Desc:
            Checks for and computes errors
        Input:
            self.prev
            self.curr
        Output:
            self.track_jump
            self.blunder
        """
        self.flag_jump()
                
        self.flag_blunder()
                    
        #record easting drift
                
        #record northing drift
                
        #record total drift (absolute value)
                
        #record cumulative drift
            
    def flag_jump(self):
        """
        Desc:
            Flags for a jump error
        Input:
            self.prev, Ellipse()
            self.curr, Coord() or Ellipse()
        Output:
            self.track_jump T/F
        """
        #flag for jump
        if self.prev.in_error_ellipse(self.curr, 3):
            #not a track jump
            self.track_jump = False
        else:
            #flag for potential track jump
            self.track_jump = True
            
    def flag_blunder(self):
        """
        Desc:
            Flags for a blunder
        Input:
            self.curr_True, Ellipse()
            self.curr, Coord() or Ellipse()
        Output:
            self.blunder T/F
        """
        #flag for blunder
        if self.curr_True.in_error_ellipse(self.curr, 3):
            #not a blunder
            self.blunder = False
        else:
            #flag for blunder
            self.blunder = True