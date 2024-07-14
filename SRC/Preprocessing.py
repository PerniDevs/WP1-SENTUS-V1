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

            # if PrevPreproObsInfo["CycleSlipBuffIdx"]== Conf.CYCLE_SLIPS[3]:
            
            # Compute Geometry-Free in cycles
            # The geometry free is the difference between Phase1 and Phase2 measurements
            # GF = 0
            
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
        SatPreproObsInfo["L2"] = float(SatCodesObs[ObsIdxP["L2"]])
        # Get L1-meters
        SatPreproObsInfo["L1Meters"] = float(SatCodesObs[ObsIdxP["L1"]]) * Wave["F1"]
        # Get L2-meters
        SatPreproObsInfo["L2Meters"] = float(SatCodesObs[ObsIdxP["L2"]]) * Wave["F2"]
        # Get Valid
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
        DeltaT = PreproObs["Sod"] - PrevPreproObsInfo[SatLabel]["PrevEpoch"]
        if DeltaT > Conf["MAX_DATA_GAP"][1]:
            DeltaT = 0
            if Conf["MAX_DATA_GAP"][0] == 1:
                PreproObs = rejectMeasurement(PreproObs, "MAX_DATA_GAP")
                # Update the dictionaries
                PreproObsInfo[SatLabel] = PreproObs
            PrevPreproObsInfo[SatLabel] = resetPrevPreproObsInfo(Conf)
        else:
            # Update the PrevPreproObsInfo with the current data
            # Get Sod
            PrevPreproObsInfo[SatLabel]["PrevEpoch"] = PreproObs["Sod"]
            # Get L1
            PrevPreproObsInfo[SatLabel]["PrevL1"] = PreproObs["L1"]
            # Get L2
            PrevPreproObsInfo[SatLabel]["PrevL2"] = PreproObs["L2"]
            # Get C1
            PrevPreproObsInfo[SatLabel]["PrevC1"] = PreproObs["C1"]
            # Get C2
            PrevPreproObsInfo[SatLabel]["PrevC2"] = PreproObs["C2"]


        # Check Satellite Elevation Angle in front of the minimum by configuration
        #--------------------------------------------------------------------
        if PreproObs["Elevation"] > Conf["MASK_ANGLE"]:
            PreproObs = rejectMeasurement(PreproObs, "MASK_ANGLE")
            # Update the dictionaries
            PreproObsInfo[SatLabel] = PreproObs
        #End if PreproObs["Elevation"] > Conf["MASK_ANGLE"]


        # Measurement quality monitoring
        #--------------------------------------------------------------------
        # Check signal to noise ratio in front of minimum by configuration (if activated)
        #--------------------------------------------------------------------
        if Const["MIN_SNR"][0] == 1:
            if PreproObs["S1"] < Conf["MIN_SNR"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MIN_SNR_F1")
                # Update the dictionaries
                PreproObsInfo[SatLabel] = PreproObs
            elif PreproObs["S2"] < Conf["MIN_SNR"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MIN_SNR_F2")
                # Update the dictionaries
                PreproObsInfo[SatLabel] = PreproObs
            # End if PreproObs["S1"] > Conf["MIN_SNR"][1] || PreproObs["S2"] > Conf["MIN_SNR"][1]
        # End if Const["MIN_SNR"][0] == 1:


        # Check Pseudo-Ranges out of range in front of maximum by configuration
        #--------------------------------------------------------------------
        if Conf["MAX_PSR_OUTRNG"][0] == 1:
            if PreproObs["C1"] > Conf["MAX_PSR_OUTRNG"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_PSR_OUTRNG_F1")
                # Update the dictionaries
                PreproObsInfo[SatLabel] = PreproObs
            elif PreproObs["C2"] > Conf["MAX_PSR_OUTRNG"][1]:
                PreproObs = rejectMeasurement(PreproObs, "MAX_PSR_OUTRNG_F2")
                # Update the dictionaries
                PreproObsInfo[SatLabel] = PreproObs
            # End if PreproObs["C1"] > Conf["MAX_PSR_OUTRNG"][1] || PreproObs["C2"] > Conf["MAX_PSR_OUTRNG"][1]
        # End if Conf["MAX_PSR_OUTRNG"][0] == 1


        # Build Measurement Combinations of Code and Phases
        #--------------------------------------------------------------------
        PreproObs = buildIonoFree(PreproObs, GammaF1F2)
        PreproObsInfo[SatLabel] = PreproObs
        

        #Perform the Code Carrier Smoothing with a Hatch Filter of 100 seconds
        #--------------------------------------------------------------------
        if DeltaT < 0:
            DeltaT = 0

        PrevPreproObsInfo[SatLabel]["Ksmooth"] = PrevPreproObsInfo[SatLabel]["Ksmooth"] + DeltaT
        SmoothingTime = PrevPreproObsInfo[SatLabel]["Ksmooth"]

        if PrevPreproObsInfo[SatLabel]["Ksmooth"] >= Conf["HATCH_TIME"]:
            SmoothingTime = Conf["HATCH_TIME"]
        # End if PrevPreproObsInfo[SatLabel]["Ksmooth"] >= Conf["HATCH_TIME"]

        # TODO: QUESTIONS for tutorship
        # TODO: if DeltaT needs to be updated in lines 325 and 263
        # TODO: about how to caluclate HF
        # CALL HATCH FILTER
        # if (n2 > 1)
        # Pionofree_smoothed = (1/n2)*Pionofree + ((n2-1)/n2)*(Pionofree_smoothed_1 + Lionofree-Lionofree_1)

        if (SmoothingTime > 0):
            Alpha = DeltaT / SmoothingTime
            PreproObs["SmoothIF"] = Alpha + PreproObs["IF_C"] + (1 - Alpha) * (PrevPreproObsInfo[SatLabel]["PrevSmooth"] + (PreproObs["IF_P"] - PrevPreproObsInfo[SatLabel]["IF_P_Prev"]))
            # Update the dictionaries
            PrevPreproObsInfo[SatLabel]["PrevSmooth"] = PreproObs["SmoothIF"]
            PrevPreproObsInfo[SatLabel]["IF_P_Prev"] = PreproObs["IF_P"]
            PreproObsInfo[SatLabel] = PreproObs
        else:
            # Update dictionaries
            PrevPreproObsInfo[SatLabel]["PrevSmooth"] =  PreproObs["IF_C"]
            PrevPreproObsInfo[SatLabel]["IF_P_Prev"] = PreproObs["IF_P"]
            PreproObsInfo[SatLabel] = PreproObs
        # End if (SmoothingTime > 0)

        # Check Phase Rate (if activated)
        #--------------------------------------------------------------------


    # End of for SatLabel, PreproObs in PreproObsInfo.items():

    return PreproObsInfo

# End of function runPreprocessing()

########################################################################
# END OF PREPROCESSING FUNCTIONS MODULE
########################################################################
