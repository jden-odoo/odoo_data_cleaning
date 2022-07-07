import pandas as pd

#############################################################################
#Input: 1: 'data/attr-val.csv' i.e. output from dirty_to_attribute_values.py
#       2: 'data/outputdata.csv' i.e. output from dirty_to_clean.py


#Output: final_output.xlsx, which is a spreadsheet ready for import into Odoo
#############################################################################

def main():
    attr_val_dict = create_attr_val_dict()
    final_data_df = add_attr_to_clean(attr_val_dict)
    final_data_df.to_excel(excel_writer = 'final_output.xlsx')


def create_attr_val_dict():

    #Convert attribute/value data to a dictionary

    #Create df for attribute/value excel file
    # attr_val_df = pd.read_csv('attr-val.csv')
    #attr_val_df = pd.read_excel('data/attr-val.xlsx')
    attr_val_df = pd.read_csv('data/attr-val.csv')


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

    
    clean_data_df = pd.read_csv('data/outputdata.csv')
    clean_data_df.replace(' ', '_', regex=True)
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

    return clean_data_df  



main()


