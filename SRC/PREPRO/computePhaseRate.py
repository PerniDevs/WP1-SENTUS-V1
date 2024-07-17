import COMMON.GnssConstants as Const

def computePhaseRate(PreProObs, PrevPreproObsInfo, SatLabel):
    
    # Check inconsistencies 0/0 
    if PrevPreproObsInfo[SatLabel]["PrevL1"] == Const.NAN and PrevPreproObsInfo[SatLabel]["PrevL2"] == Const.NAN:
        phaseRate_f1 = Const.NAN
        phaseRate_f2 = Const.NAN
    else:
        phaseRate_f1 = (PreProObs["L1Meters"] - PrevPreproObsInfo[SatLabel]["PrevL1"]) / (PreProObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
        phaseRate_f2 = (PreProObs["L2Meters"] - PrevPreproObsInfo[SatLabel]["PrevL2"]) / (PreProObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
    
    # Update dictionaries
    PreProObs["PhaseRateL1"] = phaseRate_f1
    PreProObs["PhaseRateL2"] = phaseRate_f2

    # Return updated dictionaries
    return PreProObs

def computePhaseRateStep(PreProObs, PrevPreproObsInfo, SatLabel):
    # Check inconsistencies 0/0 
    if PrevPreproObsInfo[SatLabel]["PrevPhaseRateL1"] == Const.NAN and PrevPreproObsInfo[SatLabel]["PrevPhaseRateL2"] == Const.NAN:
        phaseRateStep_f1 = Const.NAN
        phaseRateStep_f2 = Const.NAN
    else:
        phaseRateStep_f1 = (PreProObs["PhaseRateL1"] - PrevPreproObsInfo[SatLabel]["PrevPhaseRateL1"]) / (PreProObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
        phaseRateStep_f2 = (PreProObs["PhaseRateL2"] - PrevPreproObsInfo[SatLabel]["PrevPhaseRateL2"]) / (PreProObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
    
    # Update dictionaries
    PreProObs["PhaseRateStepL1"] = phaseRateStep_f1
    PreProObs["PhaseRateStepL2"] = phaseRateStep_f2

    # Return updated dictionaries
    return PreProObs