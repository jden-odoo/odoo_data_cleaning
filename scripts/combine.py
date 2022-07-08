import pandas as pd

#############################################################################
#Input: 1: '../data/attr-val.csv' i.e. output from dirty_to_attribute_values.py
#       2: '../data/outputdata.csv' i.e. output from dirty_to_clean.py


#Output: final_output.xlsx, which is a spreadsheet ready for import into Odoo
#############################################################################

def main():
    attr_val_dict = create_attr_val_dict()
    final_data_df = add_attr_to_clean(attr_val_dict)
    final_data_df.to_excel(excel_writer = '../data/final_output.xlsx')

#############################################
# Convert attribute/value data to a dictionary
# Input: Datafram from excel file
# Output: Nested dictionary, where outer key is attribute name and inner key is value name.
# The outer key corresponds to a diciontary with two values inside it
# 1. 'category-external-id', which is the attributes external id as a string.
# 2. an inner key, which corresponds to an inner dictionary
#
# The inner key's dictionary has the value external ids in it
# All keys in the dictionary have spaces in them replaced with _
# External id's are not modified at all
#
# Example 
# Original excel file
# Attribute_Name,Attribute_External_ID,Value_Name,Value_External_ID
# Color of Car Body,car_body_color,White,car_body_white
# ,,Green,car_body_green
# Color of Car Trim,car_trim_color,White,car_trim_white
# ,,Green, car_trim_green
#
# create_attr_val_dict() will return:
# {
#     'color_of_car_body', {
#         'car_body_color_value': {
#             'category_external_id': 'car_body_color',
#             'white': 'car_body_white',
#             'green': 'car_body_green'
#         }
#     }
#     'color_of_car_trim', {
#         'car_trim_color_value': {
#             'category_external_id': 'car_body_color',
#             'white': 'car_body_white',
#             'green': 'car_body_green'
#         }
#     }
# }

def create_attr_val_dict():

    

    #dirty_to_attribute_values output
    #attr_val_df = pd.read_excel('../data/attr-val.xlsx')


    #Testing
    attr_val_df = pd.read_excel('../data/original-attr-val.xlsx')

    # attr_name_values = attr_val_df['value_ids/name'] 
    # attr_name_external_ids = attr_val_df['value_ids/id']
    attr_val_dict = {}
    currDict = {}
    currCategory = None

    for row in range(0, len(attr_val_df)): 
        if not pd.isna(attr_val_df['name'][row]):  
            if currCategory:
                attr_val_dict[currCategory] = currDict
            currCategory = str(attr_val_df['name'][row]).replace(' ','_').lower() #Replace space with underscore for consistency
            currDict = {}
            currDict['category_external_id'] = str(attr_val_df['id'][row]).lower() 

        currDict[str(attr_val_df['value_ids/name'][row]).lower()] = str(attr_val_df['value_ids/id'][row])

    if currCategory:
        attr_val_dict[currCategory] = currDict

    return attr_val_dict


def add_attr_to_clean(attr_val_dict):
    clean_data_df = pd.read_csv('../data/outputdata.csv')
    clean_data_df['Product Attributes / Attributes / External ID'] = ""
    clean_data_df['Product Attributes / Values / External ID'] = ""

    for row in range(0, len(clean_data_df)): #attributes/external id needs fix

        category_name = str(clean_data_df['Attribute'][row]).lower()
        attr_name = str(clean_data_df['Value'][row]).lower()
        if category_name != 'nan':
            clean_data_df['Product Attributes / Attributes / External ID'][row] = attr_val_dict[category_name]['category_external_id']
            if attr_name != 'nan':
                clean_data_df['Product Attributes / Values / External ID'][row] = attr_val_dict[category_name][attr_name]

    return clean_data_df  



main()