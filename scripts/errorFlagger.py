class ErrorFlagger():
    """
    Flags Errors
    """
    
    def __init__(self):
        """
        """
        return
    
    def flag_errors(self):
        """
        Desc:
            Flags all of the errors in the desired order
        Input:
        Output:
        """
        self.flag_jump()
                
        self.flag_blunder() #we don't yet do anything with this
        
        self.flag_drift()
        
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
    
    def flag_drift(self):
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
        if (self.error_change.E() != 0 or self.error_change.N() != 0) and not self.track_jump:
            #flag for drift
            self.drift = True
        else:
            #not a blunder
            self.drift = False
            