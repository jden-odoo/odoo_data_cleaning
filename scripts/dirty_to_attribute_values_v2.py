# Input Format: python3 dirty_toattribute_values_v2.py filename productid attribute value parentlist
# Assumptions:
#   Attribute name 
# Sample Input: python3 dirty_to_attribute_values_v2.py ../data/dirty_data_v2.csv a i j b,c,d


import pandas as pd
import sys


def read_data(dirty_data):
    return pd.read_csv(dirty_data)


def create_csv(df):
    df.to_excel(excel_writer = "../data/attr-val.xlsx")


def get_attributes_list(attributes,df):
    print(len(df))
    print(len(df.iloc[:,ord(attributes)-97]))
    return df.iloc[:,ord(attributes)-97]


def get_values_list(values,df):
    return df.iloc[:,ord(values)-97]


def create(file, attributes, values):
    attribute_values = {}
    df = read_data(file)
    attribute_list = get_attributes_list(attributes, df)
    values_list = get_values_list(values, df)
    for i in range(len(attribute_list)):
        if(isinstance(attribute_list[i], str)):
            if attribute_list[i] in attribute_values:
                if values_list[i] not in attribute_values[attribute_list[i]]:
                    attribute_values[attribute_list[i]].append(values_list[i])
            else:
                values = []
                values.append(values_list[i])
                attribute_values[attribute_list[i]] = values
    return attribute_values


def create_df(attribute_values):
    data = []
    prev = ""
    count = 1
    for key in attribute_values:
        for value in attribute_values[key]:
            if prev != key:
                count = 1
                value_id_id = str(key).replace(" ", "_") + "_" + str(count)
                data.append([key, "attribute_" + str(key).replace(" ", "_"), "Radio", "Instantly", "Visible", value, value_id_id.lower()])
            else:
                value_id_id = str(key).replace(" ", "_") + "_" + str(count)
                data.append(["","","","","",value,value_id_id.lower()])
            prev = key
            count = count + 1
    df = pd.DataFrame(data, columns=["name", "id", "display_type", "create_variant", "visibility", "value_ids/name", "value_ids/id"]).set_index('name')
    return df


def create_csv(df):
    df.to_excel(excel_writer = '../data/attr-val.xlsx')


def main():
    a_v = create(sys.argv[1], sys.argv[3], sys.argv[4])
    df = create_df(a_v)
    create_csv(df)


main()