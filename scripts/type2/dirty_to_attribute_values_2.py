# Input Format: python3 dirty_toattribute_values_v2.py filename parentlist productid attribute value 
# Assumptions:
#   Attribute name case insensitive


import pandas as pd
import sys


# returns dataframe from dirty data csv
def read_data(dirty_data):
    return pd.read_csv(dirty_data)


# creates an excel file using dataframe
def create_csv(df):
    df.to_excel(excel_writer = "../../data/attr-val2.xlsx")


# returns all attributes in a given column
def get_attributes_list(attributes,df):
    return df.iloc[:,ord(attributes)-97]


# returns all values in a given column
def get_values_list(values,df):
    return df.iloc[:,ord(values)-97]


# creates a dictionary {Attribute: [Value1, Value2..,ValueN]}
def create(file, attributes, values):
    attribute_values = {}
    df = read_data(file)
    attribute_list = get_attributes_list(attributes, df)
    values_list = get_values_list(values, df)
    for i in range(len(attribute_list)):
        # checks if attribute name is a string
        if(isinstance(attribute_list[i], str)):
            if attribute_list[i] in attribute_values:
                # removes duplicates
                # case insensitive
                if values_list[i] not in attribute_values[attribute_list[i]]:
                    attribute_values[attribute_list[i]].append(values_list[i])
            else:
                values = []
                values.append(values_list[i])
                attribute_values[attribute_list[i]] = values
    return attribute_values


# creates a dataframe using attribute_values dictionary
def create_df(attribute_values):
    data = []
    prev = ""
    count = 1
    for key in attribute_values:
        for value in attribute_values[key]:
            if prev != key:
                count = 1
                # creates a value_ids/id
                value_id_id = str(key).replace(" ", "_") + "_" + str(count)
                # creates attribute external id and appends the line into a list, data
                # replaces spaces and periods with underscores
                data.append([key, "attribute_" + str(key).replace(" ", "_").replace(".", "_").lower(), "Radio", "Instantly", "Visible", value, value_id_id.lower()])
            else:
                # creates a value_ids/id
                value_id_id = str(key).replace(" ", "_") + "_" + str(count)
                # appends the line into a list, data
                data.append(["","","","","",value,value_id_id.lower()])
            prev = key
            count = count + 1
    df = pd.DataFrame(data, columns=["name", "id", "display_type", "create_variant", "visibility", "value_ids/name", "value_ids/id"]).set_index('name')
    return df


def main():

    a_v = create(sys.argv[1], sys.argv[4], sys.argv[5])
    df = create_df(a_v)
    create_csv(df)


main()