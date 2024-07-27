from COMMON import GnssConstants as Const
from InputOutput import CSNEPOCHS, CSNPOINTS

def resetPrevPreproObsInfo(Conf, PreproObs):
    return {
                "PrevEpoch": PreproObs["Sod"],                               # Previous SoD

                "PrevElev": [Const.NAN] * 2,                                 # Previous two elevations

                "ResetHatchFilter": 1,                                       # Flag to reset Hatch filter
                "Ksmooth": 0,                                                # Hatch filter K
                "PrevSmooth": 0,                                             # Previous Smooth Observable
                "IF_P_Prev": 0,                                              # Previous IF of the phases
                
                "PrevL1": Const.NAN,                                         # Previous L1
                "PrevPhaseRateL1": Const.NAN,                                # Previous Phase Rate
                "PrevC1": Const.NAN,                                         # Previous C1
                "PrevRangeRateL1": Const.NAN,                                # Previous Code Rate
                
                "PrevL2": Const.NAN,                                         # Previous L1
                "PrevPhaseRateL2": Const.NAN,                                # Previous Phase Rate
                "PrevC2": Const.NAN,                                         # Previous C2
                "PrevRangeRateL2": Const.NAN,                                # Previous Code Rate

                "CycleSlipBuffIdx": 0,                                         # Index of CS buffer
                "CycleSlipFlagIdx": 0,                                         # Index of CS flag array
                "GF_L_Prev": [0.0] * int(Conf["CYCLE_SLIPS"][CSNPOINTS]),      # Array with previous GF carrier phase observables
                "GF_Epoch_Prev": [0.0] * int(Conf["CYCLE_SLIPS"][CSNPOINTS]),  # Array with previous epochs
                "CycleSlipFlags": [0.0] * int(Conf["CYCLE_SLIPS"][CSNEPOCHS]), # Array with last cycle slips flags
                "CycleSlipDetectFlag": 0,                                      # Flag indicating if a cycle slip has been detected

            } 