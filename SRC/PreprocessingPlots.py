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
from COMMON.missingPRNs import missing_prns_before
from COMMON.Plots import generatePlot
from COMMON.allPRNs import allprns
from COMMON.dataDivider import dataDivider


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

    all_prns = allprns()

    PlotConf = {}
    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.4,14.6)
    PlotConf["Title"] = "Satellite Visibility from s6an on Year 24 DoY 011"   

    # PlotConf["yLabel"] = "GPS-GAL-PRN"
    # PlotConf["yTicks"] = range(1, len(all_prns.values()))
    # PlotConf["yTicksLabels"] = sorted(all_prns.keys())
    # PlotConf["yLim"] = [0, len(all_prns.values())]

    PlotConf["yLabel"] = "GPS-GAL-PRN"
    PlotConf["yTicks"] = range(0, len(sorted(unique(PreproObsData[PreproIdx["PRN"]]))))
    PlotConf["yTicksLabels"] = sorted(unique(PreproObsData[PreproIdx["PRN"]]))
    PlotConf["yLim"] = [-0.5, len(sorted(unique(PreproObsData[PreproIdx["PRN"]])))]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 1.5

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    PlotConf["Flags"] = {}

    # for prn_key, prn_value in all_prns.items():
    #     FilterCond = PreproObsData[PreproIdx["PRN"]] == prn_key
    #     PlotConf["xData"][prn_value] = PreproObsData[PreproIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
    #     PlotConf["yData"][prn_value] = PreproObsData[PreproIdx["PRN"]][FilterCond]
    #     PlotConf["zData"][prn_value] = PreproObsData[PreproIdx["ELEV"]][FilterCond]
    #     PlotConf["Flags"][prn_value] = PreproObsData[PreproIdx["STATUS"]][FilterCond]

    for prn in sorted(unique(PreproObsData[PreproIdx["PRN"]])):
        FilterCond = PreproObsData[PreproIdx["PRN"]] == prn
        PlotConf["xData"][prn] = PreproObsData[PreproIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = PreproObsData[PreproIdx["PRN"]][FilterCond]
        PlotConf["zData"][prn] = PreproObsData[PreproIdx["ELEV"]][FilterCond]
        PlotConf["Flags"][prn] = PreproObsData[PreproIdx["STATUS"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/PPVE/SAT/' + 'SAT_VISIBILITY_s6an_D011Y24.png'

    # Debugging output
    generatePlot(PlotConf)

# Plot Number of Satellites
def plotNumSats(PreproObsFile, PreproObsData):
    
    PlotConf = {}

    # PlotConf["Type"] = "Lines"
    # PlotConf["FigSize"] = (10.4, 6.6)
    
    # PlotConf["yLabel"] = "Number of Satellites"
    # PlotConf["xLabel"] = "Hour DoY 006"
    
    # PlotConf["xTicks"] = range(
    #     round(PreproObsData[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H),
    #     round(PreproObsData[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H) + 1
    # )
    # PlotConf["xLim"] = [
    #     round(PreproObsData[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H),
    #     round(PreproObsData[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H)
    # ]
    
    # PlotConf["yLim"] = [0, 20]
    # PlotConf["yTicks"] = range(0, 20)
    
    # PlotConf["Grid"] = 1
    
    # PlotConf["c"] = {0: "orange", 1: "green"}
    
    # PlotConf["Marker"] = ""
    # PlotConf["LineWidth"] = 1
    # PlotConf["LineStyle"] = "-"
    
    # PlotConf["Label"] = {0: "RAW", 1: "SMOOTHED"}
    # PlotConf["LabelLoc"] = "upper left"
    
    # PlotConf["xData"] = {}
    # PlotConf["yData"] = {}
    
    # all_prns =allprns()

    # e_const, g_const = dataDivider(PreproObsData, all_prns)

    # # Handling GPS data
    # g_const_counts = g_const.groupby(PreproObsData[PreproIdx["SOD"]])[PreproObsData[PreproIdx["PRN"]]].nunique()
    # PlotConf["xData"][0] = g_const_counts.index / GnssConstants.S_IN_H
    # PlotConf["yData"][0] = g_const_counts.values

    # # Continue with plotting using PlotConf
    # generatePlot(PlotConf)

# Plot Code IF - Code IF Smoothed
def plotIFIFSmoothed(PreproObsFile, PreproObsData):
    PlotConf = {}


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

