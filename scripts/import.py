from xmlrpc import client
import pandas as pd
import sys
import time


########################################
# This script requires the sale module
#
# Main driver function for this script. 
# Inputs:
# 1. url: This is the url for the database to import into.
# 2. db: This is the name of the database that will be accessed.
# 3. user: This is the username that will be used to access the database.
# 4. password: This is the api key that will be used to access the database.
# This function does not have an output.
#
# Example command to run script
# python import.py http://localhost:8069 import-script admin 5326200ebea7bdb285c6b25023fe67f16200ba75
########################################
def main():   
    #TODO: take url, user, db and pass as user inputs
    # url = sys.argv[1]
    # db = sys.argv[2]
    # user = sys.argv[3]
    # password = sys.argv[4]

    #hardcoded dev values
    url = 'http://localhost:8069'
    db = 'import-script'
    user = 'admin'
    password = '71d3fa29599d1a9c43a01db2a69c389a30a18f1c'


    common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, user, password, {})
    models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    attr_val_dict = create_attr_val_dict()
    database_ids = create_attribute_records(db, uid, password, models, attr_val_dict)
    add_attributes_and_values(db, uid, password, models, database_ids, attr_val_dict)

    
##################################################
# Reads from attribute-value excel file and creates corresponding attribute and value records in the database
# Note that there are hardcoded default values for the fields create_variant and display_type.
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
        
        attribute_id_number = models.execute_kw(db, uid, password, 'product.attribute', 'create', [{
            'name': attribute,
            'create_variant': CREATE_VARIANT_DEFAULT,
            'display_type': DISPLAY_TYPE_DEFAULT,
        }]) 

        attribute_external_id = attr_val_dict[attribute]['attribute_external_id']
        # models.execute_kw(db, uid, password, 'ir.model.data', 'unlink',[[attribute_id_number]] )
        # models.execute_kw(db, uid, password, 'ir.model.data', 'create', [{
        #     'name': attribute_external_id,
        #     'model': 'product.attribute',
        #     'module': 'base'
        # }])
        # print(models.execute_kw(db, uid, password, 'product.attribute', 'get_metadata', [[attribute_id_number]]))

        # TODO: no visibility field in model?
        database_ids[attribute_external_id] = attribute_id_number
        
        val_dict = attr_val_dict[attribute]['values']
        for val in val_dict.keys():
            value_external_id = val_dict[val]
            value_id_number = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [{
                'name': val,
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

    attr_val_df = pd.read_excel('../data/attr-val.xlsx')

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

def add_attributes_and_values(db, uid, password, models, database_ids,attr_val_dict):
    output_df = pd.read_csv('../data/modified_outputdata.csv')
    output_df.rename(columns = lambda x: x.strip(), inplace=True)

    product_template_fields = models.execute_kw(db, uid, password, 'product.template', 'fields_get', [])

    product_field_information = {}


    for col in output_df.columns:
        if col == "Attribute" or col == "Value":
            continue
        field_string = None
        field_data_type = None
        field_name = None
        field_comodel = None
        for field in product_template_fields.keys():
            if product_template_fields[field]['string'] == col:
                field_string = product_template_fields[field]['string']
                field_data_type = product_template_fields[field]['type']
                if field_data_type == 'many2many' or field_data_type == 'one2many':
                    field_comodel = product_template_fields[field]['relation']
                field_name = field
                break
        if field_string:
            product_field_information[field_string] = {}
            product_field_information[field_string]['name'] = field_name
            product_field_information[field_string]['type'] = field_data_type
            if field_comodel:
                product_field_information[field_string]['relation'] = field_comodel
                field_comodel = None
        else:
            print("Error: field not matched")
            print(field_name)
            

    parent_model_batch = [] 
    attribute_lines_batch = []
    product_ids = [] 

    BATCH_SIZE = 100

    curr_product_id = -1
    for row in range(0, len(output_df)):  
        #TODO: implement duplicate checking
        if row % 50 == 0:
            print(row)

        if not pd.isna(output_df['Name'][row]):
            new_product_fields = {} 
            new_product_attr_vals = {}
            curr_product_id += 1
            
            for col in output_df.columns:
                if len(parent_model_batch) > BATCH_SIZE:
                    batch_create_calls(db, uid, password, models, parent_model_batch, attribute_lines_batch)
                    parent_model_batch = []
                    product_ids = []
                    attribute_lines_batch = []
                    curr_product_id = -1
                
                if col != "Value" and col != "Attribute":
                    field_name = product_field_information[col]['name']
                    field_type = product_field_information[col]['type']
                    field_val = output_df[col][row]
                    if field_type != 'many2many' and field_type != 'one2many':
                        new_product_fields[field_name] = convert_field_data_type(field_type, field_val)
                    else:
                        if field_name in new_product_fields:
                            new_product_fields[field_name].append(link_field_to_model(db, uid, password, models, field_val, product_field_information[col]['relation']))                    
                        else:
                            new_product_fields[field_name] = [link_field_to_model(db, uid, password, models, field_val, product_field_information[col]['relation'])]
            #curr_product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [new_product_fields])
            parent_model_batch.append(new_product_fields)
                

        attribute_external_id = output_df['Attribute'][row]
        if not pd.isna(attribute_external_id) and curr_product_id != -1:
            
            attribute_id_number = database_ids[attribute_external_id]

            value_external_ids_list = output_df["Value"][row].split(',')

            for val in range(0, len(value_external_ids_list)):
                value_external_ids_list[val] = (4, database_ids[value_external_ids_list[val]], 0)

            attribute_lines_batch.append({
                'product_tmpl_id': curr_product_id,
                'attribute_id': attribute_id_number,
                'value_ids': value_external_ids_list
            })

            product_ids.append(curr_product_id)
            
            # new_attribute_line_id = models.execute_kw(db, uid, password, 'product.template.attribute.line', 'create', [{
            #     'product_tmpl_id': curr_product_id,
            #     'attribute_id': attribute_id_number,
            #     'value_ids': value_external_ids_list
            # }])

            # models.execute_kw(db, uid, password, 'product.template', 'write', [[curr_product_id], {
            #     'attribute_line_ids':[(4, new_attribute_line_id, 0)]
            # }])
        
        #TODO: remove for dev
        

        
##################################################
# Helper function that casts data to match odoo field data types
# Only called in add_attributes_and_values
# Does not handle many2many or one2many fields. That is handled in link_field_to_model
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
    elif field_type == 'boolean':
        return str(field_val).lower() == 'true'
    else:
        return str(field_val)
    #TODO: add more cases for different field types


##################################################
# Helper function to handle one2many and many2many fields
# This will try to match to an existing record by comparing the name from the csv file 
# to the name of the record via case insensitive string match. If no match can be found, then it will 
# create a new record with the name from the csv file.
# This function is only called in add_attributes_and_values.
# Input:
# 1. db: See main for documentation.
# 2. uid: See main for documentation.
# 3. password: See main for documentation.
# 4. field_val: Value of the cell in the csv file. 
# 5. comodel: Name of the comodel for the field. This the model that the funcion will search for/create.
# Output:
# 1. A tuple that represents a link command. It will be of the form (4, model_id, 0). This will then be appended into the fields.
###################################################

def link_field_to_model(db, uid, password, models, field_val, comodel):
    existing_model_records = models.execute(db, uid, password, comodel, 'search_read')
    record_match = None
    for record in existing_model_records:
        if record['name'].lower() == str(field_val).lower():
            record_match = record['id']
            break
    if record_match:
        return (4, record_match, 0)
    else:
        new_record = models.execute_kw(db, uid, password, comodel, 'create', {
            'name': field_val
        })
        return (4, new_record, 0)




# [{
#     f1: fv1,
#     f2: fv2
# },
# {
#     f1: fv1,
#     f2: fv2,
#     f3: fv3,
# }]


#######################################################
# Helper function to make create api calls. Implements batching to improve runtime.
# Input:
# 1. db: See main for documentation.
# 2. uid: db. See main for documentation.
# 3. password: See main for documentation.
# 4. models: See main for documentation.
# 5. parent_model_batch: a list of dictionaries. Each dictionary is turned into a record of the given model i.e. product.template
# The keys in the dictionary are the field technical names,
# and the values in the dictionary are the values of the corresponding fields. 
# 6. product_ids: a list of integers representing database ids of records of the given model.
# 7. attribute_lines_batch: a list of dictionaries. Each dictionary is turned into a record of product.attribute.line.
# Each key in the dictionary is a field in product.attribute.line, and it's value is the fields corresponding value.
# Output: this function has no output
#
# 
# attribute_lines_batch and product_ids must be the same length and must correspond. In other words, the attribute line
# represented by the dictionary at index i in attribute_lines_batch is related to the product.template record who's id
# is in index i in product_ids. After creating the records from attribute_lines_batch, a list of database ids of 
# attribute.line records will be returned in the same order. Each value in this list will then be linked to it's corresponding
# product.template record.
#######################################################

def batch_create_calls(db, uid, password, models, parent_model_batch, attribute_lines_batch):
            
    product_db_ids = models.execute_kw(db, uid, password, 'product.template', 'create', [parent_model_batch])
    for attr_line in attribute_lines_batch:
        attr_line['product_tmpl_id'] = product_db_ids[attr_line['product_tmpl_id']]
        print(attr_line['product_tmpl_id'])
    attribute_lines_ids = models.execute_kw(db, uid, password, 'product.template.attribute.line', 'create', [attribute_lines_batch])


    # curr_product_id = product_ids[0]
    # curr_product_attribute_line_commands = []
    # for index in range(0, len(product_ids)):
    #     if product_ids[index] != curr_product_id or index == len(product_ids) - 1:
    #         if len(curr_product_attribute_line_commands) > 0:
    #             models.execute_kw(db, uid, password, 'product.template', 'write', [[product_db_ids[product_ids[index]]], {
    #                 'attribute_line_ids': curr_product_attribute_line_commands
    #             }])
    #         curr_product_attribute_line_commands = [(4, attribute_lines_ids[index], 0)]
    #         curr_product_id = product_ids[index]
    #     else:
    #         curr_product_attribute_line_commands.append((4, attribute_lines_ids[index], 0))




start = time.time()
main()
end = time.time()
print(end - start)


#TODO
#importable fields => readonly = false
#ui to match fields
#handle onetomany, many2many columns
#field matching, Product Type matched to Type in product.template
#ask about line 3 in modified
#create_multi
#unhardcode product.template, allow for input 
#change hardcoded file paths
#attribute names/ not ids todo
#ui, match fields
#dont create new comodels, unknown all required fields. maybe ui?




#old testing databases and api keys

# db = 'import-script'
# password = 'ed714c2c397f4b0164f4cb0a47f82f77fa6753f9'

# db = 'import-script-2'
# password = '28fd30a96fb33ccde4f83fb8892260adc851b0c6'

# db = 'import-script-3'
# password = '915ffe176dad011adf22e038a7b3f6d4188d6d9f'

# db = 'import-script-4'
# password = '736bea35eed6cca1f4959e469f9c68039ea39703'

# db = 'import-script-6'
# password = 'daaf39788bc1ff76faf6e2a7b7e4551ebdaa21e3'