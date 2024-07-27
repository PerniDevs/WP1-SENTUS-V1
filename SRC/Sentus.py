#!/usr/bin/env python

########################################################################
# Sentus.py:
# This is the Main Module of SENTUS tool
#
#  Project:        SENTUS
#  File:           Sentus.py
#
#   Author: GNSS Academy
#   Copyright 2024 GNSS Academy
#
# Usage:
#   Sentus.py $SCEN_PATH
########################################################################

import sys, os

# Update Path to reach COMMON
Common = os.path.dirname(
    os.path.abspath(sys.argv[0])) + '/COMMON'
sys.path.insert(0, Common)

# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
from collections import OrderedDict
from yaml import dump
from COMMON import GnssConstants as Const
from InputOutput import readConf
from InputOutput import processConf
from InputOutput import createOutputFile
from InputOutput import readObsEpoch
from InputOutput import generatePreproFile
from InputOutput import PreproHdr
from InputOutput import CSNEPOCHS, CSNPOINTS
from InputOutput import ObsIdxC, ObsIdxP
from Preprocessing import runPreprocessing
from PreprocessingPlots import generatePreproPlots
from COMMON.Dates import convertJulianDay2YearMonthDay
from COMMON.Dates import convertYearMonthDay2Doy

#----------------------------------------------------------------------
# INTERNAL FUNCTIONS
#----------------------------------------------------------------------

def displayUsage():
    sys.stderr.write("ERROR: Please provide path to SCENARIO as a unique argument\n")

#######################################################
# MAIN BODY
#######################################################

# Check InputOutput Arguments
if len(sys.argv) != 2:
    displayUsage()
    sys.exit()

# Extract the arguments
Scen = sys.argv[1]

# Select the Configuratiun file name
CfgFile = Scen + '/CFG/sentus.cfg'

# Read conf file
Conf = readConf(CfgFile)

# Process Configuration Parameters
Conf = processConf(Conf)

# Print header
print( '------------------------------------')
print( '--> RUNNING SENTUS:')
print( '------------------------------------')

# Loop over Julian Days in simulation
#-----------------------------------------------------------------------
for Jd in range(Conf["INI_DATE_JD"], Conf["END_DATE_JD"] + 1):
    # Compute Year, Month and Day in order to build input file name
    Year, Month, Day = convertJulianDay2YearMonthDay(Jd)

    # Compute the Day of Year (DoY)
    Doy = convertYearMonthDay2Doy(Year, Month, Day)

    # Display Message
    print( '\n*** Processing Day of Year: ' + str(Doy) + ' ... ***')

    # Define the full path and name to the OBS INFO file to read
    # ObsFile = Scen + \
    #     '/INP/OBS/' + "OBS_%s_Y%02dD%03d.dat" % \
    #         (Conf['SAT_ACRONYM'], Year % 100, Doy)
    ObsFile = Scen + \
        '/INP/OBS/' + "OBS_%s_Y%02dD%03d.dat.mod" % \
            (Conf['SAT_ACRONYM'], Year % 100, Doy)

    # Display Message
    print("INFO: Reading file: %s..." %
    ObsFile)


    # # If PREPRO outputs are requested
    # if Conf["PREPRO_OUT"] == 1:
    #     # Define the full path and name to the output PREPRO OBS file
    #     PreproObsFile = Scen + \
    #         '/OUT/PPVE/' + "PREPRO_OBS_%s_Y%02dD%03d.dat" % \
    #             (Conf['SAT_ACRONYM'], Year % 100, Doy)

    #     # Display Message
    #     print("INFO: Reading file: %s and generating PREPRO figures..." %
    #     PreproObsFile)

    #     # Generate Preprocessing plots
    #     generatePreproPlots(PreproObsFile)

    # sys.exit()

    # If Preprocessing outputs are activated
    if Conf["PREPRO_OUT"] == 1:
        # Define the full path and name to the output PREPRO OBS file
        PreproObsFile = Scen + \
            '/OUT/PPVE/' + "PREPRO_OBS_%s_Y%02dD%03d.dat" % \
                (Conf['SAT_ACRONYM'], Year % 100, Doy)

        # Create output file
        fpreprobs = createOutputFile(PreproObsFile, PreproHdr)


    # Initialize Variables
    EndOfFile = False
    ObsInfo = [None]
    PrevPreproObsInfo = {}
    for const in ['G', 'E']:
        for prn in range(1, Const.MAX_NUM_SATS_CONSTEL + 1):
            PrevPreproObsInfo["%s%02d" % (const,prn)] = {
                "PrevEpoch": 86400,                                          # Previous SoD

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
                # CYCLE_SLIPS  1  0.5  3  7  2
                "GF_L_Prev": [0.0] * int(Conf["CYCLE_SLIPS"][CSNPOINTS]),      # Array with previous GF carrier phase observables
                "GF_Epoch_Prev": [0.0] * int(Conf["CYCLE_SLIPS"][CSNPOINTS]),  # Array with previous epochs
                "CycleSlipFlags": [0.0] * int(Conf["CYCLE_SLIPS"][CSNEPOCHS]), # Array with last cycle slips flags
                "CycleSlipDetectFlag": 0,                                      # Flag indicating if a cycle slip has been detected

            } # End of SatPreproObsInfo

    # Open OBS file
    with open(ObsFile, 'r') as fobs:

        # LOOP over all Epochs of OBS file
        # ----------------------------------------------------------
        while not EndOfFile:

            # If ObsInfo is not empty
            if ObsInfo != []:

                # Read Only One Epoch
                ObsInfo = readObsEpoch(fobs)

                # If ObsInfo is empty, exit loop
                if ObsInfo == []:
                    break

                # Preprocess OBS measurements
                # ----------------------------------------------------------
                PreproObsInfo = runPreprocessing(Conf, ObsInfo, PrevPreproObsInfo)

                # If PREPRO outputs are requested
                if Conf["PREPRO_OUT"] == 1:
                    # Generate output file
                    generatePreproFile(fpreprobs, PreproObsInfo)
                # break

    # If PREPRO outputs are requested
    if Conf["PREPRO_OUT"] == 1:
        # Close PREPRO output file
        fpreprobs.close()

        # Display Message
        print("INFO: Reading file: %s and generating PREPRO figures..." %
        PreproObsFile)

        # Generate Preprocessing plots
        generatePreproPlots(PreproObsFile)

# End of JD loop

print( '\n------------------------------------')
print( '--> END OF SENTUS ANALYSIS')
print( '------------------------------------')

#######################################################
# End of Sentus.py
#######################################################
