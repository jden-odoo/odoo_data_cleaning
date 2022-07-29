# cleans Odoo state/country data and matches with api lookups


import pandas as pd
import sys


# read data from csv
def read_data(dirty_data):
    return pd.read_csv(dirty_data, header=None)


# creates a state dict for state codes
def create_dict():
    df = read_data("../../../data/country_state_code_dirty.csv")
    data = {}
    for state, code, country in zip(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2]):
        if country not in data:
            data[country] = []
        temp = {state: code}
        data[country].append(temp)

    return data


# match state codes in a specified country
def match(state, country, data):
    if country in data:
        if state in data[country]:
            return data[country][state]
    return ""


# creates a country dict from odoo data
def country_dict():
    df = read_data("../../../data/country_code_dirty.csv")
    data = {}
    for country, code in zip(df.iloc[:,0], df.iloc[:,1]):
        data[country] = code
    return data
    

# match country name to country
def match_country(country_name, data):
    if country_name in data:
        return data[country_name]
    return country_name