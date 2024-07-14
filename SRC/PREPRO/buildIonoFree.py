def buildIonoFree(PreproObs, GammaF1F2):

    c_iono_free = (PreproObs["C2"] - GammaF1F2 * PreproObs["C1"])/(1-GammaF1F2)
    p_iono_free = (PreproObs["L2Meters"] - GammaF1F2 * PreproObs["L1Meters"])/(1-GammaF1F2)
    
    PreproObs["IF_C"] = c_iono_free
    PreproObs["IF_P"] = p_iono_free

    return PreproObs