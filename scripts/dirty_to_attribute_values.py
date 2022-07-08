#############################################################################################
#Usage: python3 dirty_to_attribute_values.py dirtydata.csv columns unit    
#Input (Space separated): 
#   1. Dirtydata.csv
#   2. column letters for attribute/value pairs
#   3. company name

#Output: attr-val.xlsx
#Sample Input: python3 dirty_to_attribute_values.py dirtydata.csv b, companyname, unit

import pandas as pd
import sys


display_type = "Radio"
create_variant = "Instantly"
visibility = "Visible"
company_name = "ABA company"
attributes = ["Name", "Manufacturer", "Collection", "Color", "Vendor_SKU", "Designer", "Fabric_Type", "Fiber_Contents", "Fabric_Width", "Putup_Format", "Sales Price", "Product Category"]


# Gets dirty data from dirty data csv
def get_dirty_data(dirtydata):
    return pd.read_csv(dirtydata)

# Returns list of column names ordered by dirty data csv
def list_names(dirty_data):
    return dirty_data.columns


# Get input names (case insensisitive)
# Future implementation will be drop down XML
def get_names(values):
    array = []
    for value in values:
        value = ord(value.lower())-97
        array.append(attributes[value])
    return array


def get_number_columns(values):
    array = []
    for value in values:
        value = ord(value.lower())-97
        array.append(value)
    return array


# Create ids for name_list
def get_ids(name_list, company_name):
    ids_list = []
    for cell in name_list:
        if cell in ids_list and pd.isna(cell):
            ids_list.append(" ")
        else:
            ids_list.append(company_name.lower()[:2] + "-" + cell.lower())
    return ids_list


# Get value_id/name from dirty data
def get_value_id_name(column_name, dirty_data):
    value_id_names = []
    for value in dirty_data.iloc[:,column_name].tolist():
        if value not in value_id_names:
            value_id_names.append(value)
    return value_id_names


# Creates a csv for the output
def create_csv(df):
    df.to_excel(excel_writer = '../data/attr-val.xlsx')


# Create the data to be added to the new dataframe for the output csv
# Creates value_id/id
# Appends values into the data and returns a dataframe with data
def create(input_array, dirtydata, companyname):
    dirty_data = get_dirty_data(dirtydata)
    names_list = get_names(input_array)
    numbers = get_number_columns(input_array)
    ids_list = get_ids(names_list, companyname)
    data = []
    count = 0
    for name in names_list:
        value_id_names = get_value_id_name(numbers[count], dirty_data)
        id_num = 1
        prev = ""
        for value in value_id_names:
            if not isinstance(value, str):
                continue
            value_id_id = name.lower() + "_" + str(id_num)
            id_num = id_num + 1
            if prev == name:
                data.append(["","","","","",value,value_id_id])
            else:
                data.append([name, ids_list[count], display_type, create_variant, visibility, value, value_id_id.lower()])
            prev = name
        count = count + 1
    df = pd.DataFrame(data, columns=["name", "id", "display_type", "create_variant", "visibility", "value_ids/name", "value_ids/id"]).set_index('name')
    return df


# Creates csv for dataframesantee
def parse(input_array, dirtydata, companyname):
    df = create(input_array, dirtydata, companyname)
    create_csv(df)

arr = sys.argv[2].split(",")
arr = arr[1:len(arr)-3]
parse(arr, sys.argv[1], sys.argv[3])