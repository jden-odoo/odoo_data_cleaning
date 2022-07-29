# Reads and create csv files


import pandas as pd


# reads csv file into dataframe
def read_data(dirty_data):
    return pd.read_csv(dirty_data, header=None)


# creates a csv given a dataframe
def create_csv(df, old_value):
    text = old_value.split("/")
    newfile = "CLEAN_" + text[len(text)-1][0:len(text[len(text)-1])-4]
    df.to_csv("../../../data/" + newfile + ".csv", sep=',', encoding = 'utf-8')