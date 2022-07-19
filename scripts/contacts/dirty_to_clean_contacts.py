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


# returns a list of [latitude, longitude]
def get_lat_lon(bounds):
    return [bounds["lat"], bounds["lng"]]


# returns a list of dictionaries [{Address: [Latitude, Longitude]}, ..] (google maps api)
def get_address_info(addresses):
    data = []
    for address in addresses:
        each_address = {}
        # url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input= " + address + "&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=" + config.api_key
        payload = {}
        headers = {}
        request = None # some call
        # request = requests.request("GET", url, headers=headers, data=payload)
        # request_data = json.load(request)
        # change below request -> request_data
        lat_lon = get_lat_lon(request["candidates"][0]["geometry"]["location"])
        each_address[request["candidates"][0]["formatted_address"]] = lat_lon
        data.append(each_address)
    return data


# same as get_address_info() but uses locationiq api 
def get_address_info_2(addresses):
    data = []
    for address in addresses:
        each_address = {}
        url = "https://us1.locationiq.com/v1/search?key=" + config.locationiq_api_key + "&q=" + address + "&format=json"
        response = requests.get(url)
        result = response.json()
        lat_lon = [result[0]["lat"], result[0]["lon"]]
        each_address[result[0]["display_name"]] = lat_lon
        data.append(each_address)
    return data


# same as get_address_info() but uses geocode earth api
def get_address_info_3(addresses):
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
                each_address["N/A"] = lat_lon
                data.append(each_address) 
        else:
            lat_lon = ["N/A", "N/A"]
            each_address["N/A"] = lat_lon
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
    data = get_address_info_3(all_addresses)
    values = dict_to_list(data)
    new_df = pd.DataFrame(values, columns=["Addresses", "Latitude", "Longitude"]).iloc[1: , :].set_index("Addresses")
    create_csv(new_df)


dirty_data = sys.argv[1]
index = sys.argv[2].split(",")
create(dirty_data, index)