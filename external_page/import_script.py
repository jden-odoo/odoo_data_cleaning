from pyparsing import col
import sys
from xmlrpc import client
import pandas as pd
import time


#requires --limit-time-real=100000
#python odoo-bin --addons-path=../enterprise,../,addons -d import-script --log-level warn --limit-time-real=100000

class ExternalImport():
        
    def main(self, user, password, db, url, fields, columns):

        start = time.time()
        common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, user, password, {})
        models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        attr_val_dict = self.create_attr_val_dict(fields, columns)
        database_ids = self.create_attribute_records(db, uid, password, models, attr_val_dict)
        product_field_information = self.get_field_information(db, uid, password, models, fields, columns)
        keys = list(product_field_information.keys())
        for i in range(0, 5):
            print(keys[i], product_field_information[keys[i]])
        self.add_attributes_and_values(db, uid, password, models, database_ids, attr_val_dict, product_field_information,fields,columns)

        end = time.time()
        print(end - start)

        
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
    # def create_attribute_records(self, db, uid, password, models, attr_val_dict):

    #     CREATE_VARIANT_DEFAULT = 'always'
    #     DISPLAY_TYPE_DEFAULT = 'radio'
    #     VISIBILITY_DEFAULT = 'visibile'

    #     database_ids = {}
    #     #TODO: implement duplicate checking

    #     for attribute in attr_val_dict.keys():
            
    #         attribute_id_number = models.execute_kw(db, uid, password, 'product.attribute', 'create', [{
    #             'name': attribute,
    #             'create_variant': CREATE_VARIANT_DEFAULT,
    #             'display_type': DISPLAY_TYPE_DEFAULT,
    #         }]) 

    #         attribute_external_id = attr_val_dict[attribute]['attribute_external_id']

    #         # TODO: no visibility field in model?
    #         database_ids[attribute_external_id] = attribute_id_number
            
    #         val_dict = attr_val_dict[attribute]['values']
    #         for val in val_dict.keys():
    #             value_external_id = val_dict[val]
    #             value_id_number = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [{
    #                 'name': val,
    #                 'attribute_id': attribute_id_number,
    #             }])
    #             models.execute_kw(db, uid, password, 'product.attribute', 'write', [[attribute_id_number], {
    #                 'value_ids': [(4, value_id_number, 0)]
    #             }])
    #             database_ids[value_external_id] = value_id_number
        
    #     return database_ids

    def create_attribute_records(self, db, uid, password, models, attr_val_dict):

        CREATE_VARIANT_DEFAULT = 'always'
        DISPLAY_TYPE_DEFAULT = 'radio'
        VISIBILITY_DEFAULT = 'visibile'
        attribute_id_batch = [] #keeping the batch
        MAX_BATCH_SIZE = 100
        database_ids = {}
        #TODO: implement duplicate checking
        attribute_ordered = [] #storing the attributes for each attribute in the same order as the keys of the dictionary
        for attribute in attr_val_dict.keys():
            if len(attribute_id_batch) >= MAX_BATCH_SIZE:
                self.attribute_batch_calls(self, db, uid, password, models, attribute_id_batch,attr_val_dict,attribute_ordered,database_ids)
                attribute_id_batch = []
                attribute_ordered = []

            #list of dictionary ids
            attribute_id_batch.append({
                'name': attribute,
                'create_variant': CREATE_VARIANT_DEFAULT,
                'display_type': DISPLAY_TYPE_DEFAULT,
            })


            attribute_ordered.append(attribute)

        if len(attribute_id_batch) > 0:
            self.attribute_batch_calls(db, uid, password, models, attribute_id_batch,attr_val_dict,attribute_ordered,database_ids)
        return database_ids


    # def attribute_batch_calls(self, db, uid, password, models, attribute_id_batch,attr_val_dict,attribute_ordered,database_ids):
    #     attribute_id_numbers = models.execute_kw(db, uid, password, 'product.attribute', 'create', [attribute_id_batch])
    #     for i in range(len(attribute_id_numbers)):
    #         attribute_id_number = attribute_id_numbers[i]
    #         attribute = attribute_ordered[i]
    #         attribute_external_id = attr_val_dict[attribute]['attribute_external_id']
    #         database_ids[attribute_external_id] = attribute_id_number

    #         val_dict = attr_val_dict[attribute]['values']
    #         for val in val_dict.keys():
    #             value_external_id = val_dict[val]
    #             value_id_number = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [{
    #                 'name': val,
    #                 'attribute_id': attribute_id_number,
    #             }])
    #             models.execute_kw(db, uid, password, 'product.attribute', 'write', [[attribute_id_number], {
    #                 'value_ids': [(4, value_id_number, 0)]
    #             }])
    #             database_ids[value_external_id] = value_id_number
    def attribute_batch_calls(self, db, uid, password, models, attribute_id_batch,attr_val_dict,attribute_ordered,database_ids):
        attribute_id_numbers = models.execute_kw(db, uid, password, 'product.attribute', 'create', [attribute_id_batch])
        value_batch = []
        MAX_BATCH_SIZE = 100
        val_external_id_list = []

        for i in range(len(attribute_id_numbers)):
            attribute_id_number = attribute_id_numbers[i]
            attribute = attribute_ordered[i]
            attribute_external_id = attr_val_dict[attribute]['attribute_external_id']
            database_ids[attribute_external_id] = attribute_id_number


            val_dict = attr_val_dict[attribute]['values']
            for val in val_dict.keys():
                if len(value_batch) >= MAX_BATCH_SIZE:
                    self.val_batch_calls(db, uid, password, models, value_batch,attr_val_dict,database_ids,val_external_id_list)
                    value_batch = []
                    val_external_id_list = []

                value_external_id = val_dict[val]
                val_external_id_list.append(value_external_id)
                value_batch.append({
                    'name': val,
                    'attribute_id': attribute_id_number,
                })
                # value_id_number = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [{
                #     'name': val,
                #     'attribute_id': attribute_id_number,
                # }])
                # models.execute_kw(db, uid, password, 'product.attribute', 'write', [[attribute_id_number], {
                #     'value_ids': [(4, value_id_number, 0)]
                # }])
                # database_ids[value_external_id] = value_id_number
        if len(value_batch) > 0:
            self.val_batch_calls(db, uid, password, models, value_batch,attr_val_dict,database_ids,val_external_id_list)

    def val_batch_calls(self, db, uid, password, models, value_id_batch,attr_val_dict,database_ids,val_extern_id_list):
        value_id_numbers = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [value_id_batch])
        for i in range(len(value_id_numbers)):
            value_id_number = value_id_numbers[i]
            attribute_id_number = value_id_batch[i]['attribute_id']
            models.execute_kw(db, uid, password, 'product.attribute', 'write', [[attribute_id_number], {
                    'value_ids': [(4, value_id_number, 0)]
                }])
            value_external_id = val_extern_id_list[i]
            database_ids[value_external_id] = value_id_number




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

    def create_attr_val_dict(self,fields,columns):

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

    def add_attributes_and_values(self, db, uid, password, models, database_ids, attr_val_dict, product_field_information,fields,columns):
        output_df = pd.read_csv('../data/outputdata.csv')
        output_df.rename(columns = lambda x: x.strip().lower(), inplace=True)

        parent_model_batch = [] 
        attribute_lines_batch = []
        product_ids = [] 

        BATCH_SIZE = 1000

        curr_product_id = -1

        col_name = None
        for i in range(len(fields)):
            if fields[i].lower() == 'name':
                col_name = columns[i].lower()
                break
        for row in range(0, len(output_df)):
            #TODO: implement duplicate checking
            if row % 50 == 0:
                print(row)

            if not pd.isna(output_df[col_name][row]):
                if len(parent_model_batch) > BATCH_SIZE:
                        self.batch_create_calls(db, uid, password, models, parent_model_batch, attribute_lines_batch)
                        parent_model_batch = []
                        product_ids = []
                        attribute_lines_batch = []
                        curr_product_id = -1
                
                new_product_fields = {} 
                new_product_attr_vals = {}
                curr_product_id += 1
                
                for col in output_df.columns:      
                    if col != "value" and col != "attribute":
                        col = col.lower()
                        field_name = product_field_information[col]['name']
                        field_type = product_field_information[col]['type']
                        field_val = output_df[col][row]
                        if field_type == 'many2one':
                            new_product_fields[field_name] = self.find_m2o_record(db, uid, password, models, product_field_information, col, field_val)
                        elif field_type != 'many2many' and field_type != 'one2many':
                            new_product_fields[field_name] = self.convert_field_data_type(field_type, field_val)
                        else:
                            if field_name in new_product_fields:
                                new_product_fields[field_name].append(self.link_field_to_model(db, uid, password, models, field_val, product_field_information[col]['relation']))                    
                            else:
                                new_product_fields[field_name] = [self.link_field_to_model(db, uid, password, models, field_val, product_field_information[col]['relation'])]
                parent_model_batch.append(new_product_fields)
                    

            attribute_external_id = output_df['attribute'][row]
            if not pd.isna(attribute_external_id) and curr_product_id != -1:
                
                attribute_id_number = database_ids[attribute_external_id]

                value_external_ids_list = output_df["value"][row].split(',')

                for val in range(0, len(value_external_ids_list)):
                    value_external_ids_list[val] = (4, database_ids[value_external_ids_list[val]], 0)

                attribute_lines_batch.append({
                    'product_tmpl_id': curr_product_id,
                    'attribute_id': attribute_id_number,
                    'value_ids': value_external_ids_list
                })

                product_ids.append(curr_product_id)

        if len(parent_model_batch) > 0:
            self.batch_create_calls(db, uid, password, models, parent_model_batch, attribute_lines_batch)
            parent_model_batch = []
            product_ids = []
            attribute_lines_batch = []
            curr_product_id = -1

            

            
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

    def convert_field_data_type(self, field_type, field_val):
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

    def link_field_to_model(self, db, uid, password, models, field_val, comodel):
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
    # The 'product_tmpl_id' in the attr_line objects are not actual database ids. They are placeholders that represent the index in 
    # product_db_ids that contains the database id that represents the corresponding product.template attribute.
    #######################################################

    def batch_create_calls(self, db, uid, password, models, parent_model_batch, attribute_lines_batch):
        product_db_ids = models.execute_kw(db, uid, password, 'product.template', 'create', [parent_model_batch])
        for attr_line in attribute_lines_batch:
            attr_line['product_tmpl_id'] = product_db_ids[attr_line['product_tmpl_id']]
        attribute_lines_ids = models.execute_kw(db, uid, password, 'product.template.attribute.line', 'create', [attribute_lines_batch])



    def get_field_information(self, db, uid, password, models, fields, columns):

        product_template_fields = models.execute_kw(db, uid, password, 'product.template', 'fields_get', [])
        product_field_information = {}

        for i in range(0, len(columns)):
            columns[i].strip() 
            print(columns[i])
            if columns[i] == 'attribute' or columns[i] == 'value':
                    continue
            elif not fields[i]:      
                print('Error: field could not be matched')
                #TODO: how to handle mismatch columns?
            else:                    
                curr_col = columns[i]
                product_field_information[curr_col] = {}
                product_field_information[curr_col]['name'] = fields[i]
                field_type = product_template_fields[fields[i]]['type']
                product_field_information[curr_col]['type'] = field_type
                if field_type == 'many2many' or field_type == 'one2many'or field_type == 'many2one':
                    product_field_information[curr_col]['relation'] = product_template_fields[fields[i]]['relation']
        return product_field_information

    def find_m2o_record(self, db, uid, password, models, product_field_information, col, field_val):
        record_id = models.execute_kw(db, uid, password, product_field_information[col]['relation'], 'search_read', [[['name', '=', field_val]]])
        if len(record_id) > 0:
            return record_id[0]['id']
        else:
            return models.execute_kw(db, uid, password, product_field_information[col]['relation'], 'create', [{
                'name': field_val
            }])



    #TODO
    #importable fields => readonly = false
    #ui to match fields
    #dont create new comodels, unknown all required fields. maybe ui?
    #check for required fields

    #TODO for leo
    #unhardcode product.template, allow for model input
    #fix batching error end of loop
    #implement batching for attributes and values 
    #add external ids to attribute and value records
    #unhardcode file paths
    

    #7/20
    #missing end of batch
    
    

