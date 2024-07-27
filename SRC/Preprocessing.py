#!/usr/bin/env python

########################################################################
# Preprocessing.py:
# This is the Preprocessing Module of SENTUS tool
#
#  Project:        SENTUS
#  File:           Preprocessing.py
#
#   Author: GNSS Academy
#   Copyright 2024 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
########################################################################


# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
# Add path to find all modules
Common = os.path.dirname(os.path.dirname(
    os.path.abspath(sys.argv[0]))) + '/COMMON'
sys.path.insert(0, Common)
from collections import OrderedDict
from COMMON import GnssConstants as Const
from InputOutput import ObsIdxC, ObsIdxP, REJECTION_CAUSE
from InputOutput import FLAG, VALUE, TH, CSNEPOCHS, CSNPOINTS, CSPDEGREE
import numpy as np

from PREPRO.resetPrevPrproObsInfo import resetPrevPreproObsInfo
from PREPRO.rejectMeasurement import rejectMeasurement
from PREPRO.buildIonoFree import buildIonoFree
from PREPRO.computePhaseRate import computePhaseRate, computePhaseRateStep
from PREPRO.computeCodeRate import computeCodeRate, computeCodeRateStep


# Preprocessing internal functions
#-----------------------------------------------------------------------

def runPreprocessing(Conf, ObsInfo, PrevPreproObsInfo):
    
    # Purpose: preprocess GNSS raw measurements from OBS file
    #          and generate PREPRO OBS file with the cleaned,
    #          smoothed measurements

    #          More in detail, this function handles:
             
    #          * Measurements cleaning and validation and exclusion due to different 
    #          criteria as follows:
    #             - Minimum Masking angle
    #             - Maximum Number of channels
    #             - Minimum Carrier-To-Noise Ratio (CN0)
    #             - Pseudo-Range Output of Range 
    #             - Maximum Pseudo-Range Step
    #             - Maximum Pseudo-Range Rate
    #             - Maximum Carrier Phase Increase
    #             - Maximum Carrier Phase Increase Rate
    #             - Data Gaps checks and handling 
    #             - Cycle Slips detection

    #         * Filtering/Smoothing of Code-Phase Measurements with a Hatch filter 

    # Parameters
    # ==========
    # Conf: dict
    #         Configuration dictionary
    # ObsInfo: list
    #         OBS info for current epoch
    # PrevPreproObsInfo: dict
    #         Preprocessed observations for previous epoch per sat
    #         PrevPreproObsInfo["G01"]["C1"]

    # Returns
    # =======
    # PreproObsInfo: dict
    #         Preprocessed observations for current epoch per sat
    #         PreproObsInfo["G01"]["C1"]
    
    # Get Observations
    CodesObs = ObsInfo[0]
    PhaseObs = ObsInfo[1]

    # CHALLENGE:
    # if check Cycle Slips activated
    if (Conf["CYCLE_SLIPS"][FLAG] == 1):

        # Loop over Phase measurements
        for iObs, SatPhaseObs in enumerate(PhaseObs):
            # Get SOD
            Sod = float(SatPhaseObs[ObsIdxP["SOD"]])

            # Get satellite label
            SatLabel = SatPhaseObs[ObsIdxP["PRN"]]
            
            
            # Compute Geometry-Free in cycles
            # The geometry free is the difference between Phase1 and Phase2 measurements
            # GF = PrevPreproObsInfo[SatLabel]["GF_L_Prev"] - 

            if PrevPreproObsInfo[SatLabel]["CycleSlipBuffIdx"] == Conf["CYCLE_SLIPS"][3]:
                pass
            
            # Check Data Gaps
            # ...

            # Cycle slips detection
            # fit a polynomial using previous GF measurements to compare the predicted value
            # with the observed one
            # --------------------------------------------------------------------------------------------------------------------
            # ...
            

        # end of for iObs, SatPhaseObs in enumerate(PhaseObs):

    # End of if (Conf["CYCLE_SLIPS"][FLAG] == 1)

    # Initialize output
    PreproObsInfo = OrderedDict({})

    # Loop over Code measurements
    for iObs, SatCodesObs in enumerate(CodesObs):

        # Get satellite label
        SatLabel = SatCodesObs[ObsIdxC["PRN"]]

        # Get constellation
        Constel = SatLabel[0]
        
        Wave = {}
        # Get wavelengths
        if Constel == 'G':

            # L1 wavelength
            Wave["F1"] = Const.GPS_L1_WAVE

            # L2 wavelength
            Wave["F2"] = Const.GPS_L2_WAVE

            # Gamma GPS
            GammaF1F2 = Const.GPS_GAMMA_L1L2

        elif Constel == 'E':

            # E1 wavelength
            Wave["F1"] = Const.GAL_E1_WAVE

            # E5a wavelength
            Wave["F2"] = Const.GAL_E5A_WAVE

            # Gamma Galileo
            GammaF1F2 = Const.GAL_GAMMA_E1E5A

        # Get Phases
        SatPhaseObs = PhaseObs[iObs]

        while SatPhaseObs[ObsIdxP["PRN"]] != SatLabel:
            PhaseObs.pop(iObs)
            SatPhaseObs = PhaseObs[iObs]

        assert(SatLabel == SatPhaseObs[ObsIdxP["PRN"]])

        # Initialize output info
        SatPreproObsInfo = {
            "Sod": 0.0,                   # Second of day
            
            "Elevation": 0.0,             # Elevation
            "Azimuth": 0.0,               # Azimuth
            
            "C1": 0.0,                    # GPS L1C/A pseudorange
            "C2": 0.0,                    # GPS L1P pseudorange
            "L1": 0.0,                    # GPS L1 carrier phase (in cycles)
            "L1Meters": 0.0,              # GPS L1 carrier phase (in m)
            "S1": 0.0,                    # GPS L1C/A C/No
            "L2": 0.0,                    # GPS L2 carrier phase (in cycles)
            "L2Meters": 0.0,              # GPS L2 carrier phase  (in m)
            "S2": 0.0,                    # GPS L2 C/No
            
            "GeomFree_P": Const.NAN,      # Geometry-free of Phases
            "IF_C": Const.NAN,            # Iono-free of Codes
            "IF_P": Const.NAN,            # Iono-free of Phases
            "SmoothIF": Const.NAN,        # Smoothed Iono-free of Codes 
            
            "Valid": 1,                   # Measurement Status
            "RejectionCause": 0,          # Cause of rejection flag
            "Status": 0,                  # Smoothing status
            
            "RangeRateL1": Const.NAN,     # L1 Code Rate
            "RangeRateStepL1": Const.NAN, # L1 Code Rate Step
            "PhaseRateL1": Const.NAN,     # L1 Phase Rate
            "PhaseRateStepL1": Const.NAN, # L1 Phase Rate Step
            
            "RangeRateL2": Const.NAN,     # L2 Code Rate
            "RangeRateStepL2": Const.NAN, # L2 Code Rate Step
            "PhaseRateL2": Const.NAN,     # L2 Phase Rate
            "PhaseRateStepL2": Const.NAN, # L2 Phase Rate Step
        } # End of SatPreproObsInfo

        # Prepare outputs
        # Get SoD
        SatPreproObsInfo["Sod"] = float(SatCodesObs[ObsIdxC["SOD"]])
        # Get Elevation
        SatPreproObsInfo["Elevation"] = float(SatCodesObs[ObsIdxC["ELEV"]])
        # Get Azimuth
        SatPreproObsInfo["Azimuth"] = float(SatCodesObs[ObsIdxC["AZIM"]])
        # Get C1
        SatPreproObsInfo["C1"] = float(SatCodesObs[ObsIdxC["C1"]])
        # Get C2
        SatPreproObsInfo["C2"] = float(SatCodesObs[ObsIdxC["C2"]])
        # Get S1
        SatPreproObsInfo["S1"] = float(SatCodesObs[ObsIdxC["S1"]])
        # Get S2
        SatPreproObsInfo["S2"] = float(SatCodesObs[ObsIdxC["S2"]])
        # Get L1
        SatPreproObsInfo["L1"] = float(SatPhaseObs[ObsIdxP["L1"]]) 
        # Get L2
        SatPreproObsInfo["L2"] = float(SatPhaseObs[ObsIdxP["L2"]])
        # Get L1-meters
        SatPreproObsInfo["L1Meters"] = SatPreproObsInfo["L1"] * Wave["F1"]
        # Get L2-meters
        SatPreproObsInfo["L2Meters"] = SatPreproObsInfo["L2"] * Wave["F2"]
        # Get Valid
        if SatPreproObsInfo["Sod"] == 0:
            SatPreproObsInfo["Valid"] = 0

        # Prepare output for the satellite
        PreproObsInfo[SatLabel] = SatPreproObsInfo
    
    # Loop over satellites
    for SatLabel, PreproObs in PreproObsInfo.items():

        # Get constellation
        Constel = SatLabel[0]
        Wave = {}
        # Get wavelengths
        if Constel == 'G':

            # L1 wavelength
            Wave["F1"] = Const.GPS_L1_WAVE

            # L1 wavelength
            Wave["F2"] = Const.GPS_L2_WAVE

            # Gamma
            GammaF1F2 = Const.GPS_GAMMA_L1L2

        elif Constel == 'E':

            # L1 wavelength
            Wave["F1"] = Const.GAL_E1_WAVE

            # L1 wavelength
            Wave["F2"] = Const.GAL_E5A_WAVE

            # Gamma
            GammaF1F2 = Const.GAL_GAMMA_E1E5A
        # End of if if Constel == 'G':


        # Check measurements data gaps
        #--------------------------------------------------------------------
        # TODO: Periodo de no visibilidad si DeltaT es mayor a 1000 rejection cause sigue igual, o viceversa
        # verificar con la elevacion con las epocas anteriores  
        if PreproObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"] > Conf["MAX_DATA_GAP"][1]:
            if Conf["MAX_DATA_GAP"][0] == 1 and (PreproObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"]) < 1000:
                PreproObs = rejectMeasurement(PreproObs, "MAX_DATA_GAP")
                PrevPreproObsInfo[SatLabel]["PrevElev"][0] = PrevPreproObsInfo[SatLabel]["PrevElev"][1]
                PrevPreproObsInfo[SatLabel]["PrevElev"][1] = PreproObs["Elevation"]
            PrevPreproObsInfo[SatLabel] = resetPrevPreproObsInfo(Conf, PreproObs)
        
        # if PreproObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"] > Conf["MAX_DATA_GAP"][1]:
        #     if Conf["MAX_DATA_GAP"][0] == 1 and (PrevPreproObsInfo[SatLabel]["PrevElev"][0] != Const.NAN) and (PrevPreproObsInfo[SatLabel]["PrevElev"][1] != Const.NAN):
        #         PreproObs = rejectMeasurement(PreproObs, "MAX_DATA_GAP")
        #         PrevPreproObsInfo[SatLabel]["PrevElev"][0] = PrevPreproObsInfo[SatLabel]["PrevElev"][1]
        #         PrevPreproObsInfo[SatLabel]["PrevElev"][1] = PreproObs["Elevation"]
        #     PrevPreproObsInfo[SatLabel] = resetPrevPreproObsInfo(Conf, PreproObs)


        # Check Satellite Elevation Angle in front of the minimum by configuration
        #--------------------------------------------------------------------
        if PreproObs["Elevation"] < Conf["RCVR_MASK"]:
            PreproObs = rejectMeasurement(PreproObs, "RCVR_MASK")
        #End if PreproObs["Elevation"] > Conf["RCVR_MASK"]


        # Measurement quality monitoring
        #--------------------------------------------------------------------
        # Check signal to noise ratio in front of minimum by configuration (if activated)
        #--------------------------------------------------------------------
        if Conf["MIN_SNR"][0] == 1:
            if PreproObs["S1"] < Conf["MIN_SNR"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MIN_SNR_F1")
            elif PreproObs["S2"] < Conf["MIN_SNR"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MIN_SNR_F2")
            # End if PreproObs["S1"] > Conf["MIN_SNR"][1] || PreproObs["S2"] > Conf["MIN_SNR"][1]
        # End if Const["MIN_SNR"][0] == 1:


        # Check Pseudo-Ranges out of range in front of maximum by configuration
        #--------------------------------------------------------------------
        if Conf["MAX_PSR_OUTRNG"][0] == 1:
            if PreproObs["C1"] > Conf["MAX_PSR_OUTRNG"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_PSR_OUTRNG_F1")
            elif PreproObs["C2"] > Conf["MAX_PSR_OUTRNG"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_PSR_OUTRNG_F2")
            # End if PreproObs["C1"] > Conf["MAX_PSR_OUTRNG"][1] || PreproObs["C2"] > Conf["MAX_PSR_OUTRNG"][1]
        # End if Conf["MAX_PSR_OUTRNG"][0] == 1


        # Build Measurement Combinations of Code and Phases
        #--------------------------------------------------------------------
        PreproObs = buildIonoFree(PreproObs, GammaF1F2)


        #Perform the Code Carrier Smoothing with a Hatch Filter of 100 seconds
        #--------------------------------------------------------------------
        if PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] == 1:

            # Set Ksmooth and Reset Hatch filter
            PrevPreproObsInfo[SatLabel]["Ksmooth"] = 1
            PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 0

            # Update the Prev and Prepro dicts
            PreproObs["SmoothIF"] = PreproObs["IF_C"]
            PrevPreproObsInfo[SatLabel]["PrevSmooth"] = PreproObs["SmoothIF"]
            PrevPreproObsInfo[SatLabel]["IF_P_Prev"] = PreproObs["IF_P"] 

        else:
            # Calculate Smoothing time
            SmoothingTime = PrevPreproObsInfo[SatLabel]["Ksmooth"] + (PreproObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])

            # Set smooth time with a time window of 100s
            if PrevPreproObsInfo[SatLabel]["Ksmooth"] >= Conf["HATCH_TIME"]:
                SmoothingTime = Conf["HATCH_TIME"]
            # End if PrevPreproObsInfo[SatLabel]["Ksmooth"] >= Conf["HATCH_TIME"]
        
            # CALL HATCH FILTER
            Alpha = (PreproObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"]) / SmoothingTime
            PreproObs["SmoothIF"] = Alpha * PreproObs["IF_C"] + (1 - Alpha) * (PrevPreproObsInfo[SatLabel]["PrevSmooth"] + (PreproObs["IF_P"] - PrevPreproObsInfo[SatLabel]["IF_P_Prev"]))
            
            PrevPreproObsInfo[SatLabel]["Ksmooth"] = PrevPreproObsInfo[SatLabel]["Ksmooth"] + (PreproObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"])
            PrevPreproObsInfo[SatLabel]["PrevSmooth"] = PreproObs["SmoothIF"]
            PrevPreproObsInfo[SatLabel]["IF_P_Prev"] = PreproObs["IF_P"]
        # End if PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] == 1


        # Check Phase Rate (if activated)
        #--------------------------------------------------------------------
        PreproObs = computePhaseRate(PreproObs, PrevPreproObsInfo, SatLabel)

        if Conf["MAX_PHASE_RATE"][0] == 1 and PreproObs["PhaseRateL1"] != Const.NAN:
            if  abs(PreproObs["PhaseRateL1"]) > Conf["MAX_PHASE_RATE"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_PHASE_RATE_F1")
                # Reset the hatch filter 
                PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
            if  abs(PreproObs["PhaseRateL2"]) > Conf["MAX_PHASE_RATE"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_PHASE_RATE_F2")
                # Reset the hatch filter 
                PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
            # End if PreproObs["PhaseRateL1"] > Conf["MAX_PHASE_RATE"][1] || PreproObs["PhaseRateL2"] > Conf["MAX_PHASE_RATE"][1]
        # End if Conf["MAX_PHASE_RATE"][0] == 1


        # Check Phase Rate Step (if activated)
        #--------------------------------------------------------------------
        PreproObs = computePhaseRateStep(PreproObs, PrevPreproObsInfo, SatLabel)

        if Conf["MAX_PHASE_RATE_STEP"][0] == 1 and PreproObs["PhaseRateStepL1"] != Const.NAN:
            if  abs(PreproObs["PhaseRateStepL1"]) > Conf["MAX_PHASE_RATE_STEP"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_PHASE_RATE_STEP_F1")
                # Reset the hatch filter 
                PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
            if  abs(PreproObs["PhaseRateStepL2"]) > Conf["MAX_PHASE_RATE_STEP"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_PHASE_RATE_STEP_F2")
                # Reset the hatch filter 
                PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
            # End if  PreproObs["PhaseRateStepL1"] > Conf["MAX_PHASE_RATE_STEP"][1] || PreproObs["PhaseRateStepL2"] > Conf["MAX_PHASE_RATE_STEP"][1]
        # End if Conf["MAX_PHASE_RATE_STEP"][0]


        # Check Code Rate detector (if activated)
        #--------------------------------------------------------------------
        # Compute the Code Rate in m/s as the first derivative of the raw codes
        PreproObs = computeCodeRate(PreproObs, PrevPreproObsInfo, SatLabel)
        if Conf["MAX_CODE_RATE"][0] == 1 and PreproObs["RangeRateL1"] != Const.NAN:
            if abs(PreproObs["RangeRateL1"]) > Conf["MAX_CODE_RATE"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_RANGE_RATE_F1")
                # Reset the hatch filter 
                PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
            if abs(PreproObs["RangeRateL2"]) > Conf["MAX_CODE_RATE"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_RANGE_RATE_F2")
                # Reset the hatch filter 
                PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
            # End if PreproObs["RangeRateL1"] > Conf["MAX_CODE_RATE"][1] || PreproObs["RangeRateL2"] > Conf["MAX_CODE_RATE"][1]
        # End if Conf["MAX_CODE_RATE"][0] == 1


        # Check Code Rate Step Detector (if activated)
        #--------------------------------------------------------------------
        # Compute Code Rate Step in m/s2 as the second derivative of Raw Codes
        PreproObs = computeCodeRateStep(PreproObs, PrevPreproObsInfo, SatLabel)

        if Conf["MAX_CODE_RATE_STEP"][0] == 1 and PreproObs["RangeRateStepL1"] != Const.NAN:
            if abs(PreproObs["RangeRateStepL1"]) > Conf["MAX_CODE_RATE_STEP"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_RANGE_RATE_STEP_F1")
                # Reset the hatch filter 
                PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
            if abs(PreproObs["RangeRateStepL2"]) > Conf["MAX_CODE_RATE_STEP"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_RANGE_RATE_STEP_F2")
                # Reset the hatch filter 
                PrevPreproObsInfo[SatLabel]["ResetHatchFilter"] = 1
            # End if PreproObs["RangeRateStepL1"] > Conf["MAX_CODE_RATE_STEP"][1] || PreproObs["RangeRateStepL2"] > Conf["MAX_CODE_RATE_STEP"][1]
        # End if Conf["MAX_CODE_RATE_STEP"][0] == 1


        # Update Smoothing status if it is superior to 100s
        # print(PrevPreproObsInfo[SatLabel]["Ksmooth"])
        if (PrevPreproObsInfo[SatLabel]["Ksmooth"] >= (Conf["HATCH_STATE_F"]*Conf["HATCH_TIME"])) and PreproObs["Valid"] == 1:
            PreproObs["Status"] = 1
        else:
            PreproObs["Status"] = 0

        # Update Previous values
        PrevPreproObsInfo[SatLabel]["PrevEpoch"] = PreproObs["Sod"]

        PrevPreproObsInfo[SatLabel]["Status"] = PreproObs["Status"]
        
        PrevPreproObsInfo[SatLabel]["PrevL1"] = PreproObs["L1Meters"]
        PrevPreproObsInfo[SatLabel]["PrevPhaseRateL1"] = PreproObs["PhaseRateL1"]
        PrevPreproObsInfo[SatLabel]["PrevC1"] = PreproObs["C1"]
        PrevPreproObsInfo[SatLabel]["PrevRangeRateL1"] = PreproObs["RangeRateL1"]
        
        PrevPreproObsInfo[SatLabel]["PrevL2"] = PreproObs["L2Meters"]
        PrevPreproObsInfo[SatLabel]["PrevPhaseRateL2"] = PreproObs["PhaseRateL2"]
        PrevPreproObsInfo[SatLabel]["PrevC2"] = PreproObs["C2"]
        PrevPreproObsInfo[SatLabel]["PrevRangeRateL2"] = PreproObs["RangeRateL2"]

        # Update Proprocessed information
        PreproObsInfo[SatLabel] = PreproObs

        
    # End of for SatLabel, PreproObs in PreproObsInfo.items():

    return PreproObsInfo

# End of function runPreprocessing()

########################################################################
# END OF PREPROCESSING FUNCTIONS MODULE
########################################################################
