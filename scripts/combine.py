#Script to combine the clean data with the atrribute/value data
#Written for python 3.8.5


import pandas as pd
#requires openpxl


#Convert attribute/value data to a dictionary
attribute_value_data = {}


#Create df for attribute/value excel file
attr_val_df = pd.read_excel('data/attr-val.xlsx')#TODO: prompt for user input for file name
attr_name_values = attr_val_df['value_ids/name'] #TODO: use regex or prompt user for input, probably input column
attr_name_external_ids = attr_val_df['value_ids/id']

# print(keys.isnull().values.any())
# print(vals.head().isnull().values.any())
# print(attr_val_df['name'][25])
# print(len(attr_val_df))

attr_val_dict = {}
currDict = {}
currCategory = None

for row in range(0, len(attr_val_df)): #Assumes no null keys or vals
    if not pd.isna(attr_val_df['name'][row]): #TODO: unhardcode 
        if currCategory:
            attr_val_dict[currCategory] = currDict
        currCategory = str(attr_val_df['name'][row]).lower()
        # print(attr_val_df['id'])
        currDict = {}
        currDict['category_external_id'] = str(attr_val_df['id'][row]).lower() #TODO: reserved/enum?

    currDict[str(attr_val_df['value_ids/name'][row]).lower()] = str(attr_val_df['value_ids/id'][row]).lower()

print(currCategory)
print(currDict)
if currCategory:
    attr_val_dict[currCategory] = currDict



#Manually modified file
#clean_data_df = pd.read_excel('data/modified-clean-data.xlsx')

#Dataframe for clena data without attributes
clean_data_df = pd.read_excel('data/clean-data-original.xlsx')

def cleanCells(x):
    x.str.strip() if x.dtype == "object" else x
    x.str.replace(' ','_')

clean_data_df.applymap(cleanCells)




clean_data_df['Product Attributes / Attributes / External ID'] = ""
clean_data_df['Product Attributes / Values / External ID'] = ""

for row in range(0, len(clean_data_df)): #attributes/external id needs fix
    print(row)

    category_name = str(clean_data_df['Attribute'][row]).lower()
    attr_name = str(clean_data_df['Value'][row]).lower()
    if category_name != 'nan':
        clean_data_df['Product Attributes / Attributes / External ID'][row] = attr_val_dict[category_name]['category_external_id']
        if attr_name != 'nan':
            clean_data_df['Product Attributes / Values / External ID'][row] = attr_val_dict[category_name][attr_name]

print(clean_data_df.head())    # print(row)

#TODO: strip spaces, replace with underscores

clean_data_df.to_excel(excel_writer = 'output.xlsx')


