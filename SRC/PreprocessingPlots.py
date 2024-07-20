#!/usr/bin/env python

########################################################################
# PreprocessingPlots.py:
# This is the PreprocessingPlots Module of SENTUS tool
#
#  Project:        SENTUS
#  File:           PreprocessingPlots.py
#
#   Author: GNSS Academy
#   Copyright 2024 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
########################################################################

import sys, os
from pandas import unique
from pandas import read_csv
from InputOutput import PreproIdx
from InputOutput import REJECTION_CAUSE_DESC
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from COMMON import GnssConstants
import numpy as np
from collections import OrderedDict
from COMMON.missingPRNs import findMissingPRNs
from COMMON.Plots import generatePlot


def initPlot(PreproObsFile, PlotConf, Title, Label):
    PreproObsFileName = os.path.basename(PreproObsFile)
    PreproObsFileNameSplit = PreproObsFileName.split('_')
    Rcvr = PreproObsFileNameSplit[2]
    DatepDat = PreproObsFileNameSplit[3]
    Date = DatepDat.split('.')[0]
    Year = Date[1:3]
    Doy = Date[4:]

    PlotConf["xLabel"] = "Hour of Day %s" % Doy

    PlotConf["Title"] = "%s from %s on Year %s"\
        " DoY %s" % (Title, Rcvr, Year, Doy)

    PlotConf["Path"] = sys.argv[1] + '/OUT/PPVE/figures/' + \
        '%s_%s_Y%sD%s.png' % (Label, Rcvr, Year, Doy)


# Function to convert 'G01', 'G02', etc. to 1, 2, etc.
def convert_satlabel_to_prn(value):
    return int(value[1:])


# Function to convert 'G01', 'G02', etc. to 'G'
def convert_satlabel_to_const(value):
    return value[0]


# Plot Satellite Visibility
def plotSatVisibility(PreproObsFile, PreproObsData):
    PlotConf = {}


# Plot Number of Satellites
def plotNumSats(PreproObsFile, PreproObsData):
    PlotConf = {}


# Plot Code IF - Code IF Smoothed
def plotIFIFSmoothed(PreproObsFile, PreproObsData):
    print("Ploting Satellites Visibilities ... \n")

    missing_prns = findMissingPRNs(sorted(unique(df[LOS_IDX["PRN"]])))

    PlotConf = {}
    
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Satellite Visibility from s6an on Year 24 DoY 011"
    
    PlotConf["yTicks"] = sorted(np.concatenate((sorted(unique(df[LOS_IDX["PRN"]])), missing_prns)))
    PlotConf["yTicksLabels"] = sorted(np.concatenate((sorted(unique(df[LOS_IDX["PRN"]])), missing_prns)))
    PlotConf["yLim"] = [0, max(unique(df[LOS_IDX["PRN"]])) + 1]

    PlotConf["xLabel"] = "Hour of DoY 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '|'
    PlotConf["LineWidth"] = 15

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    for prn in sorted(unique(df[LOS_IDX["PRN"]])):
        Label = "G" + ("%02d" % prn)
        FilterCond = df[LOS_IDX["PRN"]] == prn
        PlotConf["xData"][Label] = df[LOS_IDX["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = df[LOS_IDX["PRN"]][FilterCond]
        PlotConf["zData"][Label] = df[LOS_IDX["ELEV"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/PPVE/SAT/' + 'SAT_VISIBILITY_SENTINEL6A_D011Y24.png'


# Plot C/N0
def plotCN0(PreproObsFile, PreproObsData, PlotTitle, PlotLabel):
    PlotConf = {}


# Plot Rejection Flags
def plotRejectionFlags(PreproObsFile, PreproObsData):
    PlotConf = {}


# Plot Rates
def plotRates(PreproObsFile, PreproObsData, PlotTitle, PlotLabel):
    PlotConf = {}


def generatePreproPlots(PreproObsFile):
    
    # Purpose: generate output plots regarding Preprocessing results

    # Parameters
    # ==========
    # PreproObsFile: str
    #         Path to PREPRO OBS output file

    # Returns
    # =======
    # Nothing


    # Satellite Visibility
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["PRN"],PreproIdx["STATUS"],PreproIdx["ELEV"]])
    
    print('INFO: Plot Satellite Visibility Periods ...')

    # Configure plot and call plot generation function
    plotSatVisibility(PreproObsFile, PreproObsData)


    # Number of satellites
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["PRN"],PreproIdx["STATUS"]])
    
    print('INFO: Plot Number of Satellites ...')

    # Configure plot and call plot generation function
    plotNumSats(PreproObsFile, PreproObsData)


    # Code IF - Code IF Smoothed
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["REJECT"],PreproIdx["STATUS"],PreproIdx["ELEV"],\
    PreproIdx["PRN"],PreproIdx["CODE_IF"],PreproIdx["SMOOTH_IF"]])
    
    print('INFO: Plot Code IF - Code IF Smoothed ...')

    # Configure plot and call plot generation function
    plotIFIFSmoothed(PreproObsFile, PreproObsData)


    # C/N0
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["S1"],PreproIdx["S2"],\
        PreproIdx["ELEV"], PreproIdx["PRN"]])
    
    print('INFO: Plot C/N0...')

    # Configure plot and call plot generation function
    plotCN0(PreproObsFile, PreproObsData, 'CN0_F1', 'S1')

    # Configure plot and call plot generation function
    plotCN0(PreproObsFile, PreproObsData, 'CN0_F2', 'S2')


    # Rejection Flags
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["PRN"],PreproIdx["REJECT"]])
    
    print('INFO: Plot Rejection Flags ...')

    # Configure plot and call plot generation function
    plotRejectionFlags(PreproObsFile, PreproObsData)


    # Code Rate
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["VALID"],PreproIdx["CODE_RATE"],\
        PreproIdx["ELEV"], PreproIdx["PRN"]])
    
    print('INFO: Plot Code Rate ...')

    # Configure plot and call plot generation function
    plotRates(PreproObsFile, PreproObsData, 'Code Rate', 'CODE_RATE')


    # Phase Rate
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["VALID"],PreproIdx["PHASE_RATE"],\
        PreproIdx["ELEV"], PreproIdx["PRN"]])

    print('INFO: Plot Phase Rate ...')

    # Configure plot and call plot generation function
    plotRates(PreproObsFile, PreproObsData, 'Phase Rate', 'PHASE_RATE')
    

    # Code Rate Step
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["VALID"],PreproIdx["CODE_RATE_STEP"],\
        PreproIdx["ELEV"], PreproIdx["PRN"]])
    
    print('INFO: Plot Code Rate Step...')

    # Configure plot and call plot generation function
    plotRates(PreproObsFile, PreproObsData, 'Code Rate Step', 'CODE_RATE_STEP')


    # Phase Rate Step
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["VALID"],PreproIdx["PHASE_RATE_STEP"],\
        PreproIdx["ELEV"], PreproIdx["PRN"]])
    
    print('INFO: Plot Phase Rate Step...')

    # Configure plot and call plot generation function
    plotRates(PreproObsFile, PreproObsData, 'Phase Rate Step', 'PHASE_RATE_STEP')

