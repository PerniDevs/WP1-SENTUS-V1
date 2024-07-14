def rejectMeasurement(PreproObs, Criterion):
    PreproObs["Valid"] = 1
    if Criterion == "MASK_ANGLE":
        PreproObs["RejectionCause"] = 1
        return PreproObs 
    if Criterion == "MAX_DATA_GAP":
        PreproObs["RejectionCause"] = 2
        return PreproObs 
    elif Criterion == "MIN_SNR_F1":
        PreproObs["RejectionCause"] = 3
        return PreproObs 
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 4
        return PreproObs 
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 5
        return PreproObs 
    elif Criterion == "MIN_SNR_F2":
        PreproObs["RejectionCause"] = 6
        return PreproObs 