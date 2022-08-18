# cleans Odoo state/country data and matches with api lookups


import pandas as pd
import sys


def read_data(dirty_data):
    """Returns dirty data csv into a dataframe.

    :param str dirtydata: String of file name 
    """

    return pd.read_csv(dirty_data, header=None)


def create_dict():
    """Creates a dictionay for state codes.
    
    :return: {Country: {State: Code}}
    ;rtype: dict
    """
    df = read_data("../../../data/country_state_code_dirty.csv")
    data = {}
    for state, code, country in zip(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2]):
        if country not in data:
            data[country] = []
        temp = {state: code}
        data[country].append(temp)

    return data


def match(state, country, data):
    """Matches state code with data within a specified country.
    
    :return: State code
    :rtype: str
    """
    if country in data:
        if state in data[country]:
            return data[country][state]
    return ""
    


def country_dict():
    """Creates a dictionay for country codes.
    
    :return: {Country: Code}
    ;rtype: dict
    """
    df = read_data("../../../data/country_code_dirty.csv")
    data = {}
    for country, code in zip(df.iloc[:,0], df.iloc[:,1]):
        data[country] = code
    return data
    

def match_country(country_name, data):
    """Matches country code with data.
    
    :return: Country code
    :rtype: str
    """
    if country_name in data:
        return data[country_name]
    return country_name