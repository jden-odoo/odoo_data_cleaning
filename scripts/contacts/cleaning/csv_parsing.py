# Reads and create csv files


import pandas as pd


def read_data(dirty_data):
    """Returns dirty data csv into a dataframe.

    :param str dirtydata: String of file name 
    """

    return pd.read_csv(dirty_data, header=None)


def create_csv(df, old_value):
    """Creates a csv using a dataframe.
    
    :param df df: Dataframe of output file
    :param str old_value: Original file name
    """
    
    text = old_value.split("/")
    newfile = "CLEAN_" + text[len(text)-1][0:len(text[len(text)-1])-4]
    df.to_csv("../../../data/" + newfile + ".csv", sep=',', encoding = 'utf-8')