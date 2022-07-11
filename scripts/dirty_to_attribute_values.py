#############################################################################################
#Usage: python3 dirty_to_attribute_values.py dirtydata.csv attributes    
#Input (Space separated): 
#   1. Dirtydata.csv
#   2. column letters for attributes

#Output: attr-val.xlsx
#Sample Input: python3 dirty_to_attribute_values.py dirtydata.csv b,c,e,f,g,h,i,j,k


import pandas as pd
import sys


display_type = "Radio"
create_variant = "Instantly"
visibility = "Visible"


# Gets dirty data from dirty data csv
def get_dirty_data(dirtydata):
    return pd.read_csv(dirtydata)


# Returns list of column names ordered by dirty data csv
def list_all_columns(dirty_data):
    return dirty_data.columns


# Future implementation will be drop down XML
def get_attribute_names(input_array, all_columns):
    array = []
    for value in input_array:
        value = ord(value.lower())-97
        array.append(all_columns[value])
    return array


# Create ids for name_list
def get_external_ids(name_list):
    ids_list = []
    for cell in name_list:
        if cell in ids_list and cell != " ":
            ids_list.append(" ")
        else:
            ids_list.append("attribute" + "_" + cell.lower())
    return ids_list


# Get value_id/name from dirty data
def get_value_id_name(column_name, dirty_data):
    value_id_names = []
    for value in dirty_data[column_name].tolist():
        if value not in value_id_names
            value_id_names.append(value)
    return value_id_names


# Creates a csv for the output
def create_csv(df):
    df.to_excel(excel_writer = '../data/attr-val.xlsx')


# Create the data to be added to the new dataframe for the output csv
# Creates value_id/id
# Appends values into the data and returns a dataframe with data
def create(input_array, dirtydata):
    #creates dirty data dataframe
    dirty_data = get_dirty_data(dirtydata)
    #all columns of the dirty_data dataframe
    all_columns = list_all_columns(dirty_data)
    #get all attribute names from all_columns
    attribute_names = get_attribute_names(input_array, all_columns)
    #create ids from names_list
    external_ids = get_external_ids(attribute_names)
    data = []
    count = 0
    for name in attribute_names:
        value_id_names = get_value_id_name(name, dirty_data)
        id_num = 1
        prev = ""
        for value in value_id_names:
            if not isinstance(value, str):
                continue
            #create value_ids/id
            value_id_id = name.lower() + "_" + str(id_num)
            id_num = id_num + 1
            if prev == name:
                data.append(["","","","","",value,value_id_id])
            else:
                data.append([name, external_ids[count], display_type, create_variant, visibility, value, value_id_id.lower()])
            prev = name
        count = count + 1
    df = pd.DataFrame(data, columns=["name", "id", "display_type", "create_variant", "visibility", "value_ids/name", "value_ids/id"]).set_index('name')
    return df


# Creates csv for dataframe
def parse(input_array, dirtydata):
    df = create(input_array, dirtydata)
    create_csv(df)


arr = sys.argv[2].split(",")
arr = arr[1:len(arr)-3]
parse(arr, sys.argv[1])

#arr = sys.argv[3].split(",")

#parse(arr, sys.argv[1])