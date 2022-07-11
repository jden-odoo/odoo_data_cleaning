#############################################
# Convert attribute/value data to a dictionary
# Input: None. The name of the file to be opened is hard coded.
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
# ,,Green,car_trim_green
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
#             'white': 'car_trim_white',
#             'green': 'car_trim_green'
#         }
#     }
# }
##################################################

def create_attr_val_dict():


    #Testing
    attr_val_df = pd.read_excel('../data/original-attr-val.xlsx')

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