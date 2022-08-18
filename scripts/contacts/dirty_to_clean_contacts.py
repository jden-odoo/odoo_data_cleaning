# Input: python3 dirty_to_clean_contacts.py filename addresses_columns
#
# Sample Input: python3 dirty_to_clean_contacts.py ../../data/short_contacts_data.csv d
# Sample Input: python3 dirty_to_clean_contacts.py ../../data/main_addresses.csv d,e,f


import re
import pandas as pd
import sys
import json

import urllib.request
import config as config
import requests


# reads csv file into dataframe
def read_data(dirty_data):
    return pd.read_csv(dirty_data, header=None)


# gets all addresses from dirty data based on given indexes
def get_all_addresses(index, df):
    rows = len(df)
    data = []
    for i in range(rows):
        data.append("")
    for i in index:
        for r in range(rows):
            p2 = df.iloc[r,ord(i)-97]
            if not (isinstance(p2, str)):
                p2 = ""
            data[r] = str(data[r]) + str(p2) + " "
    new_df = pd.DataFrame(data, columns=["addresses"])
    return new_df.iloc[:,0]


# returns a list of dictionaries [{Address: [Latitude, Longitude]}, ..]
# same as get_address_info() but uses geocode earth api
def get_address_info(addresses):
    data = []
    for address in addresses:
        each_address = {}
        if address.replace(" ","") != "":
            updated_address = re.sub('[^a-zA-z0-9 \n\.]', '', address)
            url = ("https://api.geocode.earth/v1/search?" \
            "api_key="+config.geocode_api_key+"&"\
            "text=" + updated_address).replace(' ', '+').replace('\n', '+')
            response = json.load(urllib.request.urlopen(url))
            if response['features']:
                lat_lon = response['features'][0]['geometry']['coordinates']
                each_address[response['features'][0]['properties']['label']] = lat_lon
                data.append(each_address)
            else:
                lat_lon = ["N/A", "N/A"]
                each_address[address] = lat_lon
                data.append(each_address) 
        else:
            lat_lon = ["N/A", "N/A"]
            each_address[address] = lat_lon
            data.append(each_address)
    return data


# returns the list of dictionaries to a 2d list
def dict_to_list(values):
    data = []
    for i in range(len(values)):
        for k in values[i]:
            data.append([k, values[i][k][0], values[i][k][1]])
    return data


# creates a csv given a dataframe
def create_csv(df):
    df.to_csv("../../data/temp.csv", sep=',', encoding = 'utf-8')


def create(dirty_data, index):
    df = read_data(dirty_data)
    all_addresses = get_all_addresses(index, df)
    data = get_address_info(all_addresses)
    values = dict_to_list(data)
    new_df = pd.DataFrame(values, columns=["Addresses", "Latitude", "Longitude"]).iloc[1: , :].set_index("Addresses")
    create_csv(new_df)


dirty_data = sys.argv[1]
index = sys.argv[2].split(",")
create(dirty_data, index)