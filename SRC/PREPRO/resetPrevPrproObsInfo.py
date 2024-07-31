from COMMON import GnssConstants as Const
from InputOutput import CSNEPOCHS, CSNPOINTS

def resetPrevPreproObsInfo(Conf, PreproObs, PrevPreproObsInfo, SatLabel, condition):
    
    # access to PhaseObs or CodeObs Prev data and modify it
    if condition == 0:
        # Update PhaseObs relevant data
        PrevPreproObsInfo[SatLabel]["CycleSlipBuffIdx"] = 0
        PrevPreproObsInfo[SatLabel]["CycleSlipFlagIdx"] = 0
        PrevPreproObsInfo[SatLabel]["GF_L_Prev"] = [0.0] * int(Conf["CYCLE_SLIPS"][CSNPOINTS])
        PrevPreproObsInfo[SatLabel]["GF_Epoch_Prev"] = [0.0] * int(Conf["CYCLE_SLIPS"][CSNPOINTS])
        PrevPreproObsInfo[SatLabel]["CycleSlipFlags"] = [0.0] * int(Conf["CYCLE_SLIPS"][CSNEPOCHS])

        return PrevPreproObsInfo[SatLabel]

    elif condition == 1:
        # Update CodeObs relevant data
        PrevPreproObsInfo[SatLabel]["PrevEpoch"] = PreproObs["Sod"]

        PrevPreproObsInfo[SatLabel]["PrevElev"] = [Const.NAN] * 2

        PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
        PrevPreproObsInfo[SatLabel]["Ksmooth"] = 0
        PrevPreproObsInfo[SatLabel]["PrevSmooth"] = 0
        PrevPreproObsInfo[SatLabel]["IF_P_Prev"] = 0

        PrevPreproObsInfo[SatLabel]["PrevL1"] = Const.NAN
        PrevPreproObsInfo[SatLabel]["PrevPhaseRateL1"] = Const.NAN
        PrevPreproObsInfo[SatLabel]["PrevC1"] = Const.NAN
        PrevPreproObsInfo[SatLabel]["PrevRangeRateL1"] = Const.NAN

        PrevPreproObsInfo[SatLabel]["PrevL2"] = Const.NAN
        PrevPreproObsInfo[SatLabel]["PrevPhaseRateL2"] = Const.NAN
        PrevPreproObsInfo[SatLabel]["PrevC2"] = Const.NAN
        PrevPreproObsInfo[SatLabel]["PrevRangeRateL2"] = Const.NAN

        return PrevPreproObsInfo[SatLabel]