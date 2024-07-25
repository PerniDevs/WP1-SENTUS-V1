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
    
    return PlotConf


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

    # Divide data frame

    PreproObsDataGalileo = PreproObsData[PreproObsData[PreproIdx["PRN"]].str.startswith("E")]
    galNumSat_smoothed = PreproObsDataGalileo[PreproObsData[PreproIdx["STATUS"]] == 1]
    # print("")
    # print("GAL")
    # print(PreproObsDataGalileo.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]][86350].sum())
    # print(galNumSat_smoothed.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]][86350].sum())

    PreproObsDataGPS = PreproObsData[PreproObsData[PreproIdx["PRN"]].str.startswith("G")]
    gpsNumSat_smoothed = PreproObsDataGPS[PreproObsDataGPS[PreproIdx["STATUS"]] == 1]
    # print("")
    # print("GPS")
    # print(PreproObsDataGPS.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]][86350].sum())
    # print(gpsNumSat_smoothed.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]][86350].sum())
    
    gal_gps_smoothed = PreproObsData[PreproObsData[PreproIdx["STATUS"]] == 1]
    # print("")
    # print("Combined")
    # print(PreproObsData.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]][86350].sum())
    # print(gal_gps_smoothed.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]][86350].sum())

    # Plot configurations for GPS and Galileo
    PlotConfGalileo = {
        "Type": "Lines",
        "FigSize" : (10.4, 6.6),

        "Title" : "Number of GAL Satellites from s6an on Year 24 DoY 011",
        "yLabel" : "Number of Satellites",
        "xLabel" : "Hour of DoY 011",

        "xTicks": range(round(PreproObsDataGalileo[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H), round(PreproObsDataGalileo[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H) + 1),
        "xLim" : [round(PreproObsDataGalileo[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H), round(PreproObsDataGalileo[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H)],

        "yLim" : [0, 20],
        "yTicks" : range(0, 20),

        "Grid" : 1,
        "c" : {0: "orange", 1: "green"},
        "Marker" : "",
        "LineWidth" : 1,
        "LineStyle" : "-",

        "Label" : {0: "RAW", 1: "SMOOTHED"},
        "LabelLoc" : "upper left",
        
        "xData": {
            0: unique(PreproObsDataGalileo[PreproIdx["SOD"]]) / GnssConstants.S_IN_H,
            1: unique(galNumSat_smoothed[PreproIdx["SOD"]]) / GnssConstants.S_IN_H
        },

        "yData": {
            0: PreproObsDataGalileo.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]].sum(),
            1: galNumSat_smoothed.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]].sum()
        },

        "Path": sys.argv[1] + '/OUT/PPVE/SAT/' + 'NUMBER_OF_GAL_SATELLITES_s6an_D011Y24.png',
    }

    PlotConfGPS = {
        "Type": "Lines",
        "FigSize" : (10.4, 6.6),

        "Title" : "Number of GPS Satellites from s6an on Year 24 DoY 011",
        "yLabel" : "Number of Satellites",
        "xLabel" : "Hour of DoY 011",

        "xTicks": range(round(PreproObsDataGPS[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H), round(PreproObsDataGPS[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H) + 1),
        "xLim" : [round(PreproObsDataGPS[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H), round(PreproObsDataGPS[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H)],

        "yLim" : [0, 20],
        "yTicks" : range(0, 20),

        "Grid" : 1,
        "c" : {0: "orange", 1: "green"},
        "Marker" : "",
        "LineWidth" : 1,
        "LineStyle" : "-",

        "Label" : {0: "RAW", 1: "SMOOTHED"},
        "LabelLoc" : "upper left",
        
        "xData": {
            0: unique(PreproObsDataGPS[PreproIdx["SOD"]]) / GnssConstants.S_IN_H,
            1: unique(gpsNumSat_smoothed[PreproIdx["SOD"]]) / GnssConstants.S_IN_H
        },

        "yData": {
            0: PreproObsDataGPS.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]].sum(),
            1: gpsNumSat_smoothed.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]].sum()
        },

        "Path": sys.argv[1] + '/OUT/PPVE/SAT/' + 'NUMBER_OF_GPS_SATELLITES_s6an_D011Y24.png',
    }

    PlotConf = {
        "Type": "Lines",
        "FigSize" : (10.4, 6.6),

        "Title" : "Number of GPS+GAL from s6an on Year 24 DoY 011",
        "yLabel" : "Number of Satellites",
        "xLabel" : "Hour of DoY 011",

        "xTicks": range(round(PreproObsData[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H), round(PreproObsData[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H) + 1),
        "xLim" : [round(PreproObsData[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H), round(PreproObsData[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H)],

        "yLim" : [0, 20],
        "yTicks" : range(0, 20),

        "Grid" : 1,
        "c" : {0: "orange", 1: "green"},
        "Marker" : "",
        "LineWidth" : 1,
        "LineStyle" : "-",

        "Label" : {0: "RAW", 1: "SMOOTHED"},
        "LabelLoc" : "upper left",

        "xData": {
            0: unique(PreproObsData[PreproIdx["SOD"]]) / GnssConstants.S_IN_H,
            1: unique(gal_gps_smoothed[PreproIdx["SOD"]]) / GnssConstants.S_IN_H
        },

        "yData": {
            0: PreproObsData.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]].sum(),
            1: gal_gps_smoothed.groupby(PreproIdx["SOD"])[PreproIdx["STATUS"]].sum()
        },

        "Path": sys.argv[1] + '/OUT/PPVE/SAT/' + 'NUMBER_OF_GPS+GAL_SATELLITES_s6an_D011Y24.png',

    }

    data_array = [PlotConfGalileo, PlotConfGPS, PlotConf]

    for conf in data_array:
        generatePlot(conf)


# Plot Code IF - Code IF Smoothed
def plotIFIFSmoothed(PreproObsFile, PreproObsData):
    PlotConf = {}


# Plot C/N0
def plotCN0(PreproObsFile, PreproObsData, PlotTitle, PlotLabel):
    PlotConf = {}


# Plot Rejection Flags
def plotRejectionFlags(PreproObsFile, PreproObsData):
    all_prns = allprns()

    gal_prn = [int(convert_satlabel_to_prn(const)) for const, _ in all_prns.items() if const.startswith("E")]
    gps_prn = [int(convert_satlabel_to_prn(const)) for const, _ in all_prns.items() if const.startswith("G")]

    PreproObsDataGalileo = PreproObsData[(PreproObsData[PreproIdx["PRN"]].str.startswith("E") & (PreproObsData[PreproIdx["REJECT"]] != 0))]
    PreproObsDataGPS =     PreproObsData[(PreproObsData[PreproIdx["PRN"]].str.startswith("G") & (PreproObsData[PreproIdx["REJECT"]] != 0))]

    PlotConfGalileo = {
        "Type": "Lines",
        "FigSize" : (10.4, 6.6),

        "Title" : "GAL Rejection Flags from s6an on Year 24 DoY 011",
        "yLabel" : "GAL Rejection Flags",
        "xLabel" : "Hour of DoY 011",

        "xTicks": range(int(round(PreproObsDataGalileo[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H)), int(round(PreproObsDataGalileo[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H)) + 1),
        "xLim" : [int(round(PreproObsDataGalileo[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H)), int(round(PreproObsDataGalileo[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H))],

        "yLim" : [0, len(REJECTION_CAUSE_DESC.keys()) + 1],
        "yTicks" : range(1, len(REJECTION_CAUSE_DESC.keys()) + 1 ),
        "yTicksLabels" : REJECTION_CAUSE_DESC.keys(), 

        "Marker" : ".",
        "LineWidth" : 0,
        "Grid" : 1,

        "ColorBar" : "gist_ncar",
        "ColorBarLabel" : "Galileo PRN",
        "ColorBarMin" : min(gal_prn),
        "ColorBarMax" : max(gal_prn),
        "ColorBarSetTicks": sorted(gal_prn),
        "ColoBarBins": len(gal_prn), 

        "s" : 20, 
        "Label" : 0,
        
        "Annotations": {0: PreproObsDataGalileo[PreproIdx["PRN"]]},

        "xData": {0: unique(PreproObsDataGalileo[PreproIdx["SOD"]]) / GnssConstants.S_IN_H},
        "yData": {0: PreproObsDataGalileo[PreproIdx["REJECT"]]},
        "zData" : {0: [int(convert_satlabel_to_prn(prn)) for prn in PreproObsDataGalileo[PreproIdx["PRN"]]]}, 

        "Path": sys.argv[1] + '/OUT/PPVE/SAT/' + 'GAL_REJECTION_FLAGS_s6an_D011Y24.png',
    }

    PlotConfGPS = {
        "Type": "Lines",
        "FigSize" : (10.4, 6.6),

        "Title" : "GPS Rejection Flags from s6an on Year 24 DoY 011",
        "yLabel" : "GPS Rejection Flags",
        "xLabel" : "Hour of DoY 011",

        "xTicks": range(int(round(PreproObsDataGPS[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H)), int(round(PreproObsDataGPS[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H)) + 1),
        "xLim" : [int(round(PreproObsDataGPS[PreproIdx["SOD"]].min() / GnssConstants.S_IN_H)), int(round(PreproObsDataGPS[PreproIdx["SOD"]].max() / GnssConstants.S_IN_H))],

        "yLim" : [0, len(REJECTION_CAUSE_DESC.keys()) + 1],
        "yTicks" : range(1, len(REJECTION_CAUSE_DESC.keys()) + 1),
        "yTicksLabels" : REJECTION_CAUSE_DESC.keys(), 

        "Marker" : ".",
        "LineWidth" : 0,
        "Grid" : 1,

        "ColorBar" : "gist_ncar",
        "ColorBarLabel" : "GPS PRN",
        "ColorBarMin" : min(gps_prn),
        "ColorBarMax" : max(gps_prn),
        "ColorBarSetTicks": sorted(gps_prn),
        "ColoBarBins": len(gps_prn), 

        "s" : 20, 
        "Label" : 0,
        
        "Annotations": {0: PreproObsDataGPS[PreproIdx["PRN"]]},

        "xData": {0: PreproObsDataGPS[PreproIdx["SOD"]] / GnssConstants.S_IN_H},
        "yData": {0: PreproObsDataGPS[PreproIdx["REJECT"]]},
        "zData" : {0: [int(convert_satlabel_to_prn(prn)) for prn in PreproObsDataGPS[PreproIdx["PRN"]]]}, 

        "Path": sys.argv[1] + '/OUT/PPVE/SAT/' + 'GPS_REJECTION_FLAGS_s6an_D011Y24.png',
    }

    all_confs = [PlotConfGalileo, PlotConfGPS]

    for conf in all_confs:
        generatePlot(conf)

    # generatePlot(PlotConfGalileo)

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
    PreproObsData_test = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None)
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

