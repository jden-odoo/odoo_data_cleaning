#
#
# Sample Input: python3 dirty_contacts.py ../data/short_contacts_data.csv 


import pandas as pd
import sys


def read_data(dirty_data):
    return pd.read_csv(dirty_data)


def create_excel(new_data):
    new_data.to_excel(excel_writer = "../data/clean_contacts.xlsx")


def get_new_contacts():
    df = read_data("../data/temp.csv")
    print(df)
    data = []
    for index, row in df.iterrows():
        data.append(row)
    return data


def create():
    data = get_new_contacts()
    res = pd.DataFrame(data, columns=["Addresses", "Latitude", "Longitude"]).set_index("Addresses")
    create_excel(res)


create()
    