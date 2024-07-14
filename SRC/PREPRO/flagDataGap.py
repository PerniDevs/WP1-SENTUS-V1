def flagDataGap (PreproObsInfo, SatLabel):
    PreproObsInfo[SatLabel]["Valid"] = 0
    PreproObsInfo[SatLabel]["RejectionCause"] = 2
    return PreproObsInfo