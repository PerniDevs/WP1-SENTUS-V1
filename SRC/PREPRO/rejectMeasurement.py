def rejectMeasurement(PreproObs, Criterion):
    
    if Criterion == "RCVR_MASK":
        PreproObs["RejectionCause"] = 1
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_DATA_GAP":
        PreproObs["RejectionCause"] = 2
        PreproObs["Valid"] = 1
    elif Criterion == "MIN_SNR_F1":
        PreproObs["RejectionCause"] = 3
        PreproObs["Valid"] = 1
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 4
        PreproObs["Valid"] = 1
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 5
        PreproObs["Valid"] = 1
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 6
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_PHASE_RATE_F1":
        PreproObs["RejectionCause"] = 7
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_PHASE_RATE_F2":
        PreproObs["RejectionCause"] = 8
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_PHASE_RATE_STEP_F1":
        PreproObs["RejectionCause"] = 9
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_PHASE_RATE_STEP_F2":
        PreproObs["RejectionCause"] = 10
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_RANGE_RATE_F1":
        PreproObs["RejectionCause"] = 11
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_RANGE_RATE_F2":
        PreproObs["RejectionCause"] = 12
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_RANGE_RATE_STEP_F1":
        PreproObs["RejectionCause"] = 13
        PreproObs["Valid"] = 1
    elif Criterion == "MAX_RANGE_RATE_STEP_F2":
        PreproObs["RejectionCause"] = 14

    return PreproObs