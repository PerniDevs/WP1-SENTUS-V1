from InputOutput import readObsEpoch
from COMMON import GnssConstants as Const
from InputOutput import readConf
from InputOutput import processConf
from InputOutput import CSNEPOCHS, CSNPOINTS

ObsFile = "example/SENTUS-V1/SENTUS-V1/SCN/SCEN-SENTINEL6A-JAN24/INP/OBS/OBS_s6an_Y24D011.dat"
CfgFile = "example/SENTUS-V1/SENTUS-V1/SCN/SCEN-SENTINEL6A-JAN24/CFG/sentus.cfg"

# Read conf file
Conf = readConf(CfgFile)

# Process Configuration Parameters
Conf = processConf(Conf)

with open(ObsFile, 'r') as fobs:
    ObsInfo = readObsEpoch(fobs)


PrevPreproObsInfo = {}
for const in ['G', 'E']:
        for prn in range(1, Const.MAX_NUM_SATS_CONSTEL + 1):
            PrevPreproObsInfo["%s%02d" % (const,prn)] = {
                "PrevEpoch": 86400,                                          # Previous SoD

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

            } # End of SatPreproObsInfo

print(PrevPreproObsInfo["G01"])
