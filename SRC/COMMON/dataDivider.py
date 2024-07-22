import pandas as pd
from InputOutput import PreproIdx


def dataDivider(df:pd.DataFrame, all_prns):
    
    e_const = [prn for prn in all_prns if prn.startswith("E")]
    g_const = [prn for prn in all_prns if prn.startswith("E")]

    df_e = df[df[PreproIdx["PRN"]].isin(e_const)]
    df_g = df[df[PreproIdx["PRN"]].isin(g_const)]

    # print("E constellation data:\n", df_e)
    # print("G constellation data:\n", df_g)

    return df_e, df_g