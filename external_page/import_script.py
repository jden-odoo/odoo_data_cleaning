from pyparsing import col
import sys
from xmlrpc import client
import pandas as pd
import time

    # 9a4290dfbf1111cf575766b918178600e38f49f6
    #type 1: attribut eseperate colums
    #attribute and vlaue respective columns
    #picture example
    #seperate odoo module
    #ovverride existing

#requires --limit-time-real=100000
#python odoo-bin --addons-path=../enterprise,../,addons -d import-script --log-level warn --limit-time-real=100000
#ir.model.data


class ExternalImport():

        
    def main(self, user, password, db, url, fields, columns, model_name):
        """
        Driver function for the class
        This function is the main function that is called to run the script

        :param string user: the username of the user, typically the email address
        :param string password: an api key provided by the user
        :param string url: the url of the odoo server
        :param string db: the database name
        :param list[string] fields: a list of fields to be imported
        :param list[string]columns: a list of columns.
        :param string model_name: the name of the model to be imported
        :rtype: None

        Whenever possible, we create multiple records with one api call instead of creating one record at a time 
        in order to reduce unnecessary overhead
        This is why the functions that create records, such as 
        create_attribute_records and add_attributes_and_values have helper functions to make api calls

        
        """

        start = time.time()
        common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, user, password, {})
        models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        attr_val_dict = self.create_attr_val_dict(fields, columns)
        database_ids = self.create_attribute_records(db, uid, password, models, attr_val_dict, model_name)
        product_field_information = self.get_field_information(db, uid, password, models, fields, columns)
        if not product_field_information:
            return None
        self.add_attributes_and_values(db, uid, password, models, database_ids, attr_val_dict, product_field_information,fields,columns)

        end = time.time()
        print(end - start)


    def create_attr_val_dict(self,fields,columns):

        """
        Convert attribute/value data to a dictionary

        :param list[string] fields: a list of fields to be imported
        :param list[string]columns: a list of columns corresponding to the fields
        :rtype Dictionary attr_val_dict: nested dictionary of attribute and value names and external ids
        
        There are three layers of dictionarys in attr_val_dict:
        Outermost dictionary has attribute names as keys and dictionaries as values
        The middle layer has two hardcoded keys:
        'attribute_external_id', which is the external id of the attribute
        'values_external_id', which is another dictionary
        The innermost dictionary's keys are the names of the values and the values are the external ids of the values
        
        
        Example 
        Original excel file
        Attribute_Name,Attribute_External_ID,Value_Name,Value_External_ID
        Color of Car Body,car_body_color,White,car_body_white
        ,,Green,car_body_green
        Color of Car Trim,car_trim_color,White,car_trim_white
        ,,Green,car_trim_green
        
        create_attr_val_dict() will return:
        {
            'Color of Car Body', {
                'attribute_external_id': 'car_body_color',
                'values': {
                    'White': 'car_body_white',
                    'Green': 'car_body_green'
                }
            }
            'Color of Car Trim', {
                'attribute_external_id': 'car_trim_color'
                'values': {
                    'White': 'car_trim_white',
                    'Green': 'car_trim_green'
                }
            }
        }
        """

        attr_val_df = pd.read_excel('../data/attr-val.xlsx')

        attr_val_dict = {}
        curr_attribute = None
        
        for row in range(0, len(attr_val_df)):
            if not pd.isna(attr_val_df['name'][row]):            
                curr_attribute = str(attr_val_df['name'][row]).strip()
                attr_val_dict[curr_attribute] = {}
                attr_val_dict[curr_attribute]['attribute_external_id'] = attr_val_df['id'][row]
                attr_val_dict[curr_attribute]['values'] = {}

            curr_val_name = str(attr_val_df['value_ids/name'][row]).strip()
            curr_val_external_id = str(attr_val_df['value_ids/id'][row])
            
            attr_val_dict[curr_attribute]['values'][curr_val_name] = curr_val_external_id

        return attr_val_dict


    def create_attribute_records(self, db, uid, password, models, attr_val_dict, model_name):

        """
        Reads from attribute-value excel file and creates corresponding attribute and value records in the database
        Note that there are hardcoded default values for the fields create_variant and display_type.
        returns a dictionary of database ids to avoid making api calls to search for records
 
        :param string db: name of the database.
        :param int uid: user id for xmlrpc
        :param string password: api key
        :param ServerProxy models: object that makes api calls
        :param Dictionary attr_val_dict: nested dictionary of attribute and value names and external ids
        :rtype Dictionary database_ids: dictionary that maps attribute and value external ids to their database ids.
        """

        CREATE_VARIANT_DEFAULT = 'always' #hardcoded default values as per requirements
        DISPLAY_TYPE_DEFAULT = 'radio'
        VISIBILITY_DEFAULT = 'visibile'
        attribute_id_batch = [] #keeping the batch
        MAX_BATCH_SIZE = 100
        database_ids = {}

        attribute_ordered = [] #storing the attributes for each attribute in the same order as the keys of the dictionary
        for attribute in attr_val_dict.keys():
            if len(attribute_id_batch) >= MAX_BATCH_SIZE:
                self.attribute_batch_calls(self, db, uid, password, models, attribute_id_batch,attr_val_dict,attribute_ordered,database_ids, model_name)
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
            self.attribute_batch_calls(db, uid, password, models, attribute_id_batch,attr_val_dict,attribute_ordered,database_ids, model_name)
        return database_ids

    def get_field_information(self, db, uid, password, models, fields, columns):

        """
        retrieves informations about the fields of a given model from the database. currently hardcoded to product.template
        returns a dictionary that makes it much easiear to create records later

        :param string db: name of the database
        :param int uid: user id for xmlrpc
        :param string password: api key
        :param ServerProxy models: object that makes api calls
        :param list[string] fields: a list of fields to be imported
        :param list[string] columns: a list of columns corresponding to the fields
        :rtype Dictionary product_field_information: nested dictionary mapping column names to information about the corresponding field


        Example for product.template
        
        columns = ['Product Name', 'Company']
        fields = ['name', 'company_id']
        product_field_information = {
            'Product Name': {
                'name': 'name',
                'type': 'char',
            },
            'Company': {
                'name': 'company_id',
                'type': 'many2one',
                'relation': 'res.company',
            }
        }


        """
        
        product_template_fields = models.execute_kw(db, uid, password, 'product.template', 'fields_get', [])
        product_field_information = {}

        for i in range(0, len(columns)):
            columns[i].strip() 
            if columns[i] == 'attribute' or columns[i] == 'value':
                continue
            elif not fields[i]:      
                return None
            else:                    
                curr_col = columns[i]
                product_field_information[curr_col] = {}
                product_field_information[curr_col]['name'] = fields[i]
                field_type = product_template_fields[fields[i]]['type']
                product_field_information[curr_col]['type'] = field_type
                if field_type == 'many2many' or field_type == 'one2many'or field_type == 'many2one':
                    product_field_information[curr_col]['relation'] = product_template_fields[fields[i]]['relation']
        return product_field_information


    def attribute_batch_calls(self, db, uid, password, models, attribute_id_batch,attr_val_dict,attribute_ordered,database_ids,model_name):
        
        """
        makes api calls to create attributes and values in the database

        :param string db: name of the database
        :param int uid: user id for xmlrpc
        :param string password: api key
        :param ServerProxy models: object that makes api calls
        :param List[dict] attribute_id_batch: list of dictionaries representing attribute records
        :param Dictionary attr_val_dict: nested dictionary of attribute and value names and external ids
        :param List[string] attribute_ordered: list of attribute names in the same order as attribute_id_batch
        :param Dictionary database_ids: dictionary that maps attribute and value external ids to their database ids.
        :param string model_name: name of the model to be imported

        """

        attribute_id_numbers = models.execute_kw(db, uid, password, 'product.attribute', 'create', [attribute_id_batch])
        value_batch = []
        MAX_BATCH_SIZE = 100
        val_external_id_list = []

        attribute_model_metadata = []
        for i in range(len(attribute_id_numbers)):
            attribute_id_number = attribute_id_numbers[i]
            attribute = attribute_ordered[i]
            attribute_external_id = attr_val_dict[attribute]['attribute_external_id']
            database_ids[attribute_external_id] = attribute_id_number

            attribute_model_metadata.append({
                'model': 'product.attribute',
                'module': 'base',
                'res_id': attribute_id_number,
                'name': attribute_external_id
            })

            val_dict = attr_val_dict[attribute]['values']
            for val in val_dict.keys():
                if len(value_batch) >= MAX_BATCH_SIZE:
                    self.val_batch_calls(db, uid, password, models, value_batch,attr_val_dict,database_ids,val_external_id_list,model_name)
                    value_batch = []
                    val_external_id_list = []

                value_external_id = val_dict[val]
                val_external_id_list.append(value_external_id)
                value_batch.append({
                    'name': val,
                    'attribute_id': attribute_id_number,
                })

        if len(value_batch) > 0:
            self.val_batch_calls(db, uid, password, models, value_batch,attr_val_dict,database_ids,val_external_id_list,model_name)

        models.execute_kw(db, uid, password, 'ir.model.data', 'create', [attribute_model_metadata])


    def val_batch_calls(self, db, uid, password, models, value_id_batch,attr_val_dict,database_ids,val_extern_id_list, model_name):

        """
        makes api calls to create values in the database

        :param string db: name of the database
        :param int uid: user id for xmlrpc
        :param string password: api key
        :param ServerProxy models: object that makes api calls
        :param List[dict] value_id_batch: list of dictionaries representing value records
        :param Dictionary attr_val_dict: nested dictionary of attribute and value names and external ids
        :param Dictionary database_ids: dictionary that maps attribute and value external ids to their database ids.
        :param string model_name: name of the model to be imported
        
        """
        value_id_numbers = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [value_id_batch])

        value_model_metadata = []

        for i in range(len(value_id_numbers)):
            value_id_number = value_id_numbers[i]
            attribute_id_number = value_id_batch[i]['attribute_id']
            models.execute_kw(db, uid, password, 'product.attribute', 'write', [[attribute_id_number], {
                    'value_ids': [(4, value_id_number, 0)]
                }])
            value_external_id = val_extern_id_list[i]
            database_ids[value_external_id] = value_id_number

            value_model_metadata.append({
                'model': 'product.attribute.value',
                'module': 'base',
                'name': value_external_id,
                'res_id': value_id_number
            })
        
        models.execute_kw(db, uid, password, 'ir.model.data', 'create', [value_model_metadata])


    def add_attributes_and_values(self, db, uid, password, models, database_ids, attr_val_dict, product_field_information,fields,columns):
       
        """
        This function creates new product.template records. It then adds the corresponding attribute lines to those records.
        Input:
        :param string db: name of the database
        :param int uid: user id for xmlrpc 
        :param string password: api key
        :param ServerProxy models: object that makes api calls
        :param Dictionary database_ids: dictionary that maps attribute and value external ids to their database record ids

        """

        output_df = pd.read_csv('../data/outputdata.csv')
        output_df.rename(columns = lambda x: x.strip().lower(), inplace=True)

        parent_model_batch = [] 
        attribute_lines_batch = []
        product_ids = [] 

        BATCH_SIZE = 1000

        curr_product_id = -1

        col_name = None

        # find columns that corresponds to name field
        for i in range(len(fields)):
            if fields[i].lower() == 'name':
                col_name = columns[i].lower()
                break

        for row in range(0, len(output_df)):

            if row % 50 == 0: #status update
                print(row)

            # check if new record needs to be created
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
                            new_product_fields[field_name] = self.find_m2o_record(db, uid, password, models, product_field_information[col]['relation'], field_val)
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

                # curr_product_id is a placeholder that represents an index in parent_model_batch 
                # this index represents a product that the attribute lines will be added to
                
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


    def convert_field_data_type(self, field_type, field_val):

        """
        helper function that casts data in the file to match the field type for basic fields
        this function is only called in add_attributes_and_values

        :param string field_type: type of the field
        :param string field_val: value of the field
        :rtype 
        """

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


    #TODO: remove creation of models, replace with error warning
    def link_field_to_model(self, db, uid, password, models, field_val, comodel):

        """
        helper function to handle one2many and many2many fields
        This will try to match to an existing record by comparing the name from the csv file 
        to the name of the record via case insensitive string match. If no match can be found, then it will 
        create a new record with the name from the csv file.
        This function is only called in add_attributes_and_values.

        :param string db: database name
        :param int uid: user id for xmlrpc
        :param string password: api key
        :param string field_val: value of the cell in the csv file
        :param string comodel: Name of the comodel for the field. This the model that the funcion will search for/create.
        :rtype (int, int, int): A tuple that represents a link command. It will be of the form (4, model_id, 0). 
        """

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


    def batch_create_calls(self, db, uid, password, models, parent_model_batch, attribute_lines_batch):

        """
        Helper function to make create api calls. Implements batching to improve runtime.
        This function is only called in add_attributes_and_values.

        :param string db: database name
        :param int uid: user id for xmlrpc
        :param string password: api key
        :param ServerProxy models: object for making xmlrpc calls
        :param list[Dictionary] parent_model_batch: each dictionary represents a record of the given model e.g. product.template
        :param list[Dictionary] attribute_lines_batch: each dictionary represents a record of the attribute.line model
        :param list[int] product_ids: list of database ids of records of the given model
        :param list[Dictionary] attribute_lines_batch: each dictionary represents a record of product.attribute.line.

        """
        product_db_ids = models.execute_kw(db, uid, password, 'product.template', 'create', [parent_model_batch])
        for attr_line in attribute_lines_batch:
            attr_line['product_tmpl_id'] = product_db_ids[attr_line['product_tmpl_id']]
        attribute_lines_ids = models.execute_kw(db, uid, password, 'product.template.attribute.line', 'create', [attribute_lines_batch])


    #TODO: raise error instead of creating new model
    def find_m2o_record(self, db, uid, password, models, relation, field_val):

        """
        helper function to find the database id of a record that is linked to a m2o field

        :param string db: database name
        :param int uid: user id for xmlrpc
        :param string password: api key
        :param ServerProxy models: object for making xmlrpc calls
        :param Dictionary product_field_information: field information for the model
        :param string relation: name of the comodel that the field is linked to
        :rtype int: database id of the record
        """

        record_id = models.execute_kw(db, uid, password, relation, 'search_read', [[['name', '=', field_val]]])
        if len(record_id) > 0:
            return record_id[0]['id']
        else:
            return models.execute_kw(db, uid, password, relation, 'create', [{
                'name': field_val
            }])
    

