# Input: python3 dirty_contacts.py filename address_columns
#
# Inserts formatted Address, Latitude and Longitude into original data
#
# Sample Input: python3 dirty_contacts.py ../../data/short_contacts_data.csv d


import numpy as np
import pandas as pd
import sys


def read_data(dirty_data):
    return pd.read_csv(dirty_data)


def create_excel(new_data):
    new_data.to_excel(excel_writer = "../../data/clean_contacts.xlsx")


def get_new_contacts():
    df = read_data("../../data/temp.csv")
    data = []
    for index, row in df.iterrows():
        data.append([row["Addresses"], row["Latitude"], row["Longitude"]])
    return data


def column(matrix, i):
    return [row[i] for row in matrix]


def create(dirty_data, index):
    data = []
    num_index = []
    columns_list = []
    df = read_data(dirty_data)
    for i in index:
        num_index.append(ord(i)-97)
    address = get_new_contacts()
    for i in range(len(df.columns)):
        if i == num_index[0]:
            for j in range(3):
                data.append(column(address,j))
            columns_list.append("Address")
            columns_list.append("Latitude")
            columns_list.append("Longitude")
        elif i not in num_index:
            data.append(df.iloc[:,i].tolist())
            columns_list.append(df.columns[i])
    array = []
    for i in range(len(data[0])):
        array.append(i)
    res = pd.DataFrame({'tmp': array})
    for i in range(len(data)):
        temp = pd.DataFrame({columns_list[i]: data[i]})
        temp['tmp'] = array
        res = res.merge(temp, on="tmp", how="left")
    res = res.iloc[:,1:].set_index(columns_list[0])
    create_excel(res)


dirty_data = sys.argv[1]
index = sys.argv[2].split(",")
create(dirty_data, index)
    