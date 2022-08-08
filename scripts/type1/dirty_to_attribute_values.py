#############################################################################################
#Usage: python3 dirty_to_attribute_values.py dirtydata.csv attributes    
#Input (Space separated): 
#   1. Dirtydata.csv
#   2. column letters for attributes

#Output: attr-val.xlsx
#Sample Input: python3 dirty_to_attribute_values.py dirtydata.csv b,c,e,f,g,h,i,j,k companyname yard


import pandas as pd
# import sys

class DirtyToAttributeValues():
    # Default values
    display_type = "Radio"
    create_variant = "Instantly"
    visibility = "Visible"


    def get_dirty_data(self, dirtydata):
        """Returns dirty data csv into a dataframe.

        :param str dirtydata: String of file name 
        """

        return pd.read_csv(dirtydata)


    def list_all_columns(self, dirty_data):
        """Returns list of all columns in the dirty data dataframe.
        
        :param df dirty_data: Dataframe of dirty data
        :return: List of all columns
        :rtype: list
        """

        return dirty_data.columns


    def get_attribute_names(self, input_array, all_columns):
        """Get column name of all_columns in specified input_array.
        
        :param list input_array: All indexes of attributes
        :param list all_columns: List of all colummns in a dataframe
        :return: All column names of a list of columns
        :rtype: list
        """

        array = []
        print('input_array: ', input_array)
        print('all_columns: ', all_columns)
        for value in input_array:
            value = ord(value.lower())-97
            array.append(all_columns[value])
        print('array: ', array)
        return array


    def get_external_ids(self, name_list):
        """Creates external IDs for all names.
        
        :param list name_list: List of all names
        :return: List of all external IDs
        :rtype: list
        """
        ids_list = []
        for cell in name_list:
            if cell in ids_list and cell != " ":
                ids_list.append(" ")
            else:
                ids_list.append("attribute" + "_" + cell.lower())
        return ids_list


    def get_value_id_name(self, column_name, dirty_data):
        """Creates value_id/name.
        
        :param str column_name: Name of a column in dirty_data
        :param df dirty_data: Dirty data dataframe
        :return: List of value_id/names for a given column_name
        :rtype: list
        """

        value_id_names = []
        for value in dirty_data[column_name].tolist():
            if value not in value_id_names:
                value_id_names.append(value)
        return value_id_names


    def create_excel(self, df):
        """Converts dataframe into a excel file.
        
        :param df df: Dataframe to convert
        """
        df.to_excel(excel_writer = '../data/attr-val.xlsx')


    # Create the data to be added to the new dataframe for the output csv
    # Creates value_id/id
    # Appends values into the data and returns a dataframe with data
    def create(self, input_array, dirtydata):
        #creates dirty data dataframe
        dirty_data = self.get_dirty_data(dirtydata)
        #all columns of the dirty_data dataframe
        all_columns = self.list_all_columns(dirty_data)
        #get all attribute names from all_columns
        attribute_names = self.get_attribute_names(input_array, all_columns)
        #create ids from names_list
        external_ids = self.get_external_ids(attribute_names)
        data = []
        count = 0
        for name in attribute_names:
            value_id_names = self.get_value_id_name(name, dirty_data)
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
    def parse(self, input_array, dirtydata):
        df = create(input_array, dirtydata)
        self.create_excel(df)





#parse(sys.argv[3].split(","), sys.argv[1])
