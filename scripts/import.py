from xmlrpc import client
import pandas as pd
import sys
import threading


def main():   
    #TODO: take url, user, db and pass as user inputs
    url = 'http://localhost:8069'
    user = 'admin'

    db = 'import-script-6'
    password = 'daaf39788bc1ff76faf6e2a7b7e4551ebdaa21e3'

    common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, user, password, {})
    models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    attr_val_dict = create_attr_val_dict()
    database_ids = create_attribute_records(db, uid, password, models, attr_val_dict)

    t1 = threading.Thread(target=add_attributes_and_values(db, uid, password, models, database_ids))
    t2 = threading.Thread(target=add_attributes_and_values(db, uid, password, models, database_ids))
    t3 = threading.Thread(target=add_attributes_and_values(db, uid, password, models, database_ids))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
    

##################################################
# Reads from attribute-value excel file and creates corresponding attribute and value records in the database
# Input: 
# 1. db: This is the name of the database as a string.This is passed in from the command line via main.
# 2. uid: This is the user id, which is needed to make api calls. This is passed in from main.
# 3. password: This is the api key that allows you to access the database. This is passed in from the command line via main.
# 4. models: This is the object that allows us to make api calls. This is created and passed in from main.
# 5. attr_val_dict: This is nested dictionary that maps attributes and values to their external ids. This is the output from create-attr_val_dict.
# Output:
# 1. database_ids: This is a dictionary that maps attribute and value external ids to their database ids.
##################################################
def create_attribute_records(db, uid, password, models, attr_val_dict):

    CREATE_VARIANT_DEFAULT = 'always'
    DISPLAY_TYPE_DEFAULT = 'radio'
    VISIBILITY_DEFAULT = 'visibile'

    database_ids = {}
    #TODO: implement duplicate checking

    for attribute in attr_val_dict.keys():
        attribute_external_id = attr_val_dict[attribute]['attribute_external_id']
        attribute_id_number = models.execute_kw(db, uid, password, 'product.attribute', 'create', [{
            'name': attribute_external_id,
            'display_name': attribute,
            'create_variant': CREATE_VARIANT_DEFAULT,
            'display_type': DISPLAY_TYPE_DEFAULT,
        }]) 
        # TODO: no visibility field in model?
        database_ids[attribute_external_id] = attribute_id_number
        
        val_dict = attr_val_dict[attribute]['values']
        for val in val_dict.keys():
            value_external_id = val_dict[val]
            value_id_number = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [{
                'name': value_external_id,
                'attribute_id': attribute_id_number,
            }])
            models.execute_kw(db, uid, password, 'product.attribute', 'write', [[attribute_id_number], {
                'value_ids': [(4, value_id_number, 0)]
            }])
            database_ids[value_external_id] = value_id_number
    
    return database_ids


#############################################
# Convert attribute/value data to a dictionary
# Input: None. The name of the file to be opened is hard coded.
# Output: Nested dictionary, where outer key is attribute name and inner key is value name.
# The outer key corresponds to a diciontary with two values inside it
# 1. 'Attribute-external-id', which is the attributes external id as a string.
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
#         'attribute_external_id': 'car_body_color',
#         'values': {
#             'white': 'car_body_white',
#             'green': 'car_body_green'
#         }
#     }
#     'color_of_car_trim', {
#         'attribute_external_id': 'car_trim_color'
#         'values': {
#             'white': 'car_trim_white',
#             'green': 'car_trim_green'
#         }
#     }
# }
##################################################

def create_attr_val_dict():

    attr_val_df = pd.read_excel(sys.argv[1])

    attr_val_dict = {}
    curr_attribute = None

    for row in range(0, len(attr_val_df)):
        if not pd.isna(attr_val_df['name'][row]):            
            curr_attribute = str(attr_val_df['name'][row]).replace(' ','_').lower()
            attr_val_dict[curr_attribute] = {}
            attr_val_dict[curr_attribute]['attribute_external_id'] = attr_val_df['id'][row]
            attr_val_dict[curr_attribute]['values'] = {}

        curr_val_name = str(attr_val_df['value_ids/name'][row]).replace(' ', '_').lower()
        curr_val_external_id = str(attr_val_df['value_ids/id'][row])
        
        attr_val_dict[curr_attribute]['values'][curr_val_name] = curr_val_external_id

    return attr_val_dict


############################################################
# This function creates new product.template records. It then adds the corresponding attribute lines to those records.
# Input:
# 1. db: This is the name of the database as a string.This is passed in from the command line via main.
# 2. uid: This is the user id, which is needed to make api calls. This is passed in from main.
# 3. password: This is the api key that allows you to access the database. This is passed in from the command line via main.
# 4. models: This is the object that allows us to make api calls. This is created and passed in from main.
# 5. database_ids: This is a dictionary that maps attribute and value external ids to their database ids. This is the output from create_attribute_records.
# Output: none
#
# When creating the product.template records, there must be a field with a description that exactly matches the column 
# names except for white space before and after the column name. For example, " Name " will match with the name field, but 
# "name" will not. If a matching field cannot be found for a column, an error message will be printed and the function will ignore
# that column.
#
############################################################

def add_attributes_and_values(db, uid, password, models, database_ids):
    #output_df = pd.read_csv('../data/modified-outputdata.csv')
    #changed one column name
    output_df = pd.read_csv(sys.argv[2])
    output_df.rename(columns = lambda x: x.strip(), inplace=True)

    product_template_fields = models.execute_kw(db, uid, password, 'product.template', 'fields_get', [])
    product_field_information = {}

    for col in output_df.columns:
        if col == "Attribute" or col == "Value":
            continue
        field_string = None
        field_data_type = None
        field_name = None
        for field in product_template_fields.keys():
            if product_template_fields[field]['string'] == col:
                field_string = product_template_fields[field]['string']
                field_data_type = product_template_fields[field]['type']
                field_name = field
                break
        if field_string:
            product_field_information[field_string] = {}
            product_field_information[field_string]['name'] = field_name
            product_field_information[field_string]['type'] = field_data_type
        else:
            print("Error: field not matched")
            

    curr_product_id = None
    for row in range(0, len(output_df) - 1):  
        #TODO: implement duplicate checking
        if row % 1000 == 0:
            print(row)

        if not pd.isna(output_df['Name'][row]):
            new_product_fields = {} #ASSUMES COLUMNS ALL HAVE CORRESPONDING FIELDS AND NONE OF THE FIELDS ARE ONE2MANY/MANY2MANY
            new_product_attr_vals = {}


            for col in output_df.columns:
                if col != "Value" and col != "Attribute":
                    field_name = product_field_information[col]['name']
                    new_product_fields[field_name] = convert_field_data_type(product_field_information[col]['type'], output_df[col][row])
            curr_product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [new_product_fields])

        if curr_product_id:
            attribute_external_id = output_df['Attribute'][row]
            attribute_id_number = database_ids[attribute_external_id]

            value_external_id = output_df["Value"][row]
            value_id_number = database_ids[value_external_id]
            
            new_attribute_line_id = models.execute_kw(db, uid, password, 'product.template.attribute.line', 'create', [{
                'product_tmpl_id': curr_product_id,
                'attribute_id': attribute_id_number,
                'value_ids': [(4, value_id_number, 0)]
            }])

            models.execute_kw(db, uid, password, 'product.template', 'write', [[curr_product_id], {
                'attribute_line_ids':[(4, new_attribute_line_id, 0)]
            }])

        
##################################################
# Helper function that casts data to match odoo field data types
# Only called in add_attributes_and_values
# Input:
# 1. field_type, which is the type of data the odoo field takes as a string
# 2. data, which is read from the csv file 
# Output: the data case into the data type.
# If data type is float, monetary, or integer and the data cannot be parsed into a number, returns 0
# returns the data as a string by default
##################################################

def convert_field_data_type(field_type, field_val):
    if field_type == 'integer':
        try:
            return int(field_val.replace(' $',''))
        except:
            return 0  
    elif field_type == 'monetary' or field_type =='float':
        try:
            return float(field_val.replace(' $',''))
        except:
            return 0.0
    else:
        return str(field_val)
    #TODO: add more cases for different field types

main()


#old testing databases and api keys

# db = 'import-script'
# password = 'ed714c2c397f4b0164f4cb0a47f82f77fa6753f9'

# db = 'import-script-2'
# password = '28fd30a96fb33ccde4f83fb8892260adc851b0c6'

# db = 'import-script-3'
# password = '915ffe176dad011adf22e038a7b3f6d4188d6d9f'

# db = 'import-script-4'
# password = '736bea35eed6cca1f4959e469f9c68039ea39703'