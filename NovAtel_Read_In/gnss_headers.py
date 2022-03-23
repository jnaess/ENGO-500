class GNSS_Headers():
    """
    Contains the header information"""
    
    def __init__(self,  header = ["Log_name", "Port", "Sequence#", "% Idle Time", "Time_Status", "Week", "Seconds", "Receiver_Status", "Null", "Receiver_S/W_Version"],
                        rtk_cols = ["sol_sattus", "pos_type", "lat", "lon", "hgt", "undulation", 
                               "datum id#", "lat σ", "lon σ",  "hgt σ", "stn id", "diff_age", 
                               "sol_age", "#SVs", "#solnSVs", "#ggL1", "#solnMultiSVs", "Null", 
                               "ext sol stat", "Galileo and BeiDou sig mask", "GPS and GLONASS sig mask"],#, "xxxx", "[CR][LF]"]
                        ppp_cols = ["sol_sattus", "pos_type", "lat", "lon", "hgt", "undulation", "datum_id#", 
                               "lat_sigma", "lon_sigma",  "hgt_sigma", "stn_id", "diff_age", "sol_age", "#SVs", 
                               "#solnSVs", "#ggL1", "#solnMultiSVs", "Null", "ext sol stat", "Null", "GPS_and_GLONASS_sig_ mask"],#, "xxxx", "[CR][LF]"]
                        psr_cols = ["sol_sattus", "pos_type", "lat", "lon", "hgt", "undulation", "datum id#", "lat_sigma", 
                               "lon_sigma",  "hgt_sigma", "stn_id", "diff_age", "sol_age", "#SVs", "#solnSVs", "Null", 
                               "Null", "Null", "ext_sol_stat", "Galileo_and_BeiDou_sig_mask", "GPS_and_GLONASS_sig_mask"]):#, "xxxx", "[CR][LF]"]):
        """
        Desc:
            Sets up the object
        Input:
        Output:
        """
        self.header = header
        self.rtk_cols = rtk_cols
        self.ppp_cols = ppp_cols
        self.psr_cols = psr_cols