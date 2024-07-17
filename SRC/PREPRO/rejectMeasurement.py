def rejectMeasurement(PreproObs, Criterion):
    PreproObs["Valid"] = 1
    if Criterion == "RCVR_MASK":
        PreproObs["RejectionCause"] = 1
        
    elif Criterion == "MAX_DATA_GAP":
        PreproObs["RejectionCause"] = 2
        
    elif Criterion == "MIN_SNR_F1":
        PreproObs["RejectionCause"] = 3
        
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 4
        
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 5
        
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 6
        
    elif Criterion == "MAX_PHASE_RATE_F1":
        PreproObs["RejectionCause"] = 7
        
    elif Criterion == "MAX_PHASE_RATE_F2":
        PreproObs["RejectionCause"] = 8
        
    elif Criterion == "MAX_PHASE_RATE_STEP_F1":
        PreproObs["RejectionCause"] = 9
        
    elif Criterion == "MAX_PHASE_RATE_STEP_F2":
        PreproObs["RejectionCause"] = 10
        
    elif Criterion == "MAX_RANGE_RATE_F1":
        PreproObs["RejectionCause"] = 11
        
    elif Criterion == "MAX_RANGE_RATE_F2":
        PreproObs["RejectionCause"] = 12
        
    elif Criterion == "MAX_RANGE_RATE_STEP_F1":
        PreproObs["RejectionCause"] = 13
        
    elif Criterion == "MAX_RANGE_RATE_STEP_F2":
        PreproObs["RejectionCause"] = 14

    return PreproObs