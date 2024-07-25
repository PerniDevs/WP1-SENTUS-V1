import COMMON.GnssConstants as Const

def computeCodeRate(PreProObs, PrevPreproObsInfo, SatLabel):
    # Check inconsistencies 0/0 
    if PrevPreproObsInfo[SatLabel]["PrevC1"] == Const.NAN and PrevPreproObsInfo[SatLabel]["PrevC2"] == Const.NAN:
        rangeRate_f1 = Const.NAN
        rangeRate_f2 = Const.NAN
    else:
        rangeRate_f1 = (PreProObs["C1"] - PrevPreproObsInfo[SatLabel]["PrevC1"]) / (PreProObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
        rangeRate_f2 = (PreProObs["C2"] - PrevPreproObsInfo[SatLabel]["PrevC2"]) / (PreProObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
    
    # Update dictionaries
    PreProObs["RangeRateL1"] = rangeRate_f1
    PreProObs["RangeRateL2"] = rangeRate_f2

    # Return updated dictionaries
    return PreProObs

def computeCodeRateStep(PreProObs, PrevPreproObsInfo, SatLabel):
    # Check inconsistencies 0/0 
    if PrevPreproObsInfo[SatLabel]["PrevRangeRateL1"] == Const.NAN and PrevPreproObsInfo[SatLabel]["PrevRangeRateL2"] == Const.NAN:
        rangeRateStep_f1 = Const.NAN
        rangeRateStep_f2 = Const.NAN
    else:
        rangeRateStep_f1 = (PreProObs["RangeRateL1"] - PrevPreproObsInfo[SatLabel]["PrevRangeRateL1"]) / (PreProObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
        rangeRateStep_f2 = (PreProObs["RangeRateL2"] - PrevPreproObsInfo[SatLabel]["PrevRangeRateL2"]) / (PreProObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
    
    # Update dictionaries
    PreProObs["RangeRateStepL1"] = rangeRateStep_f1
    PreProObs["RangeRateStepL2"] = rangeRateStep_f2

    # Return updated dictionaries
    return PreProObs